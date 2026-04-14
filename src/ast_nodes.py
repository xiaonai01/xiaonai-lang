#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抽象语法树定义
定义小奈语言的所有语法结构
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, List, Optional, Union

class ASTNode(ABC):
    """抽象语法树节点基类"""
    
    @abstractmethod
    def accept(self, visitor):
        """接受访问者"""
        pass

@dataclass
class NumberLiteral(ASTNode):
    """数字字面量"""
    value: Union[int, float]
    
    def accept(self, visitor):
        return visitor.visit_number_literal(self)

@dataclass
class StringLiteral(ASTNode):
    """字符串字面量"""
    value: str
    
    def accept(self, visitor):
        return visitor.visit_string_literal(self)

@dataclass
class BooleanLiteral(ASTNode):
    """布尔字面量"""
    value: bool
    
    def accept(self, visitor):
        return visitor.visit_boolean_literal(self)

@dataclass
class NullLiteral(ASTNode):
    """空值字面量"""
    
    def accept(self, visitor):
        return visitor.visit_null_literal(self)

@dataclass
class Identifier(ASTNode):
    """标识符"""
    name: str
    
    def accept(self, visitor):
        return visitor.visit_identifier(self)

@dataclass
class BinaryOperation(ASTNode):
    """二元运算"""
    left: ASTNode
    operator: str
    right: ASTNode
    
    def accept(self, visitor):
        return visitor.visit_binary_operation(self)

@dataclass
class UnaryOperation(ASTNode):
    """一元运算"""
    operator: str
    operand: ASTNode
    
    def accept(self, visitor):
        return visitor.visit_unary_operation(self)

@dataclass
class FunctionCall(ASTNode):
    """函数调用"""
    name: str
    arguments: List[ASTNode]
    
    def accept(self, visitor):
        return visitor.visit_function_call(self)

@dataclass
class VariableDeclaration(ASTNode):
    """变量声明"""
    name: str
    value: ASTNode
    
    def accept(self, visitor):
        return visitor.visit_variable_declaration(self)

@dataclass
class Assignment(ASTNode):
    """赋值语句"""
    name: str
    value: ASTNode
    
    def accept(self, visitor):
        return visitor.visit_assignment(self)

@dataclass
class IfStatement(ASTNode):
    """if语句"""
    condition: ASTNode
    then_body: List[ASTNode]
    else_body: Optional[List[ASTNode]] = None
    
    def accept(self, visitor):
        return visitor.visit_if_statement(self)

@dataclass
class WhileStatement(ASTNode):
    """while循环"""
    condition: ASTNode
    body: List[ASTNode]
    
    def accept(self, visitor):
        return visitor.visit_while_statement(self)

@dataclass
class ForStatement(ASTNode):
    """for循环"""
    variable: str
    iterable: ASTNode
    body: List[ASTNode]
    
    def accept(self, visitor):
        return visitor.visit_for_statement(self)

@dataclass
class FunctionDefinition(ASTNode):
    """函数定义"""
    name: str
    parameters: List[str]
    body: List[ASTNode]
    
    def accept(self, visitor):
        return visitor.visit_function_definition(self)

@dataclass
class ReturnStatement(ASTNode):
    """返回语句"""
    value: Optional[ASTNode] = None
    
    def accept(self, visitor):
        return visitor.visit_return_statement(self)

@dataclass
class PrintStatement(ASTNode):
    """打印语句"""
    arguments: List[ASTNode]
    
    def accept(self, visitor):
        return visitor.visit_print_statement(self)

@dataclass
class InputExpression(ASTNode):
    """输入表达式"""
    prompt: Optional[ASTNode] = None
    
    def accept(self, visitor):
        return visitor.visit_input_expression(self)

@dataclass
class Program(ASTNode):
    """程序"""
    statements: List[ASTNode]
    
    def accept(self, visitor):
        return visitor.visit_program(self)

class ASTVisitor(ABC):
    """AST访问者基类"""
    
    @abstractmethod
    def visit_number_literal(self, node: NumberLiteral):
        pass
    
    @abstractmethod
    def visit_string_literal(self, node: StringLiteral):
        pass
    
    @abstractmethod
    def visit_boolean_literal(self, node: BooleanLiteral):
        pass
    
    @abstractmethod
    def visit_null_literal(self, node: NullLiteral):
        pass
    
    @abstractmethod
    def visit_identifier(self, node: Identifier):
        pass
    
    @abstractmethod
    def visit_binary_operation(self, node: BinaryOperation):
        pass
    
    @abstractmethod
    def visit_unary_operation(self, node: UnaryOperation):
        pass
    
    @abstractmethod
    def visit_function_call(self, node: FunctionCall):
        pass
    
    @abstractmethod
    def visit_variable_declaration(self, node: VariableDeclaration):
        pass
    
    @abstractmethod
    def visit_assignment(self, node: Assignment):
        pass
    
    @abstractmethod
    def visit_if_statement(self, node: IfStatement):
        pass
    
    @abstractmethod
    def visit_while_statement(self, node: WhileStatement):
        pass
    
    @abstractmethod
    def visit_for_statement(self, node: ForStatement):
        pass
    
    @abstractmethod
    def visit_function_definition(self, node: FunctionDefinition):
        pass
    
    @abstractmethod
    def visit_return_statement(self, node: ReturnStatement):
        pass
    
    @abstractmethod
    def visit_print_statement(self, node: PrintStatement):
        pass
    
    @abstractmethod
    def visit_input_expression(self, node: InputExpression):
        pass
    
    @abstractmethod
    def visit_program(self, node: Program):
        pass