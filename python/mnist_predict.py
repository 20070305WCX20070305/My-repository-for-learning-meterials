"""
Handwritten digit recognition -- train a model + predict digits from images

Features:
  1. Auto-download MNIST dataset and train a 3-layer neural network
  2. Save trained model weights to file (model_weights.npz)
  3. Read any image, preprocess it, predict the digit and show results

Usage:
  python mnist_predict.py                     # train + evaluate on test set
  python mnist_predict.py my_digit.png        # predict a specific image

Dependencies:
  pip install numpy matplotlib pillow
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# ================================================================
# Activation functions
# ================================================================

def sigmoid(z):
    return 1 / (1 + np.exp(-np.clip(z, -250, 250)))


def sigmoid_derivative(a):
    return a * (1 - a)


def relu(z):
    return np.maximum(0, z)


def relu_derivative(a):
    return (a > 0).astype(float)


def softmax(z):
    """
    Softmax -- convert logits to probability distribution.
    Each column (one sample) sums to 1.
    """
    z_shifted = z - np.max(z, axis=0, keepdims=True)
    exp_z = np.exp(z_shifted)
    return exp_z / np.sum(exp_z, axis=0, keepdims=True)


# ================================================================
# Neural network model
# ================================================================

class MNISTClassifier:
    """
    3-layer fully-connected neural network.

    Architecture: Input(784) -> Hidden1(128, ReLU) -> Hidden2(64, ReLU) -> Output(10, Softmax)
    """

    def __init__(self, input_size=784, hidden1_size=128, hidden2_size=64, output_size=10):
        # He initialization (recommended for ReLU)
        self.W1 = np.random.randn(hidden1_size, input_size) * np.sqrt(2.0 / input_size)
        self.b1 = np.zeros((hidden1_size, 1))
        self.W2 = np.random.randn(hidden2_size, hidden1_size) * np.sqrt(2.0 / hidden1_size)
        self.b2 = np.zeros((hidden2_size, 1))
        self.W3 = np.random.randn(output_size, hidden2_size) * np.sqrt(2.0 / hidden2_size)
        self.b3 = np.zeros((output_size, 1))

        self.loss_history = []
        self.accuracy_history = []

    def forward(self, X):
        """
        Forward propagation.

        Args:
            X: input of shape (784, batch_size)

        Returns:
            a3: softmax output of shape (10, batch_size), each column is a probability distribution
        """
        self.z1 = np.dot(self.W1, X) + self.b1
        self.a1 = relu(self.z1)
        self.z2 = np.dot(self.W2, self.a1) + self.b2
        self.a2 = relu(self.z2)
        self.z3 = np.dot(self.W3, self.a2) + self.b3
        self.a3 = softmax(self.z3)
        return self.a3

    def backward(self, X, y, output):
        """Backpropagation using the chain rule."""
        m = X.shape[1]

        # Output layer: softmax + cross-entropy gradient = (output - y) / m
        dz3 = (output - y) / m
        dW3 = np.dot(dz3, self.a2.T)
        db3 = np.sum(dz3, axis=1, keepdims=True)

        # Hidden layer 2
        dL_da2 = np.dot(self.W3.T, dz3)
        dz2 = dL_da2 * relu_derivative(self.a2)
        dW2 = np.dot(dz2, self.a1.T)
        db2 = np.sum(dz2, axis=1, keepdims=True)

        # Hidden layer 1
        dL_da1 = np.dot(self.W2.T, dz2)
        dz1 = dL_da1 * relu_derivative(self.a1)
        dW1 = np.dot(dz1, X.T)
        db1 = np.sum(dz1, axis=1, keepdims=True)

        return dW1, db1, dW2, db2, dW3, db3

    def update_params(self, grads, learning_rate):
        dW1, db1, dW2, db2, dW3, db3 = grads
        self.W1 -= learning_rate * dW1
        self.b1 -= learning_rate * db1
        self.W2 -= learning_rate * dW2
        self.b2 -= learning_rate * db2
        self.W3 -= learning_rate * dW3
        self.b3 -= learning_rate * db3

    def compute_loss(self, y_true, y_pred):
        """Cross-entropy loss."""
        eps = 1e-12
        y_pred = np.clip(y_pred, eps, 1 - eps)
        return -np.sum(y_true * np.log(y_pred)) / y_true.shape[1]

    def compute_accuracy(self, X, y):
        """Compute classification accuracy."""
        output = self.forward(X)
        predictions = np.argmax(output, axis=0)
        labels = np.argmax(y, axis=0)
        return np.mean(predictions == labels)

    def train(self, X_train, y_train, X_val=None, y_val=None,
              epochs=30, batch_size=64, learning_rate=0.1, verbose=True):
        """Mini-batch gradient descent training."""
        n_samples = X_train.shape[1]

        print(f"Training samples: {n_samples}, Batch size: {batch_size}, Epochs: {epochs}")

        for epoch in range(epochs):
            # Shuffle data at the start of each epoch
            indices = np.random.permutation(n_samples)
            X_shuffled = X_train[:, indices]
            y_shuffled = y_train[:, indices]

            epoch_loss = 0
            n_batches = 0

            for start in range(0, n_samples, batch_size):
                end = min(start + batch_size, n_samples)
                X_batch = X_shuffled[:, start:end]
                y_batch = y_shuffled[:, start:end]

                output = self.forward(X_batch)
                batch_loss = self.compute_loss(y_batch, output)
                epoch_loss += batch_loss
                n_batches += 1

                grads = self.backward(X_batch, y_batch, output)
                self.update_params(grads, learning_rate)

            avg_loss = epoch_loss / n_batches
            self.loss_history.append(avg_loss)
            train_acc = self.compute_accuracy(X_train, y_train)
            self.accuracy_history.append(train_acc)

            if verbose and (epoch + 1) % 5 == 0:
                val_str = ""
                if X_val is not None and y_val is not None:
                    val_acc = self.compute_accuracy(X_val, y_val)
                    val_str = f", Val Acc: {val_acc:.4f}"
                print(f"Epoch {epoch + 1:3d}/{epochs}, Loss: {avg_loss:.4f}, "
                      f"Train Acc: {train_acc:.4f}{val_str}")

    def predict(self, X):
        """
        Predict digit labels.

        Returns:
            predictions: digit labels (0-9)
            confidences: confidence scores for the predicted labels
            all_probs: full probability distribution over all 10 classes
        """
        output = self.forward(X)
        predictions = np.argmax(output, axis=0)
        confidences = np.max(output, axis=0)
        return predictions, confidences, output

    # ========== Model save / load ==========

    def save_weights(self, filepath="model_weights.npz"):
        """Save model parameters to a .npz file."""
        np.savez(filepath,
                 W1=self.W1, b1=self.b1,
                 W2=self.W2, b2=self.b2,
                 W3=self.W3, b3=self.b3)
        print(f"Model weights saved to: {filepath}")

    def load_weights(self, filepath="model_weights.npz"):
        """Load model parameters from a .npz file."""
        if not os.path.exists(filepath):
            print(f"Weight file not found: {filepath}")
            return False
        data = np.load(filepath)
        self.W1 = data["W1"]
        self.b1 = data["b1"]
        self.W2 = data["W2"]
        self.b2 = data["b2"]
        self.W3 = data["W3"]
        self.b3 = data["b3"]
        print(f"Model weights loaded from: {filepath}")
        return True


# ================================================================
# MNIST data loader (auto-download)
# ================================================================

def load_mnist_images(filename):
    """Read MNIST images from IDX format, return (784, n) array with pixel values 0-1."""
    with open(filename, 'rb') as f:
        magic = int.from_bytes(f.read(4), 'big')
        n_images = int.from_bytes(f.read(4), 'big')
        n_rows = int.from_bytes(f.read(4), 'big')
        n_cols = int.from_bytes(f.read(4), 'big')
        images = np.frombuffer(f.read(), dtype=np.uint8)
        images = images.reshape(n_images, n_rows * n_cols).T
        images = images / 255.0
    return images


def load_mnist_labels(filename):
    """Read MNIST labels from IDX format, return one-hot encoding (10, n)."""
    with open(filename, 'rb') as f:
        labels = np.frombuffer(f.read(), dtype=np.uint8, offset=8)
    one_hot = np.zeros((10, labels.shape[0]))
    one_hot[labels, np.arange(labels.shape[0])] = 1
    return one_hot


def download_mnist(save_dir="./mnist_data"):
    """Auto-download and extract the MNIST dataset."""
    import urllib.request
    import gzip

    save_dir = Path(save_dir)
    save_dir.mkdir(exist_ok=True)

    base_url = "https://storage.googleapis.com/cvdf-datasets/mnist/"
    files = {
        "train-images-idx3-ubyte": "train-images-idx3-ubyte.gz",
        "train-labels-idx1-ubyte": "train-labels-idx1-ubyte.gz",
        "t10k-images-idx3-ubyte": "t10k-images-idx3-ubyte.gz",
        "t10k-labels-idx1-ubyte": "t10k-labels-idx1-ubyte.gz",
    }

    for file_name, gz_name in files.items():
        file_path = save_dir / file_name
        if file_path.exists():
            print(f"  [Exists] {file_name}")
            continue

        url = base_url + gz_name
        gz_path = save_dir / gz_name
        print(f"  [Downloading] {url}...")
        urllib.request.urlretrieve(url, gz_path)
        print(f"  [Extracting] {gz_name}...")
        with gzip.open(gz_path, 'rb') as f_in:
            with open(file_path, 'wb') as f_out:
                f_out.write(f_in.read())
        gz_path.unlink()
        print(f"  [Done] {file_name}")

    print("  MNIST dataset ready!")


def load_mnist(data_dir="./mnist_data"):
    """Load MNIST dataset (auto-download if needed)."""
    print("Preparing MNIST dataset...")
    download_mnist(data_dir)

    print("Loading training set...")
    X_train = load_mnist_images(f"{data_dir}/train-images-idx3-ubyte")
    y_train = load_mnist_labels(f"{data_dir}/train-labels-idx1-ubyte")

    print("Loading test set...")
    X_test = load_mnist_images(f"{data_dir}/t10k-images-idx3-ubyte")
    y_test = load_mnist_labels(f"{data_dir}/t10k-labels-idx1-ubyte")

    return (X_train, y_train), (X_test, y_test)


# ================================================================
# Image preprocessing -- convert any image to MNIST format
# ================================================================

def preprocess_image(image_path, show=True):
    """
    Read an image and preprocess it to match MNIST format.

    Processing steps:
      1. Load image -> grayscale
      2. Resize to 28x28
      3. MNIST uses white digits on a black background.
         If the input is black-on-white, invert it.
      4. Normalize to 0-1
      5. Flatten to a 784-dim vector

    Args:
        image_path: path to the image file
        show: whether to display before/after comparison

    Returns:
        image_vector: shape (784, 1), ready for model inference
    """
    from PIL import Image

    # Open the image
    img = Image.open(image_path)

    # Convert to grayscale (mode 'L': each pixel 0-255)
    img_gray = img.convert("L")

    # Resize to 28x28 (MNIST standard size)
    img_resized = img_gray.resize((28, 28), Image.Resampling.LANCZOS)

    # Convert to numpy array, shape (28, 28), value range 0-255
    pixels = np.array(img_resized, dtype=np.uint8)

    # ---- Decide whether to invert ----
    # MNIST data has white digits (255) on a black background (0).
    # If the user's image has dark text on a light background,
    # the mean pixel value will be > 128, and we need to invert.
    if np.mean(pixels) > 128:
        # Black text on white background -> invert to MNIST style
        pixels = 255 - pixels

    # Normalize to 0-1
    pixels_normalized = pixels.astype(np.float32) / 255.0

    # Flatten to 784-dim vector and reshape to (784, 1)
    image_vector = pixels_normalized.reshape(784, 1)

    # ---- Visualization ----
    if show:
        fig, axes = plt.subplots(1, 3, figsize=(12, 3))
        axes[0].imshow(img.resize((100, 100)))
        axes[0].set_title("Original")
        axes[0].axis("off")

        axes[1].imshow(img_resized, cmap="gray")
        axes[1].set_title("Resized 28x28")
        axes[1].axis("off")

        axes[2].imshow(pixels_normalized, cmap="gray")
        axes[2].set_title("Normalized (model input)")
        axes[2].axis("off")

        plt.tight_layout()
        plt.show()

    return image_vector


# ================================================================
# Predict a single image
# ================================================================

def predict_single_image(model, image_path, show=True):
    """
    Predict the digit in a single image.

    Args:
        model: trained MNISTClassifier instance
        image_path: path to the image file
        show: whether to display processing steps and results

    Returns:
        digit: predicted digit (0-9)
        confidence: confidence score (0-1)
    """
    # Preprocess the image
    img_vector = preprocess_image(image_path, show=show)

    # Predict
    digit, confidence, all_probs = model.predict(img_vector)
    digit = int(digit[0])
    confidence = float(confidence[0])

    # Print results
    print(f"\n{'=' * 40}")
    print(f"  Prediction: {digit}")
    print(f"  Confidence: {confidence:.4f} ({confidence * 100:.2f}%)")
    print(f"{'=' * 40}")

    # Display probability distribution over all classes
    probs = all_probs[:, 0]
    labels = list(range(10))

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    # Left: input image
    axes[0].imshow(img_vector.reshape(28, 28), cmap="gray")
    axes[0].set_title(f"Input Image\nPrediction: {digit}  (Confidence: {confidence:.2%})")
    axes[0].axis("off")

    # Right: probability bar chart
    colors = ["#1f77b4"] * 10
    colors[digit] = "#ff7f0e"
    axes[1].bar(labels, probs, color=colors)
    axes[1].set_xlabel("Digit")
    axes[1].set_ylabel("Probability")
    axes[1].set_title("Prediction Probabilities by Class")
    axes[1].set_xticks(labels)
    axes[1].grid(axis="y", alpha=0.3)

    for i, p in enumerate(probs):
        if p > 0.01:
            axes[1].text(i, p + 0.01, f"{p:.1%}", ha="center", fontsize=9)

    plt.tight_layout()
    plt.show()

    return digit, confidence


# ================================================================
# Utility: generate a test digit image for demonstration
# ================================================================

def generate_test_digit(digit=5, save_path="test_digit.png"):
    """
    Generate a simulated handwritten digit image for testing.
    In practice, use a real scanned or drawn image instead.
    """
    from PIL import Image, ImageDraw, ImageFont

    img = Image.new("L", (140, 140), color=255)
    draw = ImageDraw.Draw(img)

    # Try using system fonts; fallback to a rough drawing
    try:
        if sys.platform == "win32":
            font = ImageFont.truetype("arial.ttf", 100)
        elif sys.platform == "darwin":
            font = ImageFont.truetype(
                "/System/Library/Fonts/Supplemental/Arial.ttf", 100)
        else:
            font = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 100)
        draw.text((20, 10), str(digit), fill=0, font=font)
    except (OSError, IOError):
        # Fallback: draw a rough digit shape using rectangles
        draw.rectangle([20, 10, 50, 130], fill=0)
        draw.rectangle([20, 10, 120, 40], fill=0)
        draw.rectangle([20, 70, 120, 100], fill=0)
        draw.rectangle([90, 10, 120, 130], fill=0)

    img.save(save_path)
    print(f"Test image saved: {save_path}  (digit: {digit})")
    return save_path


# ================================================================
# Main
# ================================================================

WEIGHTS_FILE = "model_weights.npz"


def main():
    # -------- Prepare / load model --------
    model = MNISTClassifier()

    # Try loading existing weights; train if not found
    if model.load_weights(WEIGHTS_FILE):
        print("Loaded existing model. Skipping training.")
    else:
        print("No saved model found. Starting training...\n")
        np.random.seed(42)

        # Load MNIST data
        (X_train, y_train), (X_test, y_test) = load_mnist()

        # Split off a validation set
        val_size = 5000
        X_val = X_train[:, :val_size]
        y_val = y_train[:, :val_size]
        X_train = X_train[:, val_size:]
        y_train = y_train[:, val_size:]

        print(f"\nTraining set: {X_train.shape[1]} images, "
              f"Validation set: {X_val.shape[1]} images, "
              f"Test set: {X_test.shape[1]} images\n")

        # Train
        model.train(X_train, y_train, X_val, y_val,
                    epochs=30, batch_size=64, learning_rate=0.1)

        # Evaluate on test set
        test_acc = model.compute_accuracy(X_test, y_test)
        print(f"\nTest set accuracy: {test_acc:.4f} ({test_acc * 100:.2f}%)")

        # Save model
        model.save_weights(WEIGHTS_FILE)

        # Show training curves
        plt.figure(figsize=(12, 4))
        plt.subplot(1, 2, 1)
        plt.plot(model.loss_history)
        plt.title("Training Loss")
        plt.xlabel("Epoch")
        plt.ylabel("Loss")
        plt.grid(True)

        plt.subplot(1, 2, 2)
        plt.plot(model.accuracy_history)
        plt.title("Training Accuracy")
        plt.xlabel("Epoch")
        plt.ylabel("Accuracy")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    # -------- Handle command-line argument --------
    if len(sys.argv) >= 2:
        # Usage: python mnist_predict.py <image_path>
        image_path = sys.argv[1]
        if not os.path.exists(image_path):
            print(f"Error: image not found '{image_path}'")
            return
        predict_single_image(model, image_path, show=True)

    else:
        # No image provided; generate a local test image for demonstration
        print("\nNo image specified. Generating a local test image for demo...")
        test_path = generate_test_digit(digit=8, save_path="test_digit.png")
        predict_single_image(model, test_path, show=True)


if __name__ == "__main__":
    main()
