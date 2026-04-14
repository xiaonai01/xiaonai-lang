#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解释器
执行抽象语法树
"""
from typing import Any, Dict, List, Optional
from ast_nodes import *
from tokens import TokenType

class ReturnException(Exception):
    """返回语句异常"""
    def __init__(self, value: Any):
        self.value = value

class Environment:
    """环境（作用域）"""
    
    def __init__(self, parent: Optional['Environment'] = None):
        self.variables: Dict[str, Any] = {}
        self.parent = parent
    
    def get(self, name: str) -> Any:
        """获取变量值"""
        if name in self.variables:
            return self.variables[name]
        
        if self.parent:
            return self.parent.get(name)
        
        raise NameError(f"变量 '{name}' 未定义")
    
    def set(self, name: str, value: Any):
        """设置变量值"""
        # 如果变量在当前环境中存在，直接设置
        if name in self.variables:
            self.variables[name] = value
            return
        
        # 如果变量在父环境中存在，递归设置
        if self.parent:
            self.parent.set(name, value)
            return
        
        # 如果变量不存在，创建新变量
        self.variables[name] = value
    
    def define(self, name: str, value: Any):
        """定义变量"""
        self.variables[name] = value

class Function:
    """函数对象"""
    
    def __init__(self, name: str, parameters: List[str], body: List[ASTNode], closure: Environment):
        self.name = name
        self.parameters = parameters
        self.body = body
        self.closure = closure
    
    def __call__(self, interpreter: 'Interpreter', arguments: List[Any]) -> Any:
        """调用函数"""
        # 创建新的环境
        env = Environment(self.closure)
        
        # 绑定参数
        if len(arguments) != len(self.parameters):
            raise TypeError(f"函数 '{self.name}' 需要 {len(self.parameters)} 个参数，但得到了 {len(arguments)} 个")
        
        for param, arg in zip(self.parameters, arguments):
            env.define(param, arg)
        
        # 执行函数体
        try:
            interpreter.execute_block(self.body, env)
        except ReturnException as e:
            return e.value
        
        return None

class Interpreter(ASTVisitor):
    """解释器"""
    
    def __init__(self):
        self.global_env = Environment()
        self.current_env = self.global_env
        self.setup_builtins()
    
    def setup_builtins(self):
        """设置内置函数"""
        # 内置函数
        def builtin_len(interpreter, args):
            if len(args) != 1:
                raise TypeError("len() 需要 1 个参数")
            return len(args[0])
        
        def builtin_str(interpreter, args):
            if len(args) != 1:
                raise TypeError("str() 需要 1 个参数")
            return str(args[0])
        
        def builtin_int(interpreter, args):
            if len(args) != 1:
                raise TypeError("int() 需要 1 个参数")
            try:
                return int(args[0])
            except:
                raise ValueError(f"无法将 '{args[0]}' 转换为整数")
        
        def builtin_float(interpreter, args):
            if len(args) != 1:
                raise TypeError("float() 需要 1 个参数")
            try:
                return float(args[0])
            except:
                raise ValueError(f"无法将 '{args[0]}' 转换为浮点数")
        
        def builtin_type(interpreter, args):
            if len(args) != 1:
                raise TypeError("type() 需要 1 个参数")
            return type(args[0]).__name__
        
        # 注册内置函数
        self.global_env.define("len", builtin_len)
        self.global_env.define("str", builtin_str)
        self.global_env.define("int", builtin_int)
        self.global_env.define("float", builtin_float)
        self.global_env.define("type", builtin_type)
        
        # 内置常量
        self.global_env.define("PI", 3.141592653589793)
        self.global_env.define("E", 2.718281828459045)
    
    def interpret(self, program: Program):
        """解释执行程序"""
        try:
            return self.visit_program(program)
        except ReturnException:
            pass
    
    def execute_block(self, statements: List[ASTNode], env: Environment):
        """执行代码块"""
        previous_env = self.current_env
        self.current_env = env
        
        try:
            for statement in statements:
                self.execute(statement)
        finally:
            self.current_env = previous_env
    
    def execute(self, node: ASTNode):
        """执行语句"""
        return node.accept(self)
    
    def evaluate(self, node: ASTNode) -> Any:
        """求值表达式"""
        return node.accept(self)
    
    def visit_program(self, node: Program):
        """访问程序节点"""
        result = None
        for statement in node.statements:
            result = self.execute(statement)
        return result
    
    def visit_number_literal(self, node: NumberLiteral):
        """访问数字字面量"""
        return node.value
    
    def visit_string_literal(self, node: StringLiteral):
        """访问字符串字面量"""
        return node.value
    
    def visit_boolean_literal(self, node: BooleanLiteral):
        """访问布尔字面量"""
        return node.value
    
    def visit_null_literal(self, node: NullLiteral):
        """访问空值字面量"""
        return None
    
    def visit_identifier(self, node: Identifier):
        """访问标识符"""
        return self.current_env.get(node.name)
    
    def visit_binary_operation(self, node: BinaryOperation):
        """访问二元运算"""
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)
        
        if node.operator == '+':
            # 支持字符串拼接
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            return left + right
        elif node.operator == '-':
            return left - right
        elif node.operator == '*':
            return left * right
        elif node.operator == '/':
            if right == 0:
                raise ZeroDivisionError("除数不能为零")
            return left / right
        elif node.operator == '%':
            if right == 0:
                raise ZeroDivisionError("模数不能为零")
            return left % right
        elif node.operator == '==':
            return left == right
        elif node.operator == '!=':
            return left != right
        elif node.operator == '<':
            return left < right
        elif node.operator == '>':
            return left > right
        elif node.operator == '<=':
            return left <= right
        elif node.operator == '>=':
            return left >= right
        elif node.operator == '与':
            return left and right
        elif node.operator == '或':
            return left or right
        else:
            raise ValueError(f"未知的二元运算符: {node.operator}")
    
    def visit_unary_operation(self, node: UnaryOperation):
        """访问一元运算"""
        operand = self.evaluate(node.operand)
        
        if node.operator == '-':
            return -operand
        elif node.operator == '非':
            return not operand
        else:
            raise ValueError(f"未知的一元运算符: {node.operator}")
    
    def visit_function_call(self, node: FunctionCall):
        """访问函数调用"""
        # 获取函数
        try:
            func = self.current_env.get(node.name)
        except NameError:
            raise NameError(f"函数 '{node.name}' 未定义")
        
        # 求值参数
        args = [self.evaluate(arg) for arg in node.arguments]
        
        # 调用函数
        if callable(func):
            return func(self, args)
        else:
            raise TypeError(f"'{node.name}' 不是函数")
    
    def visit_variable_declaration(self, node: VariableDeclaration):
        """访问变量声明"""
        value = self.evaluate(node.value)
        self.current_env.define(node.name, value)
        return value
    
    def visit_assignment(self, node: Assignment):
        """访问赋值语句"""
        value = self.evaluate(node.value)
        self.current_env.set(node.name, value)
        return value
    
    def visit_if_statement(self: 'Interpreter', node: IfStatement):
        """访问if语句"""
        condition = self.evaluate(node.condition)
        
        if condition:
            self.execute_block(node.then_body, Environment(self.current_env))
        elif node.else_body:
            self.execute_block(node.else_body, Environment(self.current_env))
        
        return None
    
    def visit_while_statement(self: 'Interpreter', node: WhileStatement):
        """访问while循环"""
        while self.evaluate(node.condition):
            self.execute_block(node.body, Environment(self.current_env))
        
        return None
    
    def visit_for_statement(self: 'Interpreter', node: ForStatement):
        """访问for循环"""
        iterable = self.evaluate(node.iterable)
        
        if not hasattr(iterable, '__iter__'):
            raise TypeError("for循环需要一个可迭代对象")
        
        for item in iterable:
            self.current_env.set(node.variable, item)
            self.execute_block(node.body, Environment(self.current_env))
        
        return None
    
    def visit_function_definition(self: 'Interpreter', node: FunctionDefinition):
        """访问函数定义"""
        func = Function(node.name, node.parameters, node.body, self.current_env)
        self.current_env.define(node.name, func)
        return func
    
    def visit_return_statement(self: 'Interpreter', node: ReturnStatement):
        """访问返回语句"""
        value = None
        if node.value:
            value = self.evaluate(node.value)
        
        raise ReturnException(value)
    
    def visit_print_statement(self: 'Interpreter', node: PrintStatement):
        """访问打印语句"""
        values = [self.evaluate(arg) for arg in node.arguments]
        print(*values)
        return None
    
    def visit_input_expression(self: 'Interpreter', node: InputExpression):
        """访问输入表达式"""
        prompt = ""
        if node.prompt:
            prompt = self.evaluate(node.prompt)
        
        return input(prompt)

def run(source: str):
    """运行小奈语言代码"""
    from lexer import lex
    from parser import parse
    
    # 词法分析
    tokens = lex(source)
    
    # 语法分析
    program = parse(tokens)
    
    # 解释执行
    interpreter = Interpreter()
    return interpreter.interpret(program)