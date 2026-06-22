# Python 排序算法学习资料

> 排序是计算机科学中最基础也是最重要的算法之一。掌握各种排序算法的思想、实现和适用场景，是每个程序员的必修课。

---

## 目录

1. [冒泡排序（Bubble Sort）](#1-冒泡排序bubble-sort)
2. [选择排序（Selection Sort）](#2-选择排序selection-sort)
3. [插入排序（Insertion Sort）](#3-插入排序insertion-sort)
4. [归并排序（Merge Sort）](#4-归并排序merge-sort)
5. [快速排序（Quick Sort）](#5-快速排序quick-sort)
6. [堆排序（Heap Sort）](#6-堆排序heap-sort)
7. [计数排序（Counting Sort）](#7-计数排序counting-sort)
8. [Python 内置排序（Timsort）](#8-python-内置排序timsort)
9. [总结与对比](#9-总结与对比)

---

## 1. 冒泡排序（Bubble Sort）

### 思路引导

冒泡排序的核心思想非常直观：**每一轮遍历都从头到尾比较相邻元素，如果顺序不对就交换，让大的元素像气泡一样慢慢"浮"到末尾**。

你可以这样思考：
- 第 1 轮：遍历整个数组，把最大的元素交换到最后一个位置
- 第 2 轮：遍历前 n-1 个元素，把第二大的元素交换到倒数第二个位置
- 以此类推，每轮确定一个元素的最终位置

**如何优化？** 如果在某一轮遍历中没有发生任何交换，说明数组已经有序，可以提前结束。

### 代码实现

```python
def bubble_sort(arr):
    """
    冒泡排序
    时间复杂度: O(n²)  空间复杂度: O(1)
    稳定排序
    """
    n = len(arr)
    # 外层循环控制轮数，每轮确定一个最大元素
    for i in range(n - 1):
        # 优化标志：如果本轮没有交换，说明已经有序
        swapped = False
        # 内层循环进行相邻比较，范围逐渐缩小
        # 因为后 i 个元素已经排好，不需要再比较
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        # 如果没有发生交换，提前结束
        if not swapped:
            break
    return arr
```

---

## 2. 选择排序（Selection Sort）

### 思路引导

选择排序的想法很直接：**每次从未排序的部分中找出最小的元素，放到已排序部分的末尾**。

你可以这样思考：
- 第 1 轮：扫描整个数组，找到最小的元素，与第一个元素交换
- 第 2 轮：扫描从第二个元素开始的子数组，找到最小的，与第二个元素交换
- 如此重复，直到所有元素排好

> 与冒泡排序的区别：冒泡排序是**相邻交换**，选择排序是**全局找最小然后交换一次**。选择排序的交换次数少，但比较次数一样多。

### 代码实现

```python
def selection_sort(arr):
    """
    选择排序
    时间复杂度: O(n²)  空间复杂度: O(1)
    不稳定排序（例如 [5, 5, 3] 中第一个5会被换到后面）
    """
    n = len(arr)
    # i 表示已排序部分的末尾位置
    for i in range(n - 1):
        # 假设当前位置 i 的元素就是最小值
        min_idx = i
        # 在未排序部分寻找真正的最小值
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        # 把找到的最小值放到已排序部分的末尾
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr
```

---

## 3. 插入排序（Insertion Sort）

### 思路引导

插入排序的灵感来自**整理扑克牌**：每次从牌堆中摸一张牌，插入到手中已经排好序的牌的正确位置。

你可以这样思考：
- 从第二个元素开始，把它当作"待插入"的牌
- 在已排序部分从右向左扫描，找到合适的位置插入
- 比待插入元素大的元素都向右移动一位，腾出空间

**特点**：对于**基本有序**的小规模数据，插入排序非常高效（接近 O(n)）。

### 代码实现

```python
def insertion_sort(arr):
    """
    插入排序
    时间复杂度: O(n²)  空间复杂度: O(1)
    稳定排序
    最佳情况（已有序）: O(n)
    """
    n = len(arr)
    # 从第二个元素开始，第一个元素视为已排序
    for i in range(1, n):
        # 当前要插入的元素
        key = arr[i]
        # j 指向已排序部分的最后一个元素
        j = i - 1
        # 从右向左扫描，将比 key 大的元素向右移动
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        # 将 key 插入到正确位置
        arr[j + 1] = key
    return arr
```

---

## 4. 归并排序（Merge Sort）

### 思路引导

归并排序是**分治思想**的经典体现：**将大问题分解为小问题，解决小问题后再合并结果**。

思考过程：
1. **分解**：将数组从中间分成两半，递归地对左右两半分别排序
2. **合并**：将两个有序的子数组合并成一个有序数组

合并两个有序数组的过程很像"拉链"：同时遍历两个数组，每次取较小的元素放入结果中。

**特点**：无论数据初始状态如何，时间复杂度始终是 O(n log n)，但需要 O(n) 的额外空间。

### 代码实现

```python
def merge_sort(arr):
    """
    归并排序
    时间复杂度: O(n log n)  空间复杂度: O(n)
    稳定排序
    """
    # 递归终止条件：只有一个元素时自然有序
    if len(arr) <= 1:
        return arr

    # 1. 分解：找到中点，分割数组
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])    # 左半部分排序
    right = merge_sort(arr[mid:])   # 右半部分排序

    # 2. 合并：将两个有序数组合并
    return merge(left, right)


def merge(left, right):
    """
    合并两个有序数组
    类似"拉链"的过程，依次比较两个数组的头部元素
    """
    result = []
    i = j = 0

    # 同时遍历两个数组，取较小的元素加入结果
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # 将剩余元素直接加入结果（两个数组最多只剩一个非空）
    result.extend(left[i:])
    result.extend(right[j:])

    return result
```

---

## 5. 快速排序（Quick Sort）

### 思路引导

快速排序也是**分治思想**的应用，但它的核心在于"**分**"的过程——**分区（partition）**：

1. 从数组中选一个**基准元素（pivot）**
2. 将比 pivot 小的元素放到左边，比 pivot 大的放到右边
3. 递归地对左右两个子数组进行同样的操作

**关键问题**：如何选 pivot？如何优雅地分区？
- 最常见的做法是选最后一个元素作为 pivot
- 用双指针法进行原地分区，不需要额外空间

### 代码实现

```python
def quick_sort(arr, low=0, high=None):
    """
    快速排序（原地排序版）
    平均时间复杂度: O(n log n)  最坏: O(n²)
    空间复杂度: O(log n)（递归栈）
    不稳定排序
    """
    if high is None:
        high = len(arr) - 1

    if low < high:
        # 分区操作，返回基准元素的最终位置
        pi = partition(arr, low, high)
        # 递归排序基准左右两边
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)

    return arr


def partition(arr, low, high):
    """
    分区函数：以 arr[high] 为基准，将小于它的放左边，大于它的放右边
    返回基准元素最终所在的索引
    """
    # 选最后一个元素为基准
    pivot = arr[high]
    # i 指向"小于基准的区域"的末尾
    i = low - 1

    # 遍历 [low, high-1]，将小于 pivot 的元素交换到左侧
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    # 将基准元素放到正确位置（i+1）
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
```

---

## 6. 堆排序（Heap Sort）

### 思路引导

堆排序利用**堆**这种数据结构来实现排序。堆是一棵完全二叉树，分为：
- **大顶堆**：每个节点的值 ≥ 左右子节点的值（用于升序排序）
- **小顶堆**：每个节点的值 ≤ 左右子节点的值（用于降序排序）

思路如下：
1. **建堆**：将无序数组构建成一个大顶堆
2. **排序**：每次将堆顶（最大值）与堆的最后一个元素交换，然后将剩余元素重新调整为大顶堆

> 如果你不熟悉树的结构，可以先把堆看作一个"能快速找到最大值"的容器。

### 代码实现

```python
def heap_sort(arr):
    """
    堆排序
    时间复杂度: O(n log n)  空间复杂度: O(1)
    不稳定排序
    """
    n = len(arr)

    # 1. 建堆：从最后一个非叶子节点开始，向前调整
    # 最后一个非叶子节点的索引为 n//2 - 1
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # 2. 排序：逐个将堆顶元素移到末尾
    for i in range(n - 1, 0, -1):
        # 将堆顶（最大值）与当前未排序部分的最后一个元素交换
        arr[0], arr[i] = arr[i], arr[0]
        # 重新调整剩余元素为大顶堆
        heapify(arr, i, 0)

    return arr


def heapify(arr, n, i):
    """
    将以 i 为根节点的子树调整为大顶堆
    n 表示当前堆的大小（元素个数）
    """
    largest = i          # 假设当前根节点是最大的
    left = 2 * i + 1     # 左子节点
    right = 2 * i + 2    # 右子节点

    # 如果左子节点存在且大于当前最大值，更新最大值
    if left < n and arr[left] > arr[largest]:
        largest = left
    # 如果右子节点存在且大于当前最大值，更新最大值
    if right < n and arr[right] > arr[largest]:
        largest = right

    # 如果最大值不是根节点，交换并继续向下调整
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)
```

---

## 7. 计数排序（Counting Sort）

### 思路引导

计数排序与前几种排序有本质不同：它不是通过比较元素大小来排序，而是**利用元素的值作为索引，统计每个值出现的次数**。

前提：**数据范围有限且已知**（例如考试成绩 0-100 分）。

思路：
1. 统计每个值出现的次数（计数数组）
2. 对计数数组进行前缀和，得到每个值的最终位置
3. 根据计数数组将原数组元素放到正确位置

**特点**：时间复杂度 O(n + k)，其中 k 是数据范围。当 k 远小于 n 时非常高效，但数据范围很大时不适合。

### 代码实现

```python
def counting_sort(arr):
    """
    计数排序
    时间复杂度: O(n + k)  空间复杂度: O(k)
    稳定排序
    k 为数据范围（最大值 - 最小值 + 1）
    """
    if not arr:
        return arr

    # 1. 确定数据范围
    min_val = min(arr)
    max_val = max(arr)
    k = max_val - min_val + 1    # 数据范围

    # 2. 统计每个元素出现的次数
    count = [0] * k
    for num in arr:
        count[num - min_val] += 1

    # 3. 对计数数组做前缀和
    # 前缀和后的 count[i] 表示 ≤ 当前值的元素个数（即最后一个该值的位置+1）
    for i in range(1, k):
        count[i] += count[i - 1]

    # 4. 从后往前遍历原数组，根据计数数组将元素放到正确位置
    # 从后往前遍历保证了稳定性
    result = [0] * len(arr)
    for num in reversed(arr):
        idx = count[num - min_val] - 1   # 该元素应放的位置
        result[idx] = num
        count[num - min_val] -= 1        # 相同元素的下一个位置前移

    return result
```

---

## 8. Python 内置排序（Timsort）

### 思路引导

Python 的 `sorted()` 和 `list.sort()` 使用的是一种叫做 **Timsort** 的混合排序算法。

Timsort 的核心思想：
- **结合了归并排序和插入排序的优点**
- 利用数据中可能存在的**有序片段（run）**
- 对于小规模数据使用插入排序（因为小规模时插入排序很快）
- 对于大规模数据使用归并排序（保证 O(n log n) 的性能）

> **给你的建议**：在实际开发中，**永远优先使用 Python 内置的排序**。它经过高度优化，比手写的排序算法快得多。

### 使用示例

```python
# 基本排序
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
sorted_nums = sorted(numbers)            # 返回新列表
numbers.sort()                           # 原地排序

# 逆序排序
sorted_nums = sorted(numbers, reverse=True)

# 自定义排序（通过 key 参数）
students = [
    {"name": "Alice", "score": 95},
    {"name": "Bob", "score": 87},
    {"name": "Charlie", "score": 92},
]
# 按分数从高到低排序
students.sort(key=lambda s: s["score"], reverse=True)

# 使用 operator 模块更优雅
from operator import itemgetter, attrgetter
students.sort(key=itemgetter("score"), reverse=True)

# 多级排序（先按分数降序，再按姓名升序）
students.sort(key=lambda s: (-s["score"], s["name"]))
```

---

## 9. 总结与对比

| 排序算法 | 平均时间复杂度 | 最坏时间复杂度 | 空间复杂度 | 稳定 | 特点 |
|---------|-------------|-------------|----------|------|------|
| 冒泡排序 | O(n²) | O(n²) | O(1) | ✅ | 简单但慢，适合教学 |
| 选择排序 | O(n²) | O(n²) | O(1) | ❌ | 交换次数少 |
| 插入排序 | O(n²) | O(n²) | O(1) | ✅ | 小规模数据很快 |
| 归并排序 | O(n log n) | O(n log n) | O(n) | ✅ | 稳定、性能稳定 |
| 快速排序 | O(n log n) | O(n²) | O(log n) | ❌ | 平均最快 |
| 堆排序 | O(n log n) | O(n log n) | O(1) | ❌ | 原地排序 |
| 计数排序 | O(n + k) | O(n + k) | O(k) | ✅ | 非比较排序，数据范围小 |
| Timsort | O(n log n) | O(n log n) | O(n) | ✅ | Python 内置，实际最快 |

### 如何选择合适的排序算法？

| 场景 | 推荐算法 |
|------|---------|
| **日常开发** | 直接用 `sorted()` 或 `list.sort()` |
| **数据几乎有序** | 插入排序 |
| **数据量极大** | 快速排序、归并排序 |
| **要求稳定性** | 归并排序、Timsort |
| **内存有限** | 堆排序、快速排序（原地） |
| **数据范围小** | 计数排序 |
| **面试/学习入门** | 冒泡排序 → 选择排序 → 插入排序 → 快速排序 |

---

> **学习建议**：先理解每种排序的**核心思想**，而不是死记代码。试着闭上眼睛，在脑海中模拟一次排序的全过程。当你能够用自己的话清晰地讲出每种排序算法的思路时，你就真正掌握了它。
