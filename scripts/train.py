import argparse
import json
import os

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def train_model(version):
    print(f"Model training for MNIST dataset VERSION {version}...")
    # Load MNIST dataset based on version
    x_train = np.load(f'data/raw/mnist_x_train_{version}.npy')
    y_train = np.load(f'data/raw/mnist_y_train_{version}.npy')
    x_test = np.load('data/raw/mnist_x_test_v1.npy')
    y_test = np.load('data/raw/mnist_y_test_v1.npy')
    print(f"Training data shape: {x_train.shape}, Training labels shape: {y_train.shape}")

    # Flatten and normalize
    x_train = x_train.reshape(x_train.shape[0], -1) / 255.0
    x_test = x_test.reshape(x_test.shape[0], -1) / 255.0

    # Train a simple RandomForest model
    print(f"Traiing model on {x_train.shape[0]} samples...")
    model = RandomForestClassifier(n_estimators=10, max_depth=10, random_state=42)
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