import argparse
import json
import os

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

DEFAULT_N_ESTIMATORS = 10
DEFAULT_MAX_DEPTH = 10
DEFAULT_RANDOM_STATE = 42

def train_model(version):
    print(f"Model training for MNIST dataset VERSION {version}...")

    # Load MNIST dataset based on version
    x_train = np.load(f'data/raw/mnist_x_train_{version}.npy')
    y_train = np.load(f'data/raw/mnist_y_train_{version}.npy')
    x_test = np.load('data/raw/mnist_x_test_v1.npy')
    y_test = np.load('data/raw/mnist_y_test_v1.npy')
    print(f"Training data shape: {x_train.shape}, Training labels shape: {y_train.shape}")

    # Load params
    if os.path.exists('params.yaml'):
        import yaml
        with open('params.yaml', 'r') as f:
            params = yaml.safe_load(f)
        print(f"Loaded params: {params}")
    else:
        params = {}
        print("No params.yaml found, using default parameters.")

    # Flatten and normalize
    x_train = x_train.reshape(x_train.shape[0], -1) / 255.0
    x_test = x_test.reshape(x_test.shape[0], -1) / 255.0

    # Train a simple RandomForest model
    print(f"Traiing model on {x_train.shape[0]} samples...")
    print(f"Model parameters: {params['model']}")
    model_params = params.get('model', {})
    n_estimators = model_params.get('n_estimators', DEFAULT_N_ESTIMATORS)
    max_depth = model_params.get('max_depth', DEFAULT_MAX_DEPTH)
    random_state = model_params.get('random_state', DEFAULT_RANDOM_STATE)
    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=random_state)
    model.fit(x_train, y_train)

    # Evaluate the model
    y_pred = model.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Test Accuracy: {accuracy}")

    # Save the model and metrics
    os.makedirs('models', exist_ok=True)
    np.save(f'models/rf_mnist_{version}.npy', model)

    metrics = {
        'accuracy': float(accuracy),
        'dataset_size': int(x_train.shape[0]),
        'dataset_version': version,
        'model_type': 'RandomForest',
        'model_version': version,
        'parameters': params['model']
    }
    with open(f'models/metrics_{version}.json', 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"Model and metrics saved for VERSION {version}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True, choices=['v1', 'v2', 'v3'])
    args = parser.parse_args()

    train_model(args.version)
    print(f"Model training for MNIST dataset VERSION {args.version} completed.")