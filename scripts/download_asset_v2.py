import numpy as np

print("Downloading MNIST dataset VERSION 2...")
# Load MNIST dataset v1
x_train_v1 = np.load('data/raw/mnist_x_train_v1.npy')
y_train_v1 = np.load('data/raw/mnist_y_train_v1.npy')

np.random.seed(42)
# Get random 1000 samples
indices = np.random.choice(len(x_train_v1), 1000, replace=False)

x_train_v2 = x_train_v1[indices]
y_train_v2 = y_train_v1[indices]

np.save('data/raw/mnist_x_train_v2.npy', x_train_v2)
np.save('data/raw/mnist_y_train_v2.npy', y_train_v2)

print(f"V2 - Training MNIST data: {x_train_v2.shape} (1000 samples)")