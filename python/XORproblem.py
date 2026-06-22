import numpy as np
import matplotlib.pyplot as plt


# ================================================================
# 激活函数
# ================================================================

def sigmoid(z):
    """Sigmoid 激活"""
    return 1 / (1 + np.exp(-np.clip(z, -250, 250)))


def sigmoid_derivative(a):
    """Sigmoid 导数"""
    return a * (1 - a)


def softmax(z):
    """
    Softmax 激活函数 —— 用于多分类输出层

    将输出向量转为概率分布（所有值之和为 1）
    
    公式: softmax(z_i) = exp(z_i) / Σ_j exp(z_j)

    参数:
        z: 形状 (n_classes, batch_size)

    返回:
        概率分布，每个值在 0~1 之间，列之和为 1
    """
    # 减去最大值防止 exp 溢出
    z_shifted = z - np.max(z, axis=0, keepdims=True)
    exp_z = np.exp(z_shifted)
    return exp_z / np.sum(exp_z, axis=0, keepdims=True)


def relu(z):
    """
    ReLU 激活函数: max(0, z)

    优点：
    - 计算简单，比 sigmoid 快
    - 缓解梯度消失问题
    - 实践中比 sigmoid/tanh 效果好
    """
    return np.maximum(0, z)


def relu_derivative(a):
    """
    ReLU 导数: z > 0 时为 1，否则为 0
    注意：a 已经是 relu(z) 的输出，但 relu 在 z=0 处不可导
    """
    return (a > 0).astype(float)


# ================================================================
# 多层神经网络（适用于 MNIST 等复杂任务）
# ================================================================

class MNISTClassifier:
    """
    三层神经网络分类器

    网络结构:
        输入层(784) → 隐藏层1(128, ReLU) → 隐藏层2(64, ReLU) → 输出层(10, Softmax)

    为什么用这个结构？
    - 输入 784：28×28 图片拉平
    - 隐藏层 128/64：足够的容量学习特征
    - 输出 10：10 个数字 (0~9)
    - ReLU：比 sigmoid 更高效，梯度消失问题更少
    - Softmax：多分类的标准输出层，输出概率分布
    """

    def __init__(self, input_size=784, hidden1_size=128, hidden2_size=64, output_size=10):
        """
        初始化参数

        使用 He 初始化（适合 ReLU）：均值为 0，方差为 2/n_in
        相比随机小值初始化，He 初始化让深层的梯度流动更顺畅
        """
        # 输入层 → 隐藏层1
        self.W1 = np.random.randn(hidden1_size, input_size) * np.sqrt(2.0 / input_size)
        self.b1 = np.zeros((hidden1_size, 1))

        # 隐藏层1 → 隐藏层2
        self.W2 = np.random.randn(hidden2_size, hidden1_size) * np.sqrt(2.0 / hidden1_size)
        self.b2 = np.zeros((hidden2_size, 1))

        # 隐藏层2 → 输出层
        self.W3 = np.random.randn(output_size, hidden2_size) * np.sqrt(2.0 / hidden2_size)
        self.b3 = np.zeros((output_size, 1))

        self.loss_history = []
        self.accuracy_history = []

    def forward(self, X):
        """
        正向传播

        参数:
            X: 输入，形状 (784, batch_size)
               每个样本是 784 维向量（28×28 拉平）

        返回:
            a3: softmax 概率输出，形状 (10, batch_size)
        """
        # 隐藏层1：线性变换 + ReLU
        self.z1 = np.dot(self.W1, X) + self.b1
        self.a1 = relu(self.z1)

        # 隐藏层2：线性变换 + ReLU
        self.z2 = np.dot(self.W2, self.a1) + self.b2
        self.a2 = relu(self.z2)

        # 输出层：线性变换 + Softmax（得到概率分布）
        self.z3 = np.dot(self.W3, self.a2) + self.b3
        self.a3 = softmax(self.z3)

        return self.a3

    def backward(self, X, y, output):
        """
        反向传播

        参数:
            X: 输入，形状 (784, batch_size)
            y: 真实标签（one-hot 编码），形状 (10, batch_size)
            output: 预测概率，形状 (10, batch_size)
        """
        m = X.shape[1]  # batch 大小

        # ========== 输出层误差 ==========
        # 对于 softmax + cross-entropy，梯度是 (output - y) / m（推导省略）
        dz3 = (output - y) / m

        dW3 = np.dot(dz3, self.a2.T)
        db3 = np.sum(dz3, axis=1, keepdims=True)

        # ========== 隐藏层 2 ==========
        dL_da2 = np.dot(self.W3.T, dz3)
        dz2 = dL_da2 * relu_derivative(self.a2)

        dW2 = np.dot(dz2, self.a1.T)
        db2 = np.sum(dz2, axis=1, keepdims=True)

        # ========== 隐藏层 1 ==========
        dL_da1 = np.dot(self.W2.T, dz2)
        dz1 = dL_da1 * relu_derivative(self.a1)

        dW1 = np.dot(dz1, X.T)
        db1 = np.sum(dz1, axis=1, keepdims=True)

        return dW1, db1, dW2, db2, dW3, db3

    def update_params(self, grads, learning_rate):
        """梯度下降更新"""
        dW1, db1, dW2, db2, dW3, db3 = grads
        self.W1 -= learning_rate * dW1
        self.b1 -= learning_rate * db1
        self.W2 -= learning_rate * dW2
        self.b2 -= learning_rate * db2
        self.W3 -= learning_rate * dW3
        self.b3 -= learning_rate * db3

    def compute_loss(self, y_true, y_pred):
        """
        交叉熵损失

        为什么用交叉熵而不是 MSE？
        - 分类任务中，交叉熵的梯度更"陡峭"，学习更快
        - MSE 在 softmax 输出下梯度会很小，学习缓慢
        """
        eps = 1e-12
        y_pred = np.clip(y_pred, eps, 1 - eps)
        return -np.sum(y_true * np.log(y_pred)) / y_true.shape[1]

    def compute_accuracy(self, X, y):
        """
        计算准确率

        参数:
            X: 输入数据
            y: one-hot 标签

        返回:
            准确率（0~1 之间）
        """
        output = self.forward(X)
        predictions = np.argmax(output, axis=0)
        labels = np.argmax(y, axis=0)
        return np.mean(predictions == labels)

    def train(self, X_train, y_train, X_val=None, y_val=None,
              epochs=50, batch_size=32, learning_rate=0.01, verbose=True):
        """
        完整训练过程

        参数:
            X_train: 训练数据 (784, n_train)
            y_train: one-hot 标签 (10, n_train)
            X_val: 验证数据（可选）
            y_val: 验证标签（可选）
            epochs: 遍历整个训练集的次数
            batch_size: 每次参数更新用的样本数
            learning_rate: 学习率
            verbose: 是否打印进度
        """
        n_samples = X_train.shape[1]

        print(f"开始训练...")
        print(f"训练样本数: {n_samples}")
        print(f"批次大小: {batch_size}")
        print(f"每轮迭代数: {n_samples // batch_size}")
        print(f"训练轮数: {epochs}")
        print(f"=" * 50)

        for epoch in range(epochs):
            # -------- 打乱数据（至关重要！）--------
            # 如果不打乱，网络可能会学到样本顺序中的虚假模式
            indices = np.random.permutation(n_samples)
            X_shuffled = X_train[:, indices]
            y_shuffled = y_train[:, indices]

            epoch_loss = 0
            n_batches = 0

            # -------- 小批量梯度下降 --------
            for start in range(0, n_samples, batch_size):
                end = min(start + batch_size, n_samples)

                # 取出一个小批量
                X_batch = X_shuffled[:, start:end]
                y_batch = y_shuffled[:, start:end]

                # 正向传播
                output = self.forward(X_batch)

                # 计算损失
                batch_loss = self.compute_loss(y_batch, output)
                epoch_loss += batch_loss
                n_batches += 1

                # 反向传播
                grads = self.backward(X_batch, y_batch, output)

                # 更新参数
                self.update_params(grads, learning_rate)

            # -------- 记录损失和准确率 --------
            avg_loss = epoch_loss / n_batches
            self.loss_history.append(avg_loss)

            train_acc = self.compute_accuracy(X_train, y_train)
            self.accuracy_history.append(train_acc)

            # -------- 打印进度 --------
            if verbose and (epoch + 1) % 5 == 0:
                val_str = ""
                if X_val is not None and y_val is not None:
                    val_acc = self.compute_accuracy(X_val, y_val)
                    val_str = f", 验证准确率: {val_acc:.4f}"
                print(f"Epoch {epoch + 1:3d}/{epochs}, Loss: {avg_loss:.4f}, "
                      f"训练准确率: {train_acc:.4f}{val_str}")

    def predict(self, X):
        """预测类别（返回 0~9 的数字）"""
        output = self.forward(X)
        return np.argmax(output, axis=0)

    def show_predictions(self, X, y, num_samples=10):
        """展示预测结果"""
        indices = np.random.choice(X.shape[1], num_samples, replace=False)
        predictions = self.predict(X[:, indices])
        labels = np.argmax(y[:, indices], axis=0)

        fig, axes = plt.subplots(2, 5, figsize=(12, 5))
        axes = axes.ravel()

        for i, idx in enumerate(range(num_samples)):
            ax = axes[i]
            img = X[:, indices[idx]].reshape(28, 28)
            ax.imshow(img, cmap='gray')
            color = 'green' if predictions[idx] == labels[idx] else 'red'
            ax.set_title(f"预测: {predictions[idx]}, 真实: {labels[idx]}",
                        color=color)
            ax.axis('off')

        plt.tight_layout()
        plt.show()


# ================================================================
# 数据加载 —— 从 MNIST 原始文件读取
# ================================================================

def load_mnist_images(filename):
    """
    从 IDX 格式文件读取 MNIST 图片

    MNIST 文件格式:
    - 前 4 个字节: magic number
    - 接下来 4 个字节: 图片数量
    - 接下来 4 个字节: 行数
    - 接下来 4 个字节: 列数
    - 之后是一个个像素值

    返回:
        numpy 数组，形状 (784, n_samples)，每个像素值 0~1
    """
    with open(filename, 'rb') as f:
        # 读取文件头
        magic = int.from_bytes(f.read(4), 'big')
        n_images = int.from_bytes(f.read(4), 'big')
        n_rows = int.from_bytes(f.read(4), 'big')
        n_cols = int.from_bytes(f.read(4), 'big')

        print(f"  图片数: {n_images}, 尺寸: {n_rows}x{n_cols}")

        # 读取像素数据
        images = np.frombuffer(f.read(), dtype=np.uint8)
        images = images.reshape(n_images, n_rows * n_cols).T  # 转置为 (784, n)

        # 归一化到 0~1（原始像素值 0~255）
        images = images / 255.0

    return images


def load_mnist_labels(filename):
    """
    从 IDX 格式文件读取 MNIST 标签

    标签文件格式:
    - 前 4 个字节: magic number
    - 接下来 4 个字节: 标签数量
    - 之后是一个个标签值 (0~9)

    返回:
        one-hot 编码矩阵，形状 (10, n_samples)
    """
    with open(filename, 'rb') as f:
        magic = int.from_bytes(f.read(4), 'big')
        n_labels = int.from_bytes(f.read(4), 'big')

        print(f"  标签数: {n_labels}")

        # 读取标签
        labels = np.frombuffer(f.read(), dtype=np.uint8)

    # 转为 one-hot 编码
    # 例如标签 3 → [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
    one_hot = np.zeros((10, n_labels))
    one_hot[labels, np.arange(n_labels)] = 1

    return one_hot


def download_mnist(save_dir="./mnist_data"):
    """
    下载 MNIST 数据集

    如果文件已存在，跳过下载。
    如果不存在，从 Yann LeCun 的网站下载。

    MNIST 数据集包含 4 个文件:
    - train-images-idx3-ubyte: 训练图片 (60000 张)
    - train-labels-idx1-ubyte: 训练标签 (60000 个)
    - t10k-images-idx3-ubyte:  测试图片  (10000 张)
    - t10k-labels-idx1-ubyte:  测试标签  (10000 个)
    """
    import os
    import urllib.request
    import gzip

    # 创建保存目录
    os.makedirs(save_dir, exist_ok=True)

    # MNIST 文件的 URL
    base_url = "https://storage.googleapis.com/cvdf-datasets/mnist/"
    files = {
        "train-images-idx3-ubyte": "train-images-idx3-ubyte.gz",
        "train-labels-idx1-ubyte": "train-labels-idx1-ubyte.gz",
        "t10k-images-idx3-ubyte": "t10k-images-idx3-ubyte.gz",
        "t10k-labels-idx1-ubyte": "t10k-labels-idx1-ubyte.gz",
    }

    for file_name, gz_name in files.items():
        file_path = os.path.join(save_dir, file_name)
        gz_path = os.path.join(save_dir, gz_name)

        if os.path.exists(file_path):
            print(f"[已存在] {file_name}")
            continue

        # 下载压缩文件
        url = base_url + gz_name
        print(f"[正在下载] {url}...")
        urllib.request.urlretrieve(url, gz_path)

        # 解压
        print(f"[正在解压] {gz_name}...")
        with gzip.open(gz_path, 'rb') as f_in:
            with open(file_path, 'wb') as f_out:
                f_out.write(f_in.read())

        # 删除压缩包
        os.remove(gz_path)
        print(f"[完成] {file_name}")

    print("所有 MNIST 文件准备完毕！")


def load_mnist(data_dir="./mnist_data"):
    """
    加载 MNIST 数据集（如果文件不存在则自动下载）

    返回:
        (X_train, y_train), (X_test, y_test)
    """
    print("=" * 50)
    print("准备 MNIST 数据集")
    print("=" * 50)

    # 自动下载
    download_mnist(data_dir)

    # 加载训练集
    print("\n加载训练集...")
    X_train = load_mnist_images(f"{data_dir}/train-images-idx3-ubyte")
    y_train = load_mnist_labels(f"{data_dir}/train-labels-idx1-ubyte")
    print(f"  训练数据形状: {X_train.shape}, 标签形状: {y_train.shape}")

    # 加载测试集
    print("\n加载测试集...")
    X_test = load_mnist_images(f"{data_dir}/t10k-images-idx3-ubyte")
    y_test = load_mnist_labels(f"{data_dir}/t10k-labels-idx1-ubyte")
    print(f"  测试数据形状: {X_test.shape}, 标签形状: {y_test.shape}")

    return (X_train, y_train), (X_test, y_test)


# ================================================================
# 主程序：训练手写数字识别
# ================================================================

if __name__ == "__main__":
    # -------- 设置随机种子（保证结果可复现）--------
    np.random.seed(42)

    # -------- 加载 MNIST 数据 --------
    (X_train, y_train), (X_test, y_test) = load_mnist()

    # 从训练集中划分一部分作为验证集（用于监控训练过程中的泛化能力）
    val_size = 5000
    X_val = X_train[:, :val_size]
    y_val = y_train[:, :val_size]
    X_train = X_train[:, val_size:]
    y_train = y_train[:, val_size:]

    print(f"\n数据划分:")
    print(f"  训练集: {X_train.shape[1]} 张")
    print(f"  验证集: {X_val.shape[1]} 张")
    print(f"  测试集: {X_test.shape[1]} 张")

    # -------- 展示一些训练样本 --------
    plt.figure(figsize=(10, 4))
    for i in range(10):
        plt.subplot(2, 5, i + 1)
        idx = np.random.randint(X_train.shape[1])
        img = X_train[:, idx].reshape(28, 28)
        label = np.argmax(y_train[:, idx])
        plt.imshow(img, cmap='gray')
        plt.title(f"数字: {label}")
        plt.axis('off')
    plt.suptitle("MNIST 训练样本预览")
    plt.tight_layout()
    plt.show()

    # -------- 创建并训练网络 --------
    model = MNISTClassifier(
        input_size=784,
        hidden1_size=128,
        hidden2_size=64,
        output_size=10
    )

    print("\n" + "=" * 50)
    print("训练开始")
    print("=" * 50)

    model.train(
        X_train, y_train,
        X_val=X_val, y_val=y_val,
        epochs=30,          # 遍历整个训练集 30 次
        batch_size=64,      # 每次用 64 个样本更新参数
        learning_rate=0.1   # 学习率
    )

    # -------- 在测试集上评估 --------
    test_accuracy = model.compute_accuracy(X_test, y_test)
    print(f"\n{'=' * 50}")
    print(f"测试集准确率: {test_accuracy:.4f} ({test_accuracy * 100:.2f}%)")
    print(f"{'=' * 50}")

    # -------- 画训练曲线 --------
    plt.figure(figsize=(12, 4))

    plt.subplot(1, 2, 1)
    plt.plot(model.loss_history)
    plt.title("训练损失曲线")
    plt.xlabel("Epoch")
    plt.ylabel("交叉熵损失")
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(model.accuracy_history)
    plt.title("训练准确率曲线")
    plt.xlabel("Epoch")
    plt.ylabel("准确率")
    plt.grid(True)

    plt.tight_layout()
    plt.show()

    # -------- 展示预测结果 --------
    print("\n随机展示测试集预测结果...")
    model.show_predictions(X_test, y_test, num_samples=10)

    

