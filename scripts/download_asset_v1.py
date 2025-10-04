import tensorflow as tf
import numpy as np
import os

print("Downloading MNIST dataset VERSION 1...")
# Load MNIST dataset
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

# Save the dataset as .npy files
np.save('data/raw/mnist_x_train_v1.npy', x_train)
np.save('data/raw/mnist_y_train_v1.npy', y_train)
np.save('data/raw/mnist_x_test_v1.npy', x_test)
np.save('data/raw/mnist_y_test_v1.npy', y_test)

print("MNIST dataset VERSION 1 downloaded and saved as .npy files.")

print(f"Train images shape: {x_train.shape}")
print(f"Test images shape: {x_test.shape}")