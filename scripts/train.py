import numpy as np
import json
import os

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load MNIST dataset
print("Loading MNIST dataset...")
x_train = np.load('data/raw/mnist_x_train.npy')
y_train = np.load('data/raw/mnist_y_train.npy')
x_test = np.load('data/raw/mnist_x_test_v1.npy')
y_test = np.load('data/raw/mnist_y_test_v1.npy')

# Flatten the images and normalize pixel values
x_train = x_train.reshape((x_train.shape[0], -1)) / 255.0
x_test = x_test.reshape((x_test.shape[0], -1)) / 255.0

print("Training on {len} samples...".format(len=len(x_train)))

# Train a Random Forest classifier
clf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
clf.fit(x_train, y_train)

# Evaluate the model
y_pred = clf.predict(x_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy on test set: {accuracy * 100:.2f}%")

# Save the trained model and metrics
os.makedirs('models', exist_ok=True)
np.save('models/rf_mnist.npy', clf)

metrics = {
    'accuracy': accuracy,
    'dataset_size': len(x_train),
    'dataset_version': 'unknown',  # Could be set to a specific version if tracked
    'model': 'RandomForestClassifier'
}

with open('models/metrics.json', 'w') as f:
    json.dump(metrics, f, indent=4)
print("Training complete. Model and metrics saved.")