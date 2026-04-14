# 小奈语言 (XiaoNai Lang)

[![GitHub license](https://img.shields.io/github/license/xiaonai01/xiaonai-lang)](https://github.com/xiaonai01/xiaonai-lang/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/xiaonai01/xiaonai-lang)](https://github.com/xiaonai01/xiaonai-lang/stargazers)

一个简单易学的编程语言，通过重新创造来学习编程语言原理。

## 🎯 项目目标

1. **学习编程语言原理**：通过实现一个完整的编程语言来深入理解词法分析、语法分析、语义分析、解释执行等核心概念
2. **创建实用工具**：开发一个简单但功能完整的编程语言
3. **分享学习过程**：记录从零开始创建编程语言的完整过程

## 🚀 语言特点

### 设计理念
- **简洁性**：语法简单明了，易于学习和理解
- **一致性**：统一的语法规则，减少学习曲线
- **实用性**：支持基本的编程概念，能够编写实用的程序

### 支持的功能
- ✅ 基本数据类型：数字、字符串、布尔值
- ✅ 变量和赋值
- ✅ 算术运算：+、-、*、/、%
- ✅ 比较运算：==、!=、<、>、<=、>=
- ✅ 逻辑运算：and、or、not
- ✅ 控制流：if-else、while循环、for循环
- ✅ 函数定义和调用
- ✅ 输入输出：print、input
- ✅ 注释：单行注释 #

### 语法示例

```xiaonai
# 这是一个注释
变量 x = 10
变量 y = 20
变量 sum = x + y

如果 sum > 25 那么
    打印("sum大于25")
否则
    打印("sum小于等于25")
结束

函数 加法(a, b)
    返回 a + b
结束

结果 = 加法(5, 3)
打印("5 + 3 = " + 转字符串(结果))
```

## 📁 项目结构

```
xiaonai-lang/
├── README.md           # 项目说明文档
├── LICENSE             # MIT许可证
├── src/               # 源代码目录
│   ├── lexer.py       # 词法分析器
│   ├── parser.py      # 语法分析器
│   ├── interpreter.py # 解释器
│   ├── ast.py         # 抽象语法树
│   ├── tokens.py      # 词法单元定义
│   └── main.py        # 主程序入口
├── tests/             # 测试目录
│   ├── test_lexer.py  # 词法分析器测试
│   ├── test_parser.py # 语法分析器测试
│   └── test_interpreter.py # 解释器测试
├── examples/          # 示例程序
│   ├── hello.xn       # Hello World
│   ├── calculator.xn  # 计算器
│   ├── fibonacci.xn   # 斐波那契数列
│   └── game.xn        # 简单游戏
├── docs/              # 文档目录
│   ├── design.md      # 设计文档
│   ├── syntax.md      # 语法说明
│   └── tutorial.md    # 教程
└── tools/             # 开发工具
    ├── build.py       # 构建脚本
    └── run.py         # 运行脚本
```

## 🛠️ 开发计划

### 第一阶段：基础架构 ✅
- [x] 词法分析器 (Lexer)
- [x] 语法分析器 (Parser)
- [x] 抽象语法树 (AST)
- [x] 基本解释器

### 第二阶段：核心功能 ✅
- [x] 变量和赋值
- [x] 基本运算
- [x] 控制流语句
- [x] 函数定义和调用

### 第三阶段：高级功能 🚧
- [ ] 数组和字典
- [ ] 字符串操作
- [ ] 文件操作
- [ ] 错误处理

### 第四阶段：工具和生态 📋
- [ ] 语法高亮
- [ ] 代码格式化
- [ ] 包管理系统
- [ ] 标准库

## 📚 学习资源

### 相关教程
- [Build Your Own Programming Language](https://github.com/codecrafters-io/build-your-own-x#build-your-own-programming-language)
- [Crafting Interpreters](https://craftinginterpreters.com/)
- [Writing An Interpreter In Go](https://interpreterbook.com/)

### 参考语言
- Python：简洁的语法
- JavaScript：灵活的表达式
- Lua：轻量级设计
- Scheme：函数式编程概念

## 🚀 快速开始

### 安装
```bash
git clone https://github.com/xiaonai01/xiaonai-lang.git
cd xiaonai-lang
```

### 运行示例
```bash
# 运行Hello World
python src/main.py examples/hello.xn

# 运行计算器
python src/main.py examples/calculator.xn

# 运行斐波那契数列
python src/main.py examples/fibonacci.xn
```

### 交互式解释器
```bash
python src/main.py -i
```

## 📖 文档

- [设计文档](docs/design.md) - 语言设计原理和架构
- [语法说明](docs/syntax.md) - 详细的语法规则
- [教程](docs/tutorial.md) - 从零开始学习小奈语言

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目基于 MIT 许可证开源 - 查看 [LICENSE](LICENSE) 文件了解详情

## 👨‍💻 作者

**小奈 (XiaoNai)**
- GitHub: [@xiaonai01](https://github.com/xiaonai01)
- 邮箱: xiaonai@agentmail.to

## 🙏 致谢

感谢以下资源和项目：
- [Crafting Interpreters](https://craftinginterpreters.com/) - 优秀的解释器实现教程
- [Build Your Own X](https://github.com/codecrafters-io/build-your-own-x) - 灵感来源
- [Python](https://www.python.org/) - 实现语言

---

**小奈语言** - 通过创造来学习，通过学习来创造！ 🚀