# C 语言零基础入门笔记

> 适合有 Python 基础的学习者，快速对比掌握 C 语言核心知识。

---

## 一、VSCode 配置 C 语言开发环境

### 1. 安装编译器（MinGW-w64）

C 是编译型语言，需要先安装编译器才能运行代码。

**Windows 推荐：MinGW-w64（GCC 的 Windows 版本）**

1. 下载地址：https://www.mingw-w64.org/ 或 https://github.com/niXman/mingw-builds-binaries/releases
2. 选择 `x86_64-12.2.0-release-win32-seh-ucrt.7z` 这类版本（64位 / UCRT 版）
3. 解压到 `C:\mingw64`
4. 将 `C:\mingw64\bin` 添加到系统环境变量 `PATH`

验证安装（打开 CMD 或 PowerShell）：

```bash
gcc --version
# 应输出 gcc (MinGW-W64) x.x.x 等信息
```

**macOS 推荐：Xcode Command Line Tools**

```bash
xcode-select --install
# 安装完成后
gcc --version
```

**Linux（Ubuntu/Debian）：**

```bash
sudo apt update && sudo apt install gcc gdb -y
gcc --version
```

### 2. 安装 VSCode 及插件

1. 下载 VSCode：https://code.visualstudio.com/
2. 安装后，在扩展商店（Ctrl+Shift+X）搜索并安装以下插件：
   - **C/C++**（Microsoft 官方，提供智能提示、调试、语法高亮）
   - **Code Runner**（可选，一键运行代码）

### 3. 配置 C/C++ 插件

按 `Ctrl+Shift+P` 打开命令面板，搜索 `C/C++: Edit Configurations (UI)`，在打开的界面中：

- **Compiler path**：选择你的 gcc 路径，例如 `C:\mingw64\bin\gcc.exe`
- **IntelliSense mode**：选择 `windows-gcc-x64`（Linux/macOS 会自动检测）

### 4. 运行 C 程序

**方法一：终端手动编译运行**

```bash
gcc hello.c -o hello    # 编译
./hello                  # 运行（Windows 下为 hello.exe）
```

常用编译选项：

| 选项 | 作用 |
|------|------|
| `-o <文件名>` | 指定输出文件名 |
| `-Wall` | 开启所有常见警告 |
| `-Wextra` | 开启额外警告 |
| `-g` | 生成调试信息（用于 GDB） |
| `-std=c11` | 指定 C 语言标准（如 C11、C17） |

示例：

```bash
gcc -Wall -Wextra -std=c11 hello.c -o hello
```

**方法二：Code Runner 插件**

安装后，在 `.c` 文件中点击右上角 ▶ 按钮或按 `Ctrl+Alt+N` 即可一键运行。

**方法三：VSCode 内置调试（GDB）**

1. 按 `Ctrl+Shift+D` 进入运行和调试
2. 点击 "创建 launch.json"，选择 "C++ (GDB/LLDB)"
3. 按 F5 即可断点调试

---

## 二、C 语言快速上手

### 1. 第一个程序

```c
#include <stdio.h>   // 导入标准输入输出库

int main() {         // 主函数，程序入口
    printf("Hello, World!\n");  // 打印输出
    return 0;        // 返回 0 表示正常结束
}
```

> **对比 Python：**
> - Python：`print("Hello, World!")`
> - C：需要 `#include <stdio.h>` + `printf()`，末尾要有分号 `;`

### 2. 注释

```c
// 这是单行注释（C99 标准起支持）

/*
   这是多行注释
   可以跨多行
*/

/// 这是文档注释（Doxygen 风格，可选）
```

> Python：`# 单行注释`，`"""多行注释"""`

### 3. 变量与数据类型

#### 基本数据类型

| 类型 | 关键字 | 占位符 | Python 对应 | 说明 |
|------|--------|--------|-------------|------|
| 整型 | `int` | `%d` | `int` | 通常 4 字节，范围 -2^31 ~ 2^31-1 |
| 字符 | `char` | `%c` | 无内置类型 | 1 字节，实际是整数（ASCII） |
| 浮点 | `float` | `%f` | `float` | 4 字节，精度约 7 位 |
| 双精度 | `double` | `%lf` | `float`（默认） | 8 字节，精度约 15 位 |
| 无值 | `void` | - | `None` | 无类型，用于函数返回值 |
| 短整型 | `short` | `%hd` | - | 通常 2 字节 |
| 长整型 | `long` | `%ld` | - | 通常 4 或 8 字节 |
| 无符号 | `unsigned int` | `%u` | - | 非负整数，范围扩大一倍 |

```c
#include <stdio.h>

int main() {
    int age = 25;
    float pi = 3.14f;        // float 常量需加 f 后缀
    double price = 99.99;
    char grade = 'A';        // 单引号表示字符
    unsigned int count = 100;

    printf("年龄：%d\n", age);
    printf("圆周率：%.2f\n", pi);     // .2 表示保留 2 位小数
    printf("价格：%.2lf\n", price);
    printf("等级：%c\n", grade);
    printf("计数值：%u\n", count);

    return 0;
}
```

#### 类型大小与范围

```c
#include <stdio.h>
#include <limits.h>   // 整型范围宏
#include <float.h>    // 浮点范围宏

int main() {
    printf("int 大小：%zu 字节\n", sizeof(int));
    printf("int 范围：%d ~ %d\n", INT_MIN, INT_MAX);
    printf("char 大小：%zu 字节\n", sizeof(char));
    printf("double 大小：%zu 字节\n", sizeof(double));
    return 0;
}
```

> Python 中变量无需声明类型，C 需要先声明后使用。

#### 常量

```c
#define PI 3.14159        // 宏常量，预处理阶段替换
const int MAX = 100;      // const 常量
```

### 3. 输入输出

```c
#include <stdio.h>

int main() {
    int num;
    char str[100];

    printf("请输入一个整数：");
    scanf("%d", &num);           // & 取地址符

    printf("请输入一个字符串：");
    scanf("%s", str);            // 字符串数组名本身就是地址，不需要 &

    printf("你输入了：%d 和 %s\n", num, str);
    return 0;
}
```

> **对比 Python：**
> - Python：`input()` 直接返回字符串
> - C：`scanf()` 需要指定格式，且传递变量的地址（`&`）
> - C 中字符串用字符数组表示，Python 有内置 `str` 类型

#### 读取一行字符串

```c
#include <stdio.h>

int main() {
    char line[100];
    printf("请输入一行文字：");
    fgets(line, sizeof(line), stdin);   // 安全读取一行
    printf("你输入的是：%s", line);
    return 0;
}
```

### 4. 格式化输出

```c
printf("%d\n", 42);          // 十进制整数
printf("%x\n", 255);         // 十六进制：ff
printf("%o\n", 8);           // 八进制：10
printf("%f\n", 3.14159);     // 浮点数
printf("%.2f\n", 3.14159);   // 保留两位小数：3.14
printf("%6d\n", 42);         // 右对齐，宽度 6
printf("%-6d\n", 42);        // 左对齐，宽度 6
printf("%s\n", "hello");     // 字符串
printf("%c\n", 'A');         // 字符
```

### 5. 运算符

#### 算术运算符

```c
int a = 10, b = 3;
printf("%d\n", a + b);   // 13
printf("%d\n", a - b);   // 7
printf("%d\n", a * b);   // 30
printf("%d\n", a / b);   // 3（整数除法，截断小数）
printf("%d\n", a % b);   // 1（取模/取余）
```

> Python 中 `/` 返回浮点数，`//` 才是整数除法。C 的 `/` 两边都是整数时执行整数除法。

#### 关系运算符

```c
int a = 5, b = 10;
printf("%d\n", a == b);  // 0（假，C 中 0 表示 false）
printf("%d\n", a != b);  // 1（真，非零表示 true）
printf("%d\n", a < b);   // 1
printf("%d\n", a > b);   // 0
```

> **关键区别：** C 没有 `bool` 类型（C99 起有 `_Bool`），用 `0` 表示假，**任何非零值**表示真。

#### 逻辑运算符

```c
int a = 1, b = 0;
printf("%d\n", a && b);   // 0（逻辑与：AND）
printf("%d\n", a || b);   // 1（逻辑或：OR）
printf("%d\n", !a);       // 0（逻辑非：NOT）
```

> Python 用 `and, or, not`，C 用 `&&, ||, !`。

#### 自增/自减

```c
int i = 0;
printf("%d\n", i++);   // 0（先取值，后自增）
printf("%d\n", ++i);   // 2（先自增，后取值）
printf("%d\n", i--);   // 2（先取值，后自减）
printf("%d\n", --i);   // 0（先自减，后取值）
```

#### 复合赋值运算符

```c
int x = 10;
x += 5;   // x = x + 5，等价于 x = 15
x -= 3;   // x = x - 3
x *= 2;   // x = x * 2
x /= 4;   // x = x / 4
x %= 3;   // x = x % 3
```

#### 条件/三元运算符

```c
int a = 10, b = 20;
int max = (a > b) ? a : b;   // 如果 a > b 则取 a，否则取 b
printf("较大值：%d\n", max);  // 20
```

> Python：`max = a if a > b else b`

#### sizeof 运算符

```c
printf("%zu\n", sizeof(int));    // 4
printf("%zu\n", sizeof(double)); // 8
printf("%zu\n", sizeof(char));   // 1
```

---

## 三、控制流

### 1. if / else if / else

```c
#include <stdio.h>

int main() {
    int score = 85;

    if (score >= 90) {
        printf("优秀\n");
    } else if (score >= 80) {
        printf("良好\n");
    } else if (score >= 60) {
        printf("及格\n");
    } else {
        printf("不及格\n");
    }
    return 0;
}
```

> 和 Python 几乎一样，只是 C 需要 `()` 和 `{}`：
> - Python：`if score >= 90:`
> - C：`if (score >= 90) {`

### 2. switch

```c
#include <stdio.h>

int main() {
    int day = 3;

    switch (day) {
        case 1:
            printf("周一\n");
            break;            // 必须 break，否则会"穿透"
        case 2:
            printf("周二\n");
            break;
        case 3:
            printf("周三\n");
            break;
        case 4:
            printf("周四\n");
            break;
        case 5:
            printf("周五\n");
            break;
        default:
            printf("周末\n");
    }
    return 0;
}
```

> - `switch` 只能判断整型或字符型，不能判断浮点或字符串
> - 每个 `case` 末尾必须有 `break`，否则继续执行下一个 case（"穿透"）
> - Python 没有内置的 switch（3.10+ 有 `match` 语句）

### 3. while 循环

```c
#include <stdio.h>

int main() {
    int i = 0;
    while (i < 5) {
        printf("i = %d\n", i);
        i++;
    }
    return 0;
}
// 输出：0 1 2 3 4
```

> 和 Python 类似，只是 C 用 `()` 和 `{}`：
> - Python：`while i < 5:`
> - C：`while (i < 5) {`

### 4. for 循环

```c
#include <stdio.h>

int main() {
    for (int i = 0; i < 5; i++) {
        printf("i = %d\n", i);
    }
    return 0;
}
// 输出：0 1 2 3 4
```

> **对比 Python：**
> - Python：`for i in range(5):`
> - C：`for (int i = 0; i < 5; i++)`
>
> C 的 `for` 更底层，需手动控制三个部分：
> - 初始化：`int i = 0;`
> - 条件判断：`i < 5;`
> - 步进操作：`i++`

`for` 循环的每个部分都可以省略，但分号不能少：

```c
int i = 0;
for (; i < 5; ) {    // 省略初始化和步进
    printf("%d\n", i);
    i++;
}

for (;;) {           // 无限循环（相当于 while(1)）
    // ...
}
```

### 5. do-while 循环

```c
#include <stdio.h>

int main() {
    int i = 0;
    do {
        printf("至少执行一次：%d\n", i);
        i++;
    } while (i < 3);
    return 0;
}
```

> `do-while` 至少执行一次循环体，`while` 可能一次都不执行。

### 6. break 和 continue

```c
for (int i = 0; i < 10; i++) {
    if (i == 3) {
        continue;   // 跳过本次循环，继续下一次
    }
    if (i == 7) {
        break;      // 跳出整个循环
    }
    printf("%d ", i);
}
// 输出：0 1 2 4 5 6
```

> 和 Python 的 `break`、`continue` 行为完全一致。

### 7. goto（不推荐但存在）

```c
#include <stdio.h>

int main() {
    int i = 0;
    loop:               // 标签
        printf("%d ", i);
        i++;
        if (i < 5)
            goto loop;  // 跳转到标签
    return 0;
}
// 输出：0 1 2 3 4
```

> 新手不推荐使用 `goto`，它会破坏程序结构。但在某些场景（如多层循环的深层错误处理）中仍有合理用途。

---

## 四、数组

### 1. 一维数组

```c
#include <stdio.h>

int main() {
    // 声明并初始化
    int arr[5] = {10, 20, 30, 40, 50};

    // 部分初始化（未指定的元素自动为 0）
    int arr2[5] = {1, 2};   // {1, 2, 0, 0, 0}

    // 自动推断大小
    int arr3[] = {1, 2, 3, 4, 5};  // 自动确定大小为 5

    // 访问元素
    printf("arr[0] = %d\n", arr[0]);  // 10
    printf("arr[2] = %d\n", arr[2]);  // 30

    // 修改元素
    arr[0] = 100;

    // 遍历
    for (int i = 0; i < 5; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");

    return 0;
}
```

> **对比 Python：**
> - `int arr[5]` 分配固定大小 5，不能动态增减
> - Python 的 `list` 可以动态伸缩，C 数组是固定大小的
> - C 数组越界**不报错**，这是常见 bug 来源

### 2. 二维数组

```c
int matrix[3][4] = {
    {1, 2, 3, 4},
    {5, 6, 7, 8},
    {9, 10, 11, 12}
};

// 遍历二维数组
for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 4; j++) {
        printf("%3d ", matrix[i][j]);
    }
    printf("\n");
}
```

### 3. 数组作为函数参数

> 数组传递给函数时会**退化为指针**，丢失长度信息，所以通常需要额外传入长度：

```c
#include <stdio.h>

void printArray(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

int main() {
    int nums[] = {10, 20, 30, 40, 50};
    int size = sizeof(nums) / sizeof(nums[0]);  // 计算数组长度
    printArray(nums, size);
    return 0;
}
```

---

## 五、字符串

C 语言没有独立的字符串类型，用字符数组表示，以 `\0`（空字符）结尾。

```c
#include <stdio.h>
#include <string.h>  // 字符串函数库

int main() {
    // 方式一：字符数组（可修改）
    char s1[] = "Hello";     // 自动在末尾加 '\0'
    // 实际上占据 6 个字节：'H' 'e' 'l' 'l' 'o' '\0'

    // 方式二：指针常量（不可修改）
    char *s2 = "World";

    // 方式三：指定大小
    char s3[10] = "Hi";      // 未使用的元素填 '\0'

    // 字符串长度
    printf("len = %zu\n", strlen(s1));  // 5（不含 \0）

    // 字符串复制
    char dst[20];
    strcpy(dst, s1);         // 复制字符串

    // 字符串拼接
    char s4[20] = "Hello ";
    strcat(s4, "World!");    // 拼接
    printf("%s\n", s4);      // Hello World!

    // 字符串比较
    if (strcmp(s1, "Hello") == 0) {    // 相等返回 0
        printf("相等\n");
    }

    return 0;
}
```

### 常用字符串函数

| 函数 | 功能 | 用法 |
|------|------|------|
| `strlen(s)` | 返回字符串长度（不含 `\0`） | `strlen("hello")` → 5 |
| `strcpy(dst, src)` | 复制字符串 | `strcpy(s1, s2)` |
| `strcat(dst, src)` | 拼接字符串 | `strcat(s1, s2)` |
| `strcmp(s1, s2)` | 比较字符串（相等返回 0） | `strcmp(a, b) == 0` |
| `strncpy(dst, src, n)` | 安全复制，最多 n 个字符 | `strncpy(s1, s2, 9)` |
| `sprintf(buf, fmt, ...)` | 格式化到字符串 | `sprintf(s, "%d", num)` |

> **对比 Python：**
> - Python：`len("hello")`、`"a" + "b"`、`s[::-1]`
> - C 没有 `+` 运算符拼接字符串，要用 `strcat()`，且目标数组要足够大
> - C 字符串是可变字符数组，Python 字符串不可变

---

## 六、指针（C 语言核心难点）

指针是 C 语言的灵魂，也是最大的难点。

### 1. 什么是指针

指针就是**内存地址**。每个变量都存储在内存中，有唯一的地址。指针变量存储的是这个地址。

```c
#include <stdio.h>

int main() {
    int x = 42;
    int *p = &x;   // p 指向 x 的地址

    printf("x 的值：%d\n", x);
    printf("x 的地址：%p\n", &x);   // %p 输出地址
    printf("p 的值（地址）：%p\n", p);
    printf("p 指向的值：%d\n", *p); // *p 解引用，获取 p 指向的值

    *p = 100;      // 通过指针修改 x
    printf("x 的新值：%d\n", x);    // 100

    return 0;
}
```

> 对比 Python：Python 中"一切皆对象"、变量是对象的引用，和指针有相似之处，但 C 的指针更底层，可以直接操作内存。

### 2. 指针的声明和操作

```c
int *p;       // 指向 int 的指针
char *cp;     // 指向 char 的指针
double *dp;   // 指向 double 的指针

int x = 10;
p = &x;       // 取地址，& 运算符
*p = 20;      // 解引用，* 运算符访问指向的值
```

### 3. Null 指针

```c
int *p = NULL;   // 不指向任何有效地址
// 对 NULL 指针解引用会导致程序崩溃（段错误）
```

> 总是初始化指针，避免"野指针"。

### 4. 指针和数组

数组名本质上就是指向第一个元素的指针常量：

```c
int arr[5] = {10, 20, 30, 40, 50};
int *p = arr;        // 等价于 int *p = &arr[0]

printf("%d\n", *p);           // 10
printf("%d\n", *(p + 1));     // 20（指针加 1 实际加 4 字节，因为 int 占 4 字节）
printf("%d\n", arr[2]);       // 30
printf("%d\n", *(arr + 2));   // 30（arr[2] 等价于 *(arr + 2)）
```

> **指针算术：** `p + n` 实际跳过的字节数为 `n * sizeof(类型)`。

### 5. 指针与函数——传引用

C 是**传值调用**，函数内修改形参不会影响实参。通过指针可以实现"传引用"效果：

```c
#include <stdio.h>

void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

int main() {
    int x = 10, y = 20;
    swap(&x, &y);              // 传地址
    printf("x = %d, y = %d\n", x, y);  // x = 20, y = 10
    return 0;
}
```

### 6. 指针与 const

```c
int x = 10;
const int *p = &x;     // 不能通过 p 修改指向的值（*p = 20; ❌）
int *const p2 = &x;    // p2 不能指向其他变量（p2 = &y; ❌）
const int *const p3 = &x;  // 两者都不可变
```

### 7. 动态内存分配（malloc / free）

C 允许在运行时分配内存，这是实现动态数据结构的基石。

```c
#include <stdio.h>
#include <stdlib.h>  // malloc, free

int main() {
    int n = 5;
    // 分配能存放 n 个 int 的内存
    int *arr = (int *)malloc(n * sizeof(int));

    if (arr == NULL) {          // 分配失败
        printf("内存分配失败\n");
        return 1;
    }

    // 使用这块内存
    for (int i = 0; i < n; i++) {
        arr[i] = i * 10;
    }
    for (int i = 0; i < n; i++) {
        printf("arr[%d] = %d\n", i, arr[i]);
    }

    free(arr);      // 释放内存！忘记释放会导致内存泄漏
    return 0;
}
```

> **对比 Python：**
> - Python 自动管理内存（垃圾回收），无需手动释放
> - C 使用 `malloc()` 分配、`free()` 释放，必须成对出现
> - 忘记 `free()` → 内存泄漏；多次 `free()` → 崩溃

其他内存分配函数：

```c
int *p = calloc(n, sizeof(int));   // 分配并清零
int *p = realloc(old_p, new_size); // 重新分配大小（扩展或缩小）
```

---

## 七、函数

### 1. 函数定义

```c
返回类型 函数名(参数类型 参数名, ...) {
    // 函数体
    return 返回值;
}
```

```c
#include <stdio.h>

// 函数声明（原型），告诉编译器函数的签名
int add(int a, int b);

int main() {
    int result = add(3, 5);
    printf("3 + 5 = %d\n", result);
    return 0;
}

// 函数定义
int add(int a, int b) {
    return a + b;
}
```

> 如果函数定义在使用之后，需要先声明（原型）。如果定义在使用之前，可以不声明。

### 2. 函数分类

```c
// 无参数无返回值
void printSeparator(void) {      // void 表示无参数
    printf("------\n");
    // 不需要 return
}

// 有参数有返回值
int square(int x) {
    return x * x;
}
```

### 3. 作用域和生命周期

```c
int global = 100;          // 全局变量，整个文件可见

void func(void) {
    int local = 10;        // 局部变量，仅在函数内可见
    static int count = 0;  // 静态局部变量，函数结束时不会被销毁
    count++;
    printf("count = %d\n", count);
}
```

> - **全局变量**：程序启动时分配，结束时销毁
> - **局部变量**：进入函数时分配，离开函数时销毁（在栈上）
> - **static 局部变量**：只初始化一次，函数返回后仍然保持值

### 4. 递归

```c
#include <stdio.h>

int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

int main() {
    printf("5! = %d\n", factorial(5));  // 120
    return 0;
}
```

> 和 Python 的递归写法几乎一样。

### 5. 函数指针

```c
#include <stdio.h>

int add(int a, int b) { return a + b; }
int sub(int a, int b) { return a - b; }

int main() {
    int (*op)(int, int);  // 声明函数指针
    op = add;             // 指向 add 函数
    printf("%d\n", op(3, 2));  // 5

    op = sub;
    printf("%d\n", op(3, 2));  // 1

    return 0;
}
```

---

## 八、结构体（struct）

结构体是 C 中自定义组合数据类型的方式，类似于 Python 的 `class`（但只有数据，没有方法）。

### 1. 定义和使用

```c
#include <stdio.h>
#include <string.h>

// 定义结构体
struct Student {
    char name[50];
    int age;
    float score;
};

int main() {
    // 声明并初始化
    struct Student stu1 = {"张三", 20, 95.5};
    struct Student stu2;

    // 逐个赋值
    strcpy(stu2.name, "李四");
    stu2.age = 22;
    stu2.score = 88.0;

    // 访问成员
    printf("姓名：%s\n", stu1.name);
    printf("年龄：%d\n", stu1.age);
    printf("成绩：%.1f\n", stu1.score);

    return 0;
}
```

> **对比 Python：**
> ```python
> class Student:
>     def __init__(self, name, age, score):
>         self.name = name
>         self.age = age
>         self.score = score
> ```
> - C 的 struct 只有属性，没有方法
> - 字符串成员需要 `strcpy` 赋值，不能直接 `=`

### 2. typedef 简化类型名

```c
typedef struct {
    char name[50];
    int age;
    float score;
} Student;

// 之后可以直接用 Student
Student stu1 = {"王五", 19, 92.0};
```

### 3. 结构体指针

```c
Student stu = {"赵六", 21, 78.5};
Student *p = &stu;

// 两种访问方式
printf("%s\n", (*p).name);   // 先解引用再访问
printf("%d\n", p->age);      // 用 -> 简化（更常用）
printf("%.1f\n", p->score);
```

### 4. 结构体作为函数参数

```c
void printStudent(Student s) {           // 传值（复制整个结构体）
    printf("%s %d %.1f\n", s.name, s.age, s.score);
}

void printStudentPtr(const Student *s) { // 传指针（推荐，效率高）
    printf("%s %d %.1f\n", s->name, s->age, s->score);
}
```

> 结构体较大时，传指针比传值效率高得多（避免复制大量数据）。

---

## 九、常见数据结构

### 1. 单链表

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node *next;
} Node;

// 创建节点
Node *createNode(int data) {
    Node *newNode = (Node *)malloc(sizeof(Node));
    if (!newNode) return NULL;
    newNode->data = data;
    newNode->next = NULL;
    return newNode;
}

// 头部插入
void insertHead(Node **head, int data) {
    Node *newNode = createNode(data);
    newNode->next = *head;
    *head = newNode;
}

// 尾部插入
void insertTail(Node **head, int data) {
    Node *newNode = createNode(data);
    if (*head == NULL) {
        *head = newNode;
        return;
    }
    Node *cur = *head;
    while (cur->next) {
        cur = cur->next;
    }
    cur->next = newNode;
}

// 删除指定值
void deleteNode(Node **head, int data) {
    if (*head == NULL) return;
    if ((*head)->data == data) {
        Node *temp = *head;
        *head = (*head)->next;
        free(temp);
        return;
    }
    Node *cur = *head;
    while (cur->next && cur->next->data != data) {
        cur = cur->next;
    }
    if (cur->next) {
        Node *temp = cur->next;
        cur->next = temp->next;
        free(temp);
    }
}

// 遍历
void printList(Node *head) {
    while (head) {
        printf("%d -> ", head->data);
        head = head->next;
    }
    printf("NULL\n");
}

// 释放链表
void freeList(Node *head) {
    Node *tmp;
    while (head) {
        tmp = head;
        head = head->next;
        free(tmp);
    }
}

int main() {
    Node *head = NULL;
    insertHead(&head, 10);
    insertHead(&head, 20);
    insertTail(&head, 30);
    printList(head);        // 20 -> 10 -> 30 -> NULL
    deleteNode(&head, 10);
    printList(head);        // 20 -> 30 -> NULL
    freeList(head);
    return 0;
}
```

> **对比 Python：**
> - Python 的 list 底层已经是动态数组，不需要自己实现链表
> - C 中链表需要手动管理内存，每个节点都要 malloc/free
> - 链表优势：插入删除 O(1)，劣势：不支持随机访问

### 2. 栈（数组实现）

```c
#include <stdio.h>
#include <stdbool.h>

#define MAX 100

typedef struct {
    int data[MAX];
    int top;   // 栈顶索引，-1 表示空栈
} Stack;

void init(Stack *s) {
    s->top = -1;
}

bool isEmpty(Stack *s) {
    return s->top == -1;
}

bool isFull(Stack *s) {
    return s->top == MAX - 1;
}

void push(Stack *s, int val) {
    if (isFull(s)) {
        printf("栈已满\n");
        return;
    }
    s->data[++(s->top)] = val;
}

int pop(Stack *s) {
    if (isEmpty(s)) {
        printf("栈已空\n");
        return -1;
    }
    return s->data[(s->top)--];
}

int peek(Stack *s) {
    if (isEmpty(s)) return -1;
    return s->data[s->top];
}

int main() {
    Stack s;
    init(&s);
    push(&s, 1);
    push(&s, 2);
    push(&s, 3);
    printf("栈顶：%d\n", peek(&s));  // 3
    printf("出栈：%d\n", pop(&s));   // 3
    printf("出栈：%d\n", pop(&s));   // 2
    return 0;
}
```

> **对比 Python：**
> - Python：`列表.append()` 入栈，`列表.pop()` 出栈
> - C 中需要自己实现栈结构

### 3. 队列（数组实现，循环队列）

```c
#include <stdio.h>
#include <stdbool.h>

#define MAX 100

typedef struct {
    int data[MAX];
    int front;   // 队首
    int rear;    // 队尾
    int size;    // 当前元素个数
} Queue;

void init(Queue *q) {
    q->front = 0;
    q->rear = 0;
    q->size = 0;
}

bool isEmpty(Queue *q) {
    return q->size == 0;
}

bool isFull(Queue *q) {
    return q->size == MAX;
}

void enqueue(Queue *q, int val) {
    if (isFull(q)) {
        printf("队列已满\n");
        return;
    }
    q->data[q->rear] = val;
    q->rear = (q->rear + 1) % MAX;  // 循环
    q->size++;
}

int dequeue(Queue *q) {
    if (isEmpty(q)) {
        printf("队列已空\n");
        return -1;
    }
    int val = q->data[q->front];
    q->front = (q->front + 1) % MAX;
    q->size--;
    return val;
}

int peek(Queue *q) {
    if (isEmpty(q)) return -1;
    return q->data[q->front];
}

int main() {
    Queue q;
    init(&q);
    enqueue(&q, 10);
    enqueue(&q, 20);
    enqueue(&q, 30);
    printf("出队：%d\n", dequeue(&q));  // 10
    printf("出队：%d\n", dequeue(&q));  // 20
    enqueue(&q, 40);
    printf("出队：%d\n", dequeue(&q));  // 30
    printf("出队：%d\n", dequeue(&q));  // 40
    return 0;
}
```

### 4. 栈（链表实现）

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct Node {
    int data;
    struct Node *next;
} Node;

typedef struct {
    Node *top;
} Stack;

void init(Stack *s) {
    s->top = NULL;
}

bool isEmpty(Stack *s) {
    return s->top == NULL;
}

void push(Stack *s, int val) {
    Node *newNode = (Node *)malloc(sizeof(Node));
    newNode->data = val;
    newNode->next = s->top;
    s->top = newNode;
}

int pop(Stack *s) {
    if (isEmpty(s)) return -1;
    Node *temp = s->top;
    int val = temp->data;
    s->top = temp->next;
    free(temp);
    return val;
}

int peek(Stack *s) {
    if (isEmpty(s)) return -1;
    return s->top->data;
}

void freeStack(Stack *s) {
    while (s->top) {
        Node *temp = s->top;
        s->top = s->top->next;
        free(temp);
    }
}
```

### 5. 二叉树

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int data;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;

TreeNode *createNode(int data) {
    TreeNode *node = (TreeNode *)malloc(sizeof(TreeNode));
    node->data = data;
    node->left = node->right = NULL;
    return node;
}

// 前序遍历：根 -> 左 -> 右
void preorder(TreeNode *root) {
    if (root == NULL) return;
    printf("%d ", root->data);
    preorder(root->left);
    preorder(root->right);
}

// 中序遍历：左 -> 根 -> 右
void inorder(TreeNode *root) {
    if (root == NULL) return;
    inorder(root->left);
    printf("%d ", root->data);
    inorder(root->right);
}

// 后序遍历：左 -> 右 -> 根
void postorder(TreeNode *root) {
    if (root == NULL) return;
    postorder(root->left);
    postorder(root->right);
    printf("%d ", root->data);
}

// 二叉搜索树插入
TreeNode *insert(TreeNode *root, int data) {
    if (root == NULL) return createNode(data);
    if (data < root->data)
        root->left = insert(root->left, data);
    else if (data > root->data)
        root->right = insert(root->right, data);
    return root;
}

// 二叉搜索树查找
TreeNode *search(TreeNode *root, int target) {
    if (root == NULL || root->data == target)
        return root;
    if (target < root->data)
        return search(root->left, target);
    return search(root->right, target);
}

// 释放二叉树
void freeTree(TreeNode *root) {
    if (root == NULL) return;
    freeTree(root->left);
    freeTree(root->right);
    free(root);
}

int main() {
    TreeNode *root = NULL;
    int values[] = {50, 30, 70, 20, 40, 60, 80};
    for (int i = 0; i < 7; i++)
        root = insert(root, values[i]);

    printf("中序遍历：");
    inorder(root);    // 20 30 40 50 60 70 80
    printf("\n");

    TreeNode *found = search(root, 60);
    printf("查找 60：%s\n", found ? "找到" : "未找到");

    freeTree(root);
    return 0;
}
```

---

## 十、文件操作

```c
#include <stdio.h>

int main() {
    FILE *fp;

    // 写文件
    fp = fopen("test.txt", "w");   // w：写入，r：读取，a：追加
    if (fp == NULL) {
        printf("文件打开失败\n");
        return 1;
    }
    fprintf(fp, "Hello, 文件!\n");
    fprintf(fp, "数字：%d\n", 42);
    fclose(fp);

    // 读文件
    char line[100];
    fp = fopen("test.txt", "r");
    if (fp == NULL) {
        printf("文件打开失败\n");
        return 1;
    }
    while (fgets(line, sizeof(line), fp)) {
        printf("读取：%s", line);
    }
    fclose(fp);

    return 0;
}
```

> **对比 Python：**
> ```python
> with open("test.txt", "w") as f:
>     f.write("hello\n")
> ```
> - C 需要 `fopen` / `fclose`，没有 `with` 语句
> - C 读取行用 `fgets()`，Python 用 `for line in f`

### 常用文件函数

| 函数 | 说明 |
|------|------|
| `fopen(文件名, 模式)` | 打开文件，返回 `FILE *` |
| `fclose(fp)` | 关闭文件 |
| `fprintf(fp, 格式, ...)` | 格式化写入文件 |
| `fscanf(fp, 格式, ...)` | 格式化读取文件 |
| `fgets(buf, size, fp)` | 读取一行 |
| `fputc(c, fp)` / `fgetc(fp)` | 读写单个字符 |
| `fwrite(buf, size, count, fp)` | 二进制写入 |
| `fread(buf, size, count, fp)` | 二进制读取 |
| `feof(fp)` | 判断是否到达文件末尾 |

---

## 十一、预处理指令

```c
#include <stdio.h>    // 包含头文件
#include "myheader.h" // 包含自定义头文件
#define PI 3.14159     // 定义宏常量
#define MAX(a, b) ((a) > (b) ? (a) : (b))  // 宏函数

#ifdef DEBUG
    printf("调试模式：x = %d\n", x);
#endif

#ifndef HEADER_H
#define HEADER_H
// 头文件保护，防止重复包含
#endif
```

### 条件编译

```c
#include <stdio.h>

#define VERSION 2

int main() {
#if VERSION == 1
    printf("版本 1\n");
#elif VERSION == 2
    printf("版本 2\n");
#else
    printf("未知版本\n");
#endif
    return 0;
}
```

---

## 十二、常见坑点与最佳实践

### 1. 数组越界
```c
int arr[5] = {0};
arr[5] = 42;  // ❌ 越界！C 不会报错，但可能覆盖其他数据
```
→ 始终确保索引在 `0 ~ size-1` 范围内。

### 2. 未初始化变量
```c
int x;
printf("%d\n", x);  // ❌ x 的值是垃圾值（未定义行为）
```
→ 始终初始化变量。

### 3. 内存泄漏
```c
int *p = malloc(100);
// 忘记 free(p) → 内存泄漏
```
→ `malloc` 和 `free` 必须成对出现。

### 4. 野指针
```c
int *p;
*p = 42;  // ❌ p 没有指向合法内存
```
→ 指针初始化为 `NULL` 或有效地址。

### 5. 字符串溢出
```c
char buf[5];
strcpy(buf, "Hello World");  // ❌ 缓冲区溢出！
```
→ 使用 `strncpy` 或确保目标数组足够大。

### 6. 忘记 break
```c
switch (n) {
    case 1:
        printf("一");   // 没有 break 会继续执行 case 2
    case 2:
        printf("二");
}
```
→ 每个 `case` 末尾加 `break`，除非故意穿透。

### 7. scanf 忘记 &
```c
int x;
scanf("%d", x);   // ❌ 缺少 &，它会崩溃
scanf("%d", &x);  // ✅ 正确
```

---

## 十三、C 与 Python 核心差异速查

| 概念 | Python | C |
|------|--------|----|
| 类型系统 | 动态类型 | 静态类型 |
| 变量声明 | 无需声明类型 | `int x;` 先声明后使用 |
| 字符串 | 内置 `str`，功能丰富 | 字符数组 + 函数库 |
| 列表/数组 | 动态大小 list | 固定大小数组 |
| 字典 | 内置 dict | 需要自己实现或使用第三方库 |
| 面向对象 | 完整 OOP 支持 | 无，只有 struct |
| 内存管理 | 自动垃圾回收 | 手动 malloc/free |
| 函数返回值 | 可返回多个值 | 只能返回一个值（可用指针"返回"多个） |
| 错误处理 | try/except | 返回值检查（无异常机制） |
| 布尔类型 | True/False | 0/非0（C99 有 _Bool） |
| 代码块 | 缩进 | 花括号 {} |
| 分号 | 不需要 | 每个语句末尾都要 `;` |
| 编译/解释 | 解释型 | 编译型 |
| 运行速度 | 较慢 | 很快 |

---

## 十四、推荐学习路径

1. **基础语法**：变量、数据类型、输入输出、运算符
2. **控制流**：if、for、while、switch
3. **数组和字符串**：一维/二维数组、字符串函数
4. **函数**：定义、参数传递、返回值、递归
5. **指针**：地址、解引用、指针与数组、动态内存
6. **结构体**：定义、嵌套、typedef
7. **数据结构**：链表、栈、队列、二叉树
8. **文件操作**：读写文件
9. **进阶**：多文件编程、Makefile、多线程、网络编程

### 推荐资源

- **书籍**：《C Primer Plus》（中文第6版）——最适合零基础
- **书籍**：《The C Programming Language》（K&R）——经典但较精简
- **在线练习**：LeetCode 用 C 刷题、Codewars
- **参考文档**：cppreference.com

### 练习项目建议

1. 学生成绩管理系统（结构体 + 文件）
2. 通讯录（链表增删查改 + 文件持久化）
3. 简易计算器（中缀表达式转后缀，栈的应用）
4. 贪吃蛇（控制台版，练习指针和链表）
5. 简易 Shell（进程管理，Linux 系统调用）

---

*Happy Coding! C 语言虽然比 Python 繁琐，但它让你真正理解计算机的工作原理，是通往系统编程的必经之路。*
