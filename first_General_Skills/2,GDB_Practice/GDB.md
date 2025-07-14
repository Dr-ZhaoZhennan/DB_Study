# 我的学习内容：
## GDB做的事情
1，随着程序启动，观察任何可能影响程序运行的内容
2，按照自己的想法，让其在特定情况下停止
3，程序停止之后，查看程序做了什么，当前是什么装填
4，更改程序某些内容，正确错误互相修改，查看对于修改内容的相应。

调试范围：本地程序，模拟器远程代码
适配：win,linux,macos
具体原理太复杂了，暂时先不看了。。。

## 安装GDB
### Linux系统：
1，Ubuntu系统：
```bash
sudo apt install gdb
```
2,EulerOS/SUSE系统：
```bash
yum install gdb
```
3，Linux系统编译安装：
安装地址：
```html
http://ftp/gnu.org/gnu/gdb
```

下载之后上传Linux解压：
```bash
tar -xvzf gdb-14.2.tar.gz
```

进入源码目录，配置GDB：cd gdb-14.2 &&./configure
编译安装：make &&make install
查看版本，验证安装：
```bash
gdb -v
```

## GDB实操代码
1，GDB的启动推出和帮助
2，如何设置和管理断点
3，查改运行数据
4，控制程序运行


# 《GDB 调试从命令行到 VS Code：全面掌握程序调试》

### GDB 调试入门教程：从命令行到 VS Code 可视化调试&#xA;

这份教程将带你从基础的 GDB 命令行调试入门，逐步过渡到使用 VS Code 进行可视化调试，帮助你掌握程序调试的核心技能。


#### **1. GDB 基础概念**

GDB（GNU Debugger）是一个强大的命令行调试工具，用于调试 C、C++ 等语言编写的程序。它可以让你：




*   在指定位置暂停程序执行（断点）


*   逐行执行代码，观察程序运行流程


*   查看和修改变量的值


*   分析程序崩溃原因（如段错误）


#### **2. 环境准备**

##### **2.1 安装 MinGW（Windows 用户）**

MinGW 提供 GCC 编译器和 GDB 调试器：




1.  下载安装包：[https://osdn.net/projects/mingw/](https://osdn.net/projects/mingw/)

2.  安装时勾选：`mingw32-gcc-g++` 和 `mingw32-gdb`

3.  配置环境变量：将`C:\MinGW\bin`添加到系统`Path`中


验证安装：




```
gcc --version  # 应显示版本信息


gdb --version  # 应显示版本信息
```

##### **2.2 Linux/macOS 用户**

Linux 用户：




```
sudo apt-get install gcc gdb  # Ubuntu/Debian


sudo yum install gcc gdb      # CentOS/RHEL
```

macOS 用户（需先安装 Xcode Command Line Tools）：




```
xcode-select --install
```

#### **3. 编译带调试信息的程序**

调试前需要用`-g`选项编译代码，生成调试符号：




```
gcc -g factorial.c -o factorial
```

> 示例代码
>
> `factorial.c`
>
> ：
>



```
\#include \<stdio.h>


long long factorial(int n) {


&#x20;   long long result = 1;


&#x20;   for (int i = 0; i <= n; i++) {  // 注意：这里有错误（i应从1开始）


&#x20;       result \*= i;


&#x20;   }


&#x20;   return result;


}


int main() {


&#x20;   int num;


&#x20;   printf("请输入一个正整数: ");


&#x20;   scanf("%d", \&num);


&#x20;   printf("%d的阶乘是: %lld\n", num, factorial(num));


&#x20;   return 0;


}
```

#### **4. GDB 命令行调试实战**

##### **4.1 启动 GDB**



```
gdb factorial  # 加载可执行文件
```

##### **4.2 基本调试命令**



| 命令&#xA;          | 作用&#xA;                             |
| ---------------- | ----------------------------------- |
| `break 函数名`      | 在函数入口设置断点（如：`break factorial`）&#xA; |
| `break 行号`       | 在指定行设置断点（如：`break 5`）&#xA;          |
| `run` 或 `r`      | 运行程序，遇到断点暂停&#xA;                    |
| `next` 或 `n`     | 单步执行下一行（不进入函数）&#xA;                 |
| `step` 或 `s`     | 单步执行下一行（进入函数内部）&#xA;                |
| `continue` 或 `c` | 继续执行直到下一个断点&#xA;                    |
| `print 变量名`      | 查看变量值（如：`print i` 或简写 `p i`）&#xA;   |
| `list` 或 `l`     | 显示当前代码上下文&#xA;                      |
| `quit` 或 `q`     | 退出 GDB&#xA;                         |

##### **4.3 调试示例：找出阶乘计算错误**



```
(gdb) break factorial    # 在factorial函数设置断点


(gdb) run                # 运行程序


请输入一个正整数: 5      # 输入5


(gdb) next               # 单步执行


(gdb) print result       # 查看result的值


\$1 = 1


(gdb) next               # 继续单步执行


(gdb) print i            # 查看i的值


\$2 = 0                   # 发现i从0开始（错误！应从1开始）


(gdb) next


(gdb) print result       # 此时result = 0（因为乘以了0）


\$3 = 0
```

#### **5. 使用 VS Code 进行可视化调试**

VS Code 可以集成 GDB，提供更友好的图形化调试界面。


##### **5.1 安装 C/C++ 扩展**

在 VS Code 扩展商店中搜索并安装`C/C++`扩展（作者：Microsoft）。


##### **5.2 配置 launch.json**



1.  打开包含`factorial.c`的文件夹


2.  点击左侧调试图标（或按`Ctrl+Shift+D`）


3.  点击 "创建 launch.json 文件"


4.  选择 "C++ (GDB/LLDB)" 环境


5.  修改配置如下：




```
{


&#x20;   "version": "0.2.0",


&#x20;   "configurations": \[


&#x20;       {


&#x20;           "name": "GDB调试",


&#x20;           "type": "cppdbg",


&#x20;           "request": "launch",


&#x20;           "program": "\${workspaceFolder}/factorial",  // 可执行文件路径


&#x20;           "args": \[],  // 程序参数


&#x20;           "stopAtEntry": false,


&#x20;           "cwd": "\${workspaceFolder}",


&#x20;           "environment": \[],


&#x20;           "externalConsole": false,


&#x20;           "MIMode": "gdb",


&#x20;           "miDebuggerPath": "gdb",  // GDB路径（确保已添加到PATH）


&#x20;           "setupCommands": \[


&#x20;               {


&#x20;                   "description": "为GDB启用整齐打印",


&#x20;                   "text": "-enable-pretty-printing",


&#x20;                   "ignoreFailures": true


&#x20;               }


&#x20;           ]


&#x20;       }


&#x20;   ]


}
```

##### **5.3 开始调试**



1.  在代码行号左侧点击设置断点（红色圆点）


2.  按`F5`启动调试


3.  使用调试工具栏进行操作：


*



![调试按钮](https://img.shields.io/badge/继续-F5-green)

&#x20;继续执行




*



![单步跳过](https://img.shields.io/badge/单步跳过-F10-yellow)

&#x20;单步跳过（对应 GDB 的`next`）




*



![单步调试](https://img.shields.io/badge/单步调试-F11-orange)

&#x20;单步调试（对应 GDB 的`step`）




*



![跳出](https://img.shields.io/badge/跳出-Shift+F11-blue)

&#x20;跳出当前函数




*



![停止](https://img.shields.io/badge/停止-Shift+F5-red)

&#x20;停止调试




1.  查看变量面板：自动显示当前作用域的变量值


2.  查看调用栈：显示函数调用关系


#### **6. 进阶调试技巧**

##### **6.1 条件断点**

在 VS Code 中右键断点→"编辑断点"，设置条件（如`i > 5`）。


在 GDB 中使用命令：




```
break 8 if i > 5  # 在第8行设置条件断点
```

##### **6.2 观察点（Watch Point）**

监视变量变化，当变量值改变时暂停程序：




```
(gdb) watch result  # 监视result变量
```

##### **6.3 多线程调试**



```
info threads       # 查看所有线程


thread 线程ID      # 切换到指定线程
```

#### **7. 常见问题与解决方案**



1.  **GDB 找不到可执行文件**

    确保：


*   已使用`-g`选项编译


*   可执行文件与 GDB 在同一目录，或使用绝对路径指定


1.  **VS Code 调试无法启动**

*   检查`launch.json`配置是否正确


*   确保 GDB 已安装且路径正确


*   尝试重新生成任务配置（`.vscode/tasks.json`）


1.  **变量显示为 "优化掉的"**

    编译时不要使用优化选项（如`-O2`），调试时建议使用`-O0`（不优化）。


#### **总结**



*   **GDB 命令行**适合高级用户和服务器环境，需记忆命令但功能强大。


*   **VS Code 调试**适合快速定位问题，提供直观的图形化界面。


*   核心调试思路相同：设置断点→单步执行→观察变量→修复问题。


通过本教程，你已掌握基本调试技能，可以开始调试自己的程序了！实践中多尝试不同命令，逐步掌握更高级的调试技巧。&#x20;

> （注：文档部分内容可能由 AI 生成）
>