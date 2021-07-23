---
title: bazel C++语法入门
date: 2020-12-16 14:46:35
tags: [Bazel,C++]
categories:
top:
---

Bazel是Google开源的一款代码构建工具。Bazel支持多种语言并且跨平台，还支持增量编译、自动化测试和部署、具有再现性（Reproducibility）和规模化等特征。Bazel 在谷歌大规模软件开发实践能力方面起着至关重要的作用。

<!-- more -->

# Install Bazel
macOS:  `brew install bazel`
Ubuntu: `sudo apt install bazel`


bazel的所有代码都在当前工程，每个工程都是一个 WORKSPACE 。
 每个WORKSPACE下有多个BUILD文件。
 BUILD内是多个targets，这些targets都是以[starlark](https://docs.bazel.build/versions/master/skylark/language.html)语言声明。

## Starlark语言

- 和python很像。
- 线程安全
- 数据类型有 None, bool, dict, function, int, list, string, depset, struct
- 可变数据结构有 lists 和 dicts

## 命令行

规则

```xml
bazel [<startup options>] <command> [<args>]
```

或

```xml
bazel [<startup options>] <command> [<args>] -- [<target patterns>]
```

[命令行参数文档](https://docs.bazel.build/versions/master/command-line-reference.html)

### 工作原理

- 加载与target有关的BUILD文件
- 分析inputs和dependencies，生成 action graph
- 执行graph，产出outputs

action graph： bazel依赖这个图来追踪文件变化，以及是否需要重新编译，并且还可以为用户提供代码之间的依赖关系图。

## 依赖声明

- 同一个文件BUILD之内

```bash
cc_library(
    name = "hello-greet",		# target名
    srcs = ["hello-greet.cc"],	# 源文件
    hdrs = ["hello-greet.h"],	# 头文件
)

cc_binary(
    name = "hello-world",
    srcs = ["hello-world.cc"],
    deps = [
        ":hello-greet",	# 依赖
    ],
)
```

- 不同BUILD文件之间

```bash
cc_library(
    name = "hello-greet",
    srcs = ["hello-greet.cc"],
    hdrs = ["hello-greet.h"],
)

cc_binary(
    name = "hello-world",
    srcs = ["hello-world.cc"],
    deps = [
        ":hello-greet",
        "//lib:hello-time",
    ],
)
```

:hello-time 定义在 lib 目录
 不同的目录BUILD在bazel中被称为 不同的package

- 可见性
   同一个package内的targets默认互相可见
   不同package之间targets的可见性需要手动定义

```bash
cc_library(
    name = "hello-time",
    srcs = ["hello-time.cc"],
    hdrs = ["hello-time.h"],
    visibility = ["//main:__pkg__"],
)
```

可以在每个package的BUILD文件顶部声明其中的targets对其他包的默认可见性

```go
package(
    default_visibility = [
        "//tensorflow_serving:internal",
    ],
    features = ["-layering_check"],
)
```

对所有包可见声明如下



```bash
cc_proto_library(
    name = "cc_echo_c++_proto",
    deps = [
        ":echo_c++_proto",
    ],
    visibility = [
        "//visibility:public",
    ],
)
```

## target

有2种

- rule target，比如 cc_library
- file target

## C++ 最佳实践

#### BUILD文件

- 一个包（package）包含一个BUILD文件
- 每个BUILD文件包含一个 cc_library 规则目标, 每条规则都是一个目标（target）
- 尽可能细粒度C++库，以提高并行速度，并减少增量编译
- 如果srcs中只有一个文件，那么 cc_library的名字和这个文件名相同，比如：

```bash
   cc_library(
       name = "mylib",
       srcs = ["mylib.cc"],
       hdrs = ["mylib.h"],
       deps = [":lower-level-lib"]
   )
```

- 每个library都有个单独的test target，并且以_test结尾命名这个target和测试文件名，比如

```bash
   cc_test(
       name = "mylib_test",
       srcs = ["mylib_test.cc"],
       deps = [":mylib"]
   )
```

#### include路径

- 所有include路径都相对于WORKSPACE目录
- 非系统目录用 `#include "foo/bar/baz.h"`,  系统目录用 `#include <foo/bar/baz.h>`
- 不要使用 `.` 和 `..`
- 对第三方库可以使用  [`include_prefix`](https://docs.bazel.build/versions/master/be/c-cpp.html#cc_library.include_prefix) 和 [`strip_include_prefix`](https://docs.bazel.build/versions/master/be/c-cpp.html#cc_library.strip_include_prefix)

有时候依赖第三方库的时候，这些库里的文件已有的include path如果放到当前目录，会不符合从workspace root引用文件的规则，就需要添加目录，比如下面的目录



```css
└── my-project
    ├── legacy
    │   └── some_lib
    │       ├── BUILD
    │       ├── include
    │       │   └── some_lib.h
    │       └── some_lib.cc
    └── WORKSPACE
```

以上，bazel要求`some_lib.h`必须以`legacy/some_lib/include/some_lib.h`这个形式包含，但`some_lib.cc`现在是`"include/some_lib.h"`这样包含的，要使这个include path有效，需要按如下方式指定路径(待验证)：



```bash
cc_library(
    name = "some_lib",
    srcs = ["some_lib.cc"],
    hdrs = ["include/some_lib.h"],
    copts = ["-Ilegacy/some_lib/include"],
)
```

## 包含多个文件

使用[glob](https://docs.bazel.build/versions/be/functions.html#glob), 全局匹配，类似CMake。

```bash
cc_library(
    name = "build-all-the-files",
    srcs = glob(["*.cc"]),
    hdrs = glob(["*.h"]),		# 匹配BUILD文件目录下所有.h文件
)
```

- copts：C的编译选项

```bash
cc_library(
    name = "some_lib",
    srcs = ["some_lib.cc"],
    hdrs = ["include/some_lib.h"],
    copts = ["-Ilegacy/some_lib/include"], # 指定头文件目录
) 
```

## 依赖处理

- bazel中的依赖不传递解析

如果包含了其他头文件，就要把这个头文件的target包含进来。这个头文件内部的include则不用管。比如

sandwich依赖bread，bread依赖flour，但sandwich不依赖flour。

```bash
cc_library(
    name = "sandwich",
    srcs = ["sandwich.cc"],
    hdrs = ["sandwich.h"],
    deps = [":bread"],
)

cc_library(
    name = "bread",
    srcs = ["bread.cc"],
    hdrs = ["bread.h"],
    deps = [":flour"],
)

cc_library(
    name = "flour",
    srcs = ["flour.cc"],
    hdrs = ["flour.h"],
)
```

- 单个头文件，如果没有实现，也需要定义target，比如

```bash
cc_library(
    name = "source_adapter",
    hdrs = ["source_adapter.h"],
    visibility = [
        "//visibility:public",
    ],
    deps = [
        ":loader",
        ":servable_data",
        ":source",
        ":storage_path",
        ":target",
        "//tensorflow_serving/util:class_registration",
        "@org_tensorflow//tensorflow/core:lib",
    ],
)
```

## 包含外部库

假设我们要使用[Google Test](https://github.com/google/googletest)，可以在WORKSPACE中这样指定：

```bash
new_http_archive(
    name = "gtest",
    url = "https://github.com/google/googletest/archive/release-1.7.0.zip",
    sha256 = "b58cb7547a28b2c718d1e38aee18a3659c9e3ff52440297e965f5edffe34b6d0",
    build_file = "gtest.BUILD",
)
```

【注】如果库已经包含了一个BUILD文件，可以使用 `non-new_` 函数。
 创建文件`gtest.BUILD`，这个文件用来编译Google Test，由于google test比较特殊的需求，所以它的编译规则会更复杂，特殊性在于：

- `googletest-release-1.7.0/src/gtest-all.cc` `#include`了`googletest-release-1.7.0/src/`下的所有文件，所以需要把这个文件排除掉
- 它的头文件都是相对于这个目录的`googletest-release-1.7.0/include/`，比如`"gtest/gtest.h"`，所以需要把这个目录加到copts的-I选项中
- 需要链接pthread

所以，最终编译规则如下：

```csharp
cc_library(
    name = "main",
    srcs = glob(
        ["googletest-release-1.7.0/src/*.cc"],
        exclude = ["googletest-release-1.7.0/src/gtest-all.cc"]
    ),
    hdrs = glob([
        "googletest-release-1.7.0/include/**/*.h",
        "googletest-release-1.7.0/src/*.h"
    ]),
    copts = [
        "-Iexternal/gtest/googletest-release-1.7.0/include"
    ],
    linkopts = ["-pthread"],
    visibility = ["//visibility:public"],
)
```

这个看起来有点乱，因为里面包含了那个版本目录名，这个名字可以在`new_http_archive`中使用`strip_prefix`去掉:

```bash
new_http_archive(
    name = "gtest",
    url = "https://github.com/google/googletest/archive/release-1.7.0.zip",
    sha256 = "b58cb7547a28b2c718d1e38aee18a3659c9e3ff52440297e965f5edffe34b6d0",
    build_file = "gtest.BUILD",
    strip_prefix = "googletest-release-1.7.0",
)
```

去掉后的gtest.BUILD文件如下：

```csharp
cc_library(
    name = "main",
    srcs = glob(
        ["src/*.cc"],
        exclude = ["src/gtest-all.cc"]
    ),
    hdrs = glob([
        "include/**/*.h",
        "src/*.h"
    ]),
    copts = ["-Iexternal/gtest/include"],
    linkopts = ["-pthread"],
    visibility = ["//visibility:public"],
)
```

现在，其他的 `cc_ rules` 可以依赖于 `@gtest//:main` 。

更详细的cc rule说明参考 [cc rules](https://docs.bazel.build/versions/master/be/c-cpp.html)

## 编写测试用例

创建文件 `./test/hello-test.cc`

```cpp
#include "gtest/gtest.h"
#include "lib/hello-greet.h"

TEST(HelloTest, GetGreet) {
  EXPECT_EQ(get_greet("Bazel"), "Hello Bazel");
}
```

创建 `./test/BUILD`

```bash
cc_test(
    name = "hello-test",
    srcs = ["hello-test.cc"],
    copts = ["-Iexternal/gtest/include"],
    deps = [
        "@gtest//:main",
        "//lib:hello-greet",
    ],
)
```

注意，要使`hello-greet`对`hello-test`可见，需要在 `./lib/BUILD`文件中添加属性`visibility`，值为 `//test:__pkg__`。

运行测试用例：

```bash
bazel test test:hello-test
```

输出：

```bash
INFO: Found 1 test target...
Target //test:hello-test up-to-date:
  bazel-bin/test/hello-test
INFO: Elapsed time: 4.497s, Critical Path: 2.53s
//test:hello-test PASSED in 0.3s

Executed 1 out of 1 tests: 1 test passes.
```

该部分来自于 [bazel C++ use case](https://docs.bazel.build/versions/master/cpp-use-cases.html)

## 包含预编译的库

- 动态库

```bash
cc_library(
    name = "mylib",
    srcs = ["mylib.so"],
    hdrs = ["mylib.h"],
)
```

## 处理外部依赖

[Working with external dependencies](https://docs.bazel.build/versions/master/external.html)

#### 依赖bazel工程

- [`local_repository`](http://docs.bazel.build/be/workspace.html#local_repository)
- [`git_repository`](https://docs.bazel.build/be/workspace.html#git_repository)
- [`http_archive`](http://docs.bazel.build/be/workspace.html#http_archive)

### 依赖非bazel工程

- [`new_local_repository`](http://docs.bazel.build/be/workspace.html#new_local_repository)
- [`new_git_repository`](https://docs.bazel.build/be/workspace.html#new_git_repository)
- [`new_http_archive`](http://docs.bazel.build/be/workspace.html#new_http_archive)

需要编写BUILD文件

### 依赖隐藏（Shadowing）

- 依赖同一个package的不同版本

## .bazelrc，Bazel 的配置文件

Bazel 有许多选项参数，一些参数是经常变化的，例如 --subcommands 还有一些是不怎么变化的。为了避免每次构建都写参数，你能够指定配置文件。

### .bazelrc 文件位置

Bazel 配置文件在下列地方，按照先后顺序加载，所以后边的可以覆盖前边的选项。控制那个文件被加载是启动选项。

1. system rc
    `/etc/bazel.bazelrc`
    如果其他系统需要，你必须自己构建 Bazel 二进制，并且使用 BAZEL_SYSTEM_BAZELRC_PATH 值 在 //src/main/cpp:option_processor.
2. workspace rc
    `$workspace/.bazelrc`
3. home rc
    `$HOME/.bazelrc`
4. 用户指定 rc
    `--bazelrc=file`
    除此之外，bazel 还会查找全局 rc 文件，参见 [global bazelrc section](https://links.jianshu.com/go?to=https%3A%2F%2Fdocs.bazel.build%2Fversions%2F3.7.0%2Fguide.html%23global_bazelrc)



**References:**

- [bazel C++语法入门](https://www.jianshu.com/p/4e778df3c13b)

- [getting started bazel C++](https://docs.bazel.build/versions/master/tutorial/cpp.html)

- [工具 Bazel](https://www.cnblogs.com/yangwenhuan/p/12882366.html)