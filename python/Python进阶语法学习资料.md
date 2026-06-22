# Python 进阶语法学习资料

> 适合有一定 Python 基础，想深入学习面向对象编程、装饰器、迭代器、上下文管理器等进阶内容的读者。

---

## 一、面向对象编程（OOP）

### 1. 类与对象

```python
# 定义一个类：类就像一张蓝图，对象是根据蓝图造出来的具体实例
class Dog:
    """狗类——类的文档字符串"""

    # 类属性：所有实例共享，相当于所有狗的共性
    species = "Canis familiaris"

    # 构造方法：创建对象时自动调用，用来初始化实例属性
    def __init__(self, name, age):
        self.name = name    # 实例属性，每条狗有自己的名字
        self.age = age      # 实例属性，每条狗有自己的年龄

    # 实例方法：必须通过实例调用，第一个参数 self 指向实例本身
    def bark(self):
        """狗叫的方法"""
        return f"{self.name} says 汪汪!"

    # 另一个实例方法
    def description(self):
        """返回狗的描述信息"""
        return f"{self.name} 今年 {self.age} 岁"


# 创建对象（实例化）
dog1 = Dog("旺财", 3)
dog2 = Dog("小白", 2)

# 调用实例方法
print(dog1.bark())           # 输出: 旺财 says 汪汪!
print(dog2.description())    # 输出: 小白 今年 2 岁

# 访问属性
print(dog1.name)             # 输出: 旺财
print(dog1.species)          # 输出: Canis familiaris（类属性）
```

### 2. 继承 —— 子类继承父类的属性和方法

```python
# 父类（基类）
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        """父类的默认实现，子类可以覆盖"""
        raise NotImplementedError("子类必须实现 speak 方法")


# 子类（派生类）
class Cat(Animal):          # 继承 Animal
    def speak(self):
        """重写父类的 speak 方法"""
        return f"{self.name} 说: 喵喵~"


class Duck(Animal):
    def speak(self):
        return f"{self.name} 说: 嘎嘎!"


# 多态：同样的接口，不同的行为
animals = [Cat("咪咪"), Duck("唐老鸭")]
for animal in animals:
    print(animal.speak())
# 输出:
# 咪咪 说: 喵喵~
# 唐老鸭 说: 嘎嘎!
```

### 3. super() —— 调用父类的方法

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age


class Student(Person):
    def __init__(self, name, age, student_id):
        # super() 调用父类的 __init__，避免重复代码
        super().__init__(name, age)
        self.student_id = student_id  # 子类独有的属性

    def info(self):
        return f"学生: {self.name}, 年龄: {self.age}, 学号: {self.student_id}"


s = Student("小明", 18, "2024001")
print(s.info())  # 输出: 学生: 小明, 年龄: 18, 学号: 2024001
```

### 4. 私有属性与 @property

```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        # 前导双下划线表示"私有"属性，外部不能直接访问
        self.__balance = balance

    # @property 把方法变成属性来用，外部可以像访问属性一样读取
    @property
    def balance(self):
        """只读属性——外部不能直接修改余额"""
        return self.__balance

    # setter —— 让属性可以被"受控地"修改
    @balance.setter
    def balance(self, amount):
        if amount < 0:
            raise ValueError("余额不能为负数！")
        self.__balance = amount

    def deposit(self, amount):
        """存款"""
        if amount <= 0:
            raise ValueError("存款金额必须为正数")
        self.__balance += amount

    def withdraw(self, amount):
        """取款"""
        if amount > self.__balance:
            raise ValueError("余额不足！")
        self.__balance -= amount


acc = BankAccount("张三", 1000)
print(acc.balance)       # 读取余额，相当于调用 balance() 方法 → 1000

acc.deposit(500)
print(acc.balance)       # 1500

# acc.__balance = 0      # ❌ 错误，不能直接访问私有属性
acc.balance = 2000       # ✅ 通过 setter 修改
print(acc.balance)       # 2000
```

### 5. 类方法 @classmethod 与 静态方法 @staticmethod

```python
class Date:
    """日期工具类"""
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    # 实例方法——必须通过实例调用
    def format(self):
        return f"{self.year}-{self.month:02d}-{self.day:02d}"

    # 类方法——通过类直接调用，第一个参数 cls 指向类本身
    @classmethod
    def from_string(cls, date_str):
        """从字符串 '2024-01-15' 创建 Date 对象"""
        year, month, day = map(int, date_str.split("-"))
        return cls(year, month, day)  # 调用 __init__

    # 静态方法——像是"寄居"在类里的普通函数，与类和实例无关
    @staticmethod
    def is_valid_year(year):
        """判断年份是否合法"""
        return 1900 <= year <= 2100


# 使用类方法创建对象
d = Date.from_string("2024-01-15")
print(d.format())           # 输出: 2024-01-15

# 使用静态方法
print(Date.is_valid_year(2024))   # True
print(Date.is_valid_year(1800))   # False
```

### 6. 特殊方法（魔术方法 / dunder methods）

```python
class Vector:
    """二维向量，演示常见的魔术方法"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    # __str__：给用户看的，print() 时调用
    def __str__(self):
        return f"Vector({self.x}, {self.y})"

    # __repr__：给开发者看的，调试时使用
    def __repr__(self):
        return f"Vector({self.x!r}, {self.y!r})"

    # __add__：定义 + 运算符的行为
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    # __sub__：定义 - 运算符的行为
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    # __mul__：定义 * 运算符的行为（向量乘以标量）
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    # __eq__：定义 == 运算符
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    # __len__：len() 时调用
    def __len__(self):
        """向量的长度（从原点到该点的曼哈顿距离）"""
        return abs(self.x) + abs(self.y)

    # __getitem__：支持索引访问，如 v[0]
    def __getitem__(self, index):
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        raise IndexError("向量索引超出范围")


v1 = Vector(1, 2)
v2 = Vector(3, 4)

print(v1)                     # Vector(1, 2)
print(v1 + v2)                # Vector(4, 6)
print(v1 * 3)                 # Vector(3, 6)
print(v1 == Vector(1, 2))     # True
print(len(v1))                # 3（1 + 2 的曼哈顿距离）
print(v1[0])                  # 1
```

---

## 二、装饰器（Decorator）

装饰器本质上是一个函数，它接收一个函数作为参数，返回一个新的函数，在不修改原函数代码的前提下扩展其功能。

### 1. 最简单的装饰器

```python
# 装饰器函数：接收一个函数，返回一个增强版的新函数
def say_hello(func):
    def wrapper():
        print("=== 函数执行前 ===")
        func()                # 调用原始函数
        print("=== 函数执行后 ===")
    return wrapper


# 使用 @ 语法糖来应用装饰器
@say_hello
def greet():
    print("你好！")


greet()
# 输出:
# === 函数执行前 ===
# 你好！
# === 函数执行后 ===
```

### 2. 装饰带参数的函数

```python
def log_call(func):
    """打印函数调用日志的装饰器"""
    def wrapper(*args, **kwargs):
        # *args 接受所有位置参数，**kwargs 接受所有关键字参数
        print(f"[日志] 调用函数: {func.__name__}")
        print(f"[日志] 位置参数: {args}")
        print(f"[日志] 关键字参数: {kwargs}")
        result = func(*args, **kwargs)  # 调用原函数
        print(f"[日志] 返回结果: {result}")
        return result
    return wrapper


@log_call
def add(a, b):
    """两数相加"""
    return a + b


add(3, 5)
# 输出:
# [日志] 调用函数: add
# [日志] 位置参数: (3, 5)
# [日志] 关键字参数: {}
# [日志] 返回结果: 8
```

### 3. 保留原函数信息的装饰器（@functools.wraps）

```python
import functools

def timer(func):
    """计算函数执行时间的装饰器"""
    @functools.wraps(func)  # 保留原函数的 __name__、__doc__ 等信息
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} 执行耗时: {end - start:.4f} 秒")
        return result
    return wrapper


@timer
def slow_sum(n):
    """计算 1 累加到 n 的和"""
    total = 0
    for i in range(n):
        total += i
    return total


print(slow_sum(1000000))
print(slow_sum.__name__)  # 不加 @functools.wraps 会输出 "wrapper"
print(slow_sum.__doc__)   # 不加 @functools.wraps 会输出 None
```

### 4. 带参数的装饰器（装饰器工厂）

```python
import functools

def repeat(times):
    """装饰器工厂：控制函数重复执行的次数"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator


@repeat(times=3)   # 相当于 repeat(3)(say_hello)
def say_hello(name):
    print(f"你好, {name}!")


say_hello("小明")
# 输出:
# 你好, 小明!
# 你好, 小明!
# 你好, 小明!
```

### 5. 装饰器的实际应用场景

```python
import functools
import time

# ------ 场景一：权限校验 ------
def require_admin(func):
    """模拟管理员权限校验装饰器"""
    @functools.wraps(func)
    def wrapper(user, *args, **kwargs):
        if not user.get("is_admin"):
            raise PermissionError("只有管理员才能执行此操作！")
        return func(user, *args, **kwargs)
    return wrapper


@require_admin
def delete_user(user, target_id):
    print(f"删除用户 {target_id} 成功")


# ------ 场景二：缓存计算结果 ------
def cache(func):
    """缓存函数的返回值，避免重复计算"""
    memo = {}  # 字典作为缓存
    @functools.wraps(func)
    def wrapper(*args):
        if args in memo:
            print(f"[缓存命中] {args} → {memo[args]}")
            return memo[args]
        result = func(*args)
        memo[args] = result
        print(f"[计算并缓存] {args} → {result}")
        return result
    return wrapper


@cache
def fibonacci(n):
    """斐波那契数列（递归）"""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


# ------ 场景三：重试机制 ------
def retry(max_attempts=3, delay=0.5):
    """函数执行失败时自动重试"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"第 {attempt} 次尝试失败: {e}")
                    if attempt == max_attempts:
                        raise  # 最后一次失败，抛出异常
                    time.sleep(delay)
            return None
        return wrapper
    return decorator


@retry(max_attempts=3)
def unstable_network_request():
    """模拟不稳定的网络请求"""
    import random
    if random.random() < 0.7:  # 70% 概率失败
        raise ConnectionError("网络连接失败！")
    return "请求成功"
```

---

## 三、迭代器（Iterator）与生成器（Generator）

### 1. 迭代器协议

```python
# 迭代器必须实现 __iter__ 和 __next__ 两个方法
class CountDown:
    """倒计时迭代器：从 n 数到 0"""
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        """返回迭代器对象本身"""
        return self

    def __next__(self):
        """返回下一个值，没有值时抛出 StopIteration"""
        if self.current < 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value


# 使用迭代器
for num in CountDown(5):
    print(num, end=" ")   # 输出: 5 4 3 2 1 0
```

### 2. 生成器（yield）

```python
def count_down(n):
    """生成器版本：用 yield 实现，比手写迭代器类简单得多"""
    while n >= 0:
        yield n       # yield 会"暂停"函数，保存当前状态
        n -= 1


for num in count_down(5):
    print(num, end=" ")   # 输出: 5 4 3 2 1 0

# 生成器表达式——类似列表推导式，但节省内存
squares = (x * x for x in range(10))
print(list(squares))  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

### 3. 生成器的实际应用

```python
def read_large_file(file_path):
    """
    逐行读取大文件，一次只读一行，不会把整个文件加载到内存
    适用于处理 GB 级别的日志文件
    """
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            yield line.strip()


# 使用示例（假设有个大文件）
# for line in read_large_file("huge_log.txt"):
#     process(line)


def fibonacci_gen():
    """无限斐波那契数列生成器——需要多少算多少，不会浪费内存"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


# 只需要前 10 个斐波那契数
fib = fibonacci_gen()
first_10 = [next(fib) for _ in range(10)]
print(first_10)  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

---

## 四、上下文管理器（Context Manager）

### 1. with 语句与上下文管理器协议

```python
# 上下文管理器协议包含 __enter__ 和 __exit__ 两个方法
class ManagedFile:
    """自定义文件上下文管理器——自动处理文件的打开和关闭"""

    def __init__(self, filename, mode="r"):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        """进入 with 块时自动调用，返回值赋给 as 后面的变量"""
        print(f"打开文件: {self.filename}")
        self.file = open(self.filename, self.mode, encoding="utf-8")
        return self.file  # 这个会被赋给 as 后面的变量

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        离开 with 块时自动调用
        参数 exc_type, exc_val, exc_tb 用于处理异常
        返回 True 表示"吞掉"异常，False 或不返回表示让异常继续传播
        """
        self.file.close()
        print(f"关闭文件: {self.filename}")
        # 返回 False，异常会正常抛出
        return False


# 使用自定义上下文管理器
with ManagedFile("test.txt", "w") as f:
    f.write("Hello, World!")
# 输出:
# 打开文件: test.txt
# 关闭文件: test.txt
```

### 2. 用 @contextmanager 简化上下文管理器

```python
from contextlib import contextmanager


@contextmanager
def managed_file(filename, mode="r"):
    """用装饰器方式定义上下文管理器，更简洁"""
    print(f"打开文件: {filename}")
    f = open(filename, mode, encoding="utf-8")
    try:
        yield f  # yield 前面的代码相当于 __enter__，yield 的值赋给 as 后面的变量
    finally:
        f.close()
        print(f"关闭文件: {filename}")


# 使用方式完全一样
with managed_file("test.txt", "w") as f:
    f.write("使用 @contextmanager 简化写法")
```

### 3. 上下文管理器的实际应用

```python
import time
from contextlib import contextmanager


@contextmanager
def timer(name="代码块"):
    """计时器：自动计算代码块的执行时间"""
    start = time.time()
    try:
        yield  # 执行 with 块里的代码
    finally:
        elapsed = time.time() - start
        print(f"[{name}] 执行耗时: {elapsed:.4f} 秒")


# 使用
with timer("数据处理"):
    total = sum(range(1_000_000))
    print(f"总和: {total}")


# --------------------------------------------


@contextmanager
def db_transaction(connection):
    """数据库事务：自动提交或回滚"""
    print("开始事务")
    try:
        yield connection  # 执行事务中的操作
        connection.commit()
        print("事务提交成功")
    except Exception as e:
        connection.rollback()
        print(f"事务回滚: {e}")
        raise
```

---

## 五、元类（Metaclass）—— 类的类

> 元类是创建类的类。类定义了对象的行为，而元类定义了类的行为。

```python
# type 是 Python 中的默认元类
# 使用 type 可以动态创建类

# 普通方式定义类
class Foo:
    bar = 42

# 等价于用 type 动态创建
Foo = type("Foo", (), {"bar": 42})

# type(name, bases, dict) 三个参数:
#   name:   类名
#   bases:  父类元组
#   dict:   类属性和方法


# 自定义元类——继承 type
class SingletonMeta(type):
    """
    单例模式元类：一个类只能创建一个实例
    所有使用 SingletonMeta 作为元类的类都会变成单例
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        # __call__ 在"调用类"（即创建实例）时被调用
        if cls not in cls._instances:
            # 如果还没有创建过实例，就创建一个
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


# 使用元类 —— 指定 metaclass
class Database(metaclass=SingletonMeta):
    """数据库连接类 —— 全局只需要一个连接实例"""

    def __init__(self):
        print("初始化数据库连接...")

    def query(self, sql):
        return f"执行查询: {sql}"


# 测试单例 —— 两次创建得到的是同一个对象
db1 = Database()   # 只打印一次 "初始化数据库连接..."
db2 = Database()

print(db1 is db2)  # True —— 确实是同一个对象
print(db1.query("SELECT 1"))  # 执行查询: SELECT 1
```

---

## 六、描述符（Descriptor）

描述符是一个类，实现了 `__get__`、`__set__`、`__delete__` 中的至少一个方法，用来"托管"另一个类的属性访问。

```python
class PositiveNumber:
    """描述符：确保属性值是正数"""

    def __set_name__(self, owner, name):
        # Python 3.6+ 自动调用，记录属性名
        self._name = name

    def __get__(self, instance, owner):
        """获取属性值时自动调用"""
        if instance is None:
            return self  # 通过类访问时返回描述符本身
        return instance.__dict__.get(self._name, 0)

    def __set__(self, instance, value):
        """设置属性值时自动调用——可以做校验"""
        if value <= 0:
            raise ValueError(f"{self._name} 必须为正数，收到: {value}")
        instance.__dict__[self._name] = value


class Product:
    """商品类——使用描述符来保证价格和库存为正数"""
    price = PositiveNumber()
    stock = PositiveNumber()

    def __init__(self, name, price, stock):
        self.name = name
        self.price = price      # 走描述符的 __set__
        self.stock = stock      # 走描述符的 __set__


p = Product("手机", 2999, 100)
print(p.price)    # 2999（走描述符的 __get__）
print(p.stock)    # 100

try:
    p.price = -100  # ❌ 触发描述符的校验，抛出 ValueError
except ValueError as e:
    print(e)        # price 必须为正数，收到: -100
```

---

## 七、抽象基类（ABC）

```python
from abc import ABC, abstractmethod


class Shape(ABC):
    """抽象基类——不能被实例化，只能被继承"""

    @abstractmethod
    def area(self):
        """抽象方法——子类必须实现"""
        pass

    @abstractmethod
    def perimeter(self):
        """抽象方法——子类必须实现"""
        pass

    def describe(self):
        """普通方法——子类可以直接继承使用"""
        return f"面积: {self.area()}, 周长: {self.perimeter()}"


class Circle(Shape):
    """圆形——必须实现 Shape 的所有抽象方法"""
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius * self.radius

    def perimeter(self):
        return 2 * 3.14159 * self.radius


class Rectangle(Shape):
    """矩形"""
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


# s = Shape()          # ❌ 错误：不能实例化抽象类
c = Circle(5)
r = Rectangle(4, 6)

print(c.describe())   # 面积: 78.53975, 周长: 31.4159
print(r.describe())   # 面积: 24, 周长: 20
```

---

## 八、Type Hints（类型注解）

```python
from typing import List, Dict, Optional, Union, Callable, Tuple


# 基础类型的注解
name: str = "小明"
age: int = 18
height: float = 1.75
is_student: bool = True


# 容器类型的注解
def process_items(items: List[str]) -> None:
    """处理字符串列表，不返回任何内容"""
    for item in items:
        print(item)


def get_scores() -> Dict[str, int]:
    """返回一个字典：名字 → 分数"""
    return {"语文": 90, "数学": 95, "英语": 88}


# Optional 表示"要么是指定类型，要么是 None"
def find_user(user_id: int) -> Optional[str]:
    """根据 ID 查找用户，找不到返回 None"""
    users = {1: "张三", 2: "李四"}
    return users.get(user_id)  # 可能返回 str 或 None


# Union 表示"可以是多种类型之一"
def double(value: Union[int, float]) -> Union[int, float]:
    """输入整数或浮点数，返回对应翻倍的结果"""
    return value * 2


# Callable 表示"可调用对象（函数）"
def apply_func(
    func: Callable[[int, int], int],
    a: int,
    b: int
) -> int:
    """接收一个函数和两个整数，返回函数调用的结果"""
    return func(a, b)


print(apply_func(lambda x, y: x + y, 3, 5))  # 8


# Type Alias（类型别名）
Vector2D = Tuple[float, float]

def add_vectors(v1: Vector2D, v2: Vector2D) -> Vector2D:
    """两个二维向量相加"""
    return (v1[0] + v2[0], v1[1] + v2[1])
```

---

## 九、混入类（Mixin）

Mixin 是一种设计模式，通过多重继承给类添加额外的功能。

```python
class JSONMixin:
    """Mixin：给类添加 JSON 序列化功能"""

    def to_json(self) -> str:
        """将对象转为 JSON 字符串"""
        import json
        # 收集所有非私有、非方法的属性
        data = {}
        for key, value in self.__dict__.items():
            if not key.startswith("_"):
                data[key] = value
        return json.dumps(data, ensure_ascii=False, indent=2)


class LogMixin:
    """Mixin：给类添加日志功能"""

    def log(self, message: str):
        """打印带时间戳的日志"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{self.__class__.__name__}] {message}")


# 同时使用多个 Mixin
class User(JSONMixin, LogMixin):
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age


user = User("小红", 20)
print(user.to_json())
# {
#   "name": "小红",
#   "age": 20
# }
user.log("用户已创建")  # [2024-01-15 10:30:00] [User] 用户已创建
```

---

## 十、枚举类

```python
from enum import Enum, auto, unique


# 普通枚举
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


print(Color.RED)              # Color.RED
print(Color.RED.name)         # "RED"
print(Color.RED.value)        # 1
print(repr(Color.RED))        # <Color.RED: 1>


# auto() 自动分配值
class Status(Enum):
    PENDING = auto()    # 1
    PROCESSING = auto() # 2
    COMPLETED = auto()  # 3
    FAILED = auto()     # 4


# @unique 装饰器确保没有重复值
@unique
class Direction(Enum):
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"
    # NORTH = "N"  # ❌ 如果取消注释，会报 ValueError: duplicate values


# 枚举的实用方法
def get_status_message(status: Status) -> str:
    """根据状态返回对应的消息"""
    messages = {
        Status.PENDING: "等待处理",
        Status.PROCESSING: "正在处理中",
        Status.COMPLETED: "已完成",
        Status.FAILED: "处理失败",
    }
    return messages[status]


print(get_status_message(Status.PENDING))   # 等待处理
```

---

## 十一、数据类（dataclass）

```python
from dataclasses import dataclass, field, asdict


# @dataclass 自动生成 __init__、__repr__、__eq__ 等方法
@dataclass
class Point:
    """二维点"""
    x: float = 0.0
    y: float = 0.0


@dataclass
class Student:
    """学生数据类"""
    name: str
    age: int
    scores: List[int] = field(default_factory=list)
    # field(default_factory=list) 确保每个实例有自己的列表
    is_active: bool = True

    # 可以像普通类一样定义方法
    def average_score(self) -> float:
        if not self.scores:
            return 0.0
        return sum(self.scores) / len(self.scores)


# 使用数据类
p1 = Point(1.0, 2.0)
p2 = Point(1.0, 2.0)
print(p1)                    # Point(x=1.0, y=2.0)
print(p1 == p2)              # True（自动生成了 __eq__）

s = Student("小明", 18, [90, 85, 92])
print(s)                     # Student(name='小明', age=18, scores=[90, 85, 92], is_active=True)
print(s.average_score())     # 89.0

# 转为字典
print(asdict(s))
# {'name': '小明', 'age': 18, 'scores': [90, 85, 92], 'is_active': True}
```

---

## 十二、更多实用技巧

### 1. 命名元组（namedtuple）

```python
from collections import namedtuple

# namedtuple 创建轻量级"类"——像元组一样不可变，但可以通过属性名访问
Car = namedtuple("Car", ["brand", "model", "year"])

my_car = Car("Toyota", "Camry", 2024)
print(my_car.brand)    # Toyota
print(my_car.year)     # 2024
brand, model, year = my_car  # 可以解包
```

### 2. 函数注解与 __annotations__

```python
def greet(name: str, age: int = 18) -> str:
    return f"{name} 今年 {age} 岁"

print(greet.__annotations__)
# {'name': <class 'str'>, 'age': <class 'int'>, 'return': <class 'str'>}
```

### 3. 使用 __slots__ 节省内存

```python
class PointWithSlots:
    """__slots__ 告诉 Python 只允许这些属性，省掉 __dict__，内存更小"""
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x = x
        self.y = y

    # 优点：每个实例节省约 50% 内存
    # 缺点：不能动态添加属性
    # p.z = 3  # ❌ AttributeError


# 内存对比
p1 = PointWithSlots(1, 2)
print(p1.x, p1.y)  # 1 2
# p1.z = 3  # 报错
```

---

## 总结

| 知识点 | 用途 | 关键语法 |
|--------|------|---------|
| 类与对象 | 组织代码，封装数据和行为 | `class`, `self`, `__init__` |
| 继承 | 代码复用 | `class A(B)`, `super()` |
| 装饰器 | 在不修改原函数的前提下扩展功能 | `@decorator` |
| 生成器 | 惰性求值，节省内存 | `yield` |
| 上下文管理器 | 自动管理资源（文件、锁、数据库连接） | `with`, `__enter__/__exit__` |
| 元类 | 控制类的创建 | `metaclass=...`, `__new__` |
| 描述符 | 托管属性访问 | `__get__/__set__` |
| ABC | 定义接口规范 | `@abstractmethod` |
| dataclass | 简化数据类编写 | `@dataclass` |

> 学习建议：不要试图一次性掌握所有内容。先理解**类与对象**和**装饰器**这两个最常用的概念，然后逐步学习生成器、上下文管理器、描述符等。动手写代码是最好的学习方法！
