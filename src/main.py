#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小奈语言主程序
命令行工具，可以运行小奈语言文件或启动交互式解释器
"""
import sys
import os
import argparse
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from lexer import lex
from parser import parse
from interpreter import Interpreter, run

def run_file(file_path: str):
    """运行小奈语言文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        print(f"运行文件: {file_path}")
        print("=" * 50)
        
        result = run(source)
        
        print("=" * 50)
        if result is not None:
            print(f"程序返回值: {result}")
        
    except FileNotFoundError:
        print(f"错误: 文件 '{file_path}' 不存在")
        sys.exit(1)
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)

def interactive_mode():
    """交互式解释器"""
    print("小奈语言交互式解释器")
    print("输入 '退出' 或 'exit' 退出")
    print("=" * 50)
    
    interpreter = Interpreter()
    
    while True:
        try:
            # 读取多行输入
            lines = []
            prompt = ">>> "
            
            while True:
                try:
                    line = input(prompt)
                except EOFError:
                    print("\n退出")
                    return
                
                # 检查退出命令
                if line.strip().lower() in ['退出', 'exit', 'quit']:
                    print("再见！")
                    return
                
                # 检查是否继续输入
                if line.strip().endswith('\\'):
                    lines.append(line.rstrip('\\'))
                    prompt = "... "
                    continue
                
                lines.append(line)
                break
            
            # 组合输入
            source = '\n'.join(lines)
            
            if not source.strip():
                continue
            
            # 执行代码
            try:
                result = run(source)
                if result is not None:
                    print(f"=> {result}")
            except Exception as e:
                print(f"错误: {e}")
        
        except KeyboardInterrupt:
            print("\n中断")
            continue
        except Exception as e:
            print(f"错误: {e}")
            continue

def show_tokens(source: str):
    """显示词法分析结果"""
    print("词法分析结果:")
    print("=" * 50)
    
    try:
        tokens = lex(source)
        for i, token in enumerate(tokens):
            print(f"{i+1:3d}: {token}")
    except Exception as e:
        print(f"词法错误: {e}")

def show_ast(source: str):
    """显示语法分析结果"""
    print("语法分析结果:")
    print("=" * 50)
    
    try:
        tokens = lex(source)
        program = parse(tokens)
        
        # 简单的AST打印
        def print_ast(node, indent=0):
            prefix = "  " * indent
            if hasattr(node, '__dict__'):
                print(f"{prefix}{node.__class__.__name__}:")
                for key, value in node.__dict__.items():
                    if isinstance(value, list):
                        print(f"{prefix}  {key}: [")
                        for item in value:
                            if hasattr(item, '__dict__'):
                                print_ast(item, indent + 2)
                            else:
                                print(f"{prefix}    {item!r}")
                        print(f"{prefix}  ]")
                    elif hasattr(value, '__dict__'):
                        print(f"{prefix}  {key}:")
                        print_ast(value, indent + 2)
                    else:
                        print(f"{prefix}  {key}: {value!r}")
            else:
                print(f"{prefix}{node!r}")
        
        print_ast(program)
        
    except Exception as e:
        print(f"语法错误: {e}")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="小奈语言解释器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s hello.xn           # 运行hello.xn文件
  %(prog)s -i                 # 启动交互式解释器
  %(prog)s --tokens hello.xn  # 显示词法分析结果
  %(prog)s --ast hello.xn     # 显示语法分析结果
        """
    )
    
    parser.add_argument(
        'file',
        nargs='?',
        help='要运行的小奈语言文件'
    )
    
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='启动交互式解释器'
    )
    
    parser.add_argument(
        '--tokens',
        action='store_true',
        help='显示词法分析结果'
    )
    
    parser.add_argument(
        '--ast',
        action='store_true',
        help='显示语法分析结果'
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='小奈语言 v1.0.0'
    )
    
    args = parser.parse_args()
    
    # 检查参数
    if args.interactive:
        interactive_mode()
    elif args.file:
        if args.tokens:
            with open(args.file, 'r', encoding='utf-8') as f:
                source = f.read()
            show_tokens(source)
        elif args.ast:
            with open(args.file, 'r', encoding='utf-8') as f:
                source = f.read()
            show_ast(source)
        else:
            run_file(args.file)
    else:
        # 如果没有参数，启动交互式解释器
        interactive_mode()

if __name__ == '__main__':
    main()