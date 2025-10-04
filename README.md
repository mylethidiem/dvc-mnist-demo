Note:
- This project is from my learning in AIO2025 class - AI VIET NAM \
- Reference source: https://github.com/dangnha/dvc-mnist-demo

# MNIST Practice with DVC(Data Version Control)


## Install DVC
Follow this doc: https://dvc.org/doc/start
Recommend using Python version 3.10-3.11
Install requirements packages:
```bash
pip install -r requirements.txt
```

## Add data version 1
### Download MNIST Dateset
The data will saving as [standard binary file format](https://github.com/numpy/numpy/blob/067cb067cb17a20422e51da908920a4fbb3ab851/doc/neps/nep-0001-npy-format.rst). We can use other format like parquet to optimize the storage
```bash
python ./scripts/download_asset_v1.py
```
### DVC init and add data
```bash
dvc init
dvc add data/raw/mnist_x_train_v1.npy
```

Add meta data in `npy.dvc` file to track the data version
```
meta:
  version: v1.0
  date: 10/04/2025
  author: banhmuy
  description: MNIST dataset version 1
```

Add `cache_under.txt` by dvc
```bash
data add cache_under.txt
```

Try to change `cache_under.txt` and run `dvc status` to see the change. Run `dvc add cache_under.txt` to update the cache.
It save another hash for this  in `cache_under.txt.dvc` file and when pushing, it will push cache version

Push the last files in MNIST dataset to remote storage
```bash
dvc add data/raw/mnist_y_train_v1.npy
dvc add data/raw/mnist_x_test_v1.npy
dvc add data/raw/mnist_y_test_v1.npy
```

Git add and commit the `.dvc` files. It will push the `.npy.dvc` containing the meta data and hash of the data, ignore the `.npy` files.
It can download the data(Cache will store in cloud) from remote storage by `dvc pull` command.

There is a connection between the dvc version with git version.

Add the train file to train data

## Train the model and how to pull the data storage
Goto `data/raw`
Symbolic link for data:
```bash
mklink x_train.npy x_train_v1.npy
```
For Linux/WSL:
```bash
ln -s mnist_x_train_v1.npy mnist_x_train.npy
ln -s mnist_y_train_v1.npy mnist_y_train.npy
ln -s mnist_x_test_v1.npy mnist_x_test.npy
ln -s mnist_y_test_v1.npy mnist_y_test.npy
```
Run train.py to train the model and save the model and metrics.
Run dvc add to add the model and metrics to dvc.
```bash
dvc add models/rf_mnist.npy
dvc add models/metrics.json
```
Create local storage contain the data cache:
```bash
mkdir ../dvc_storage

dvc remote add -d local ../dvc_storage
```
Remove local stograge if already exist:
```bash
dvc remote remove local
```
When you want to pull the dvc storage to your local machine, create a folder with the same level as git folder and run:
```bash
dvc remote add -d local ../your_dvc_storage
dvc pull
```
## Add data version 2
Create new data version 2 and add it to dvc.
```bash
dvc add data/raw/mnist_x_train_v2.npy
dvc add data/raw/mnist_y_train_v2.npy
```

DVC have no version, it bases on git to track the version of the data. DVC itself does not reinvent the version control system. Instead, it is designed to extend Git to handle large files, data, and models.

Create new symbol link to the new data version 2 and retrain the model.
```bash
cd data/raw
rm mnist_x_train.npy mnist_y_train.npy

# Create new
ln -s mnist_x_train_v2.npy mnist_x_train.npy
ln -s mnist_y_train_v2.npy mnist_y_train.npy

cd ../..

# Retrain model
python scripts/train.py

# dvc v2
dvc add models/metrics.json
dvc add models/rf_mnist.npy
```

