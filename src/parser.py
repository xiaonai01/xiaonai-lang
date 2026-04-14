#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语法分析器
将词法单元流转换成抽象语法树
"""
from typing import List, Optional
from .tokens import Token, TokenType
from .ast import *

class ParserError(Exception):
    """语法分析错误"""
    def __init__(self, message: str, token: Token):
        self.message = message
        self.token = token
        super().__init__(f"语法错误 第{token.line}行第{token.column}列: {message}")

class Parser:
    """语法分析器"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0] if tokens else None
    
    def error(self, message: str):
        """抛出语法错误"""
        raise ParserError(message, self.current_token)
    
    def peek(self, offset: int = 0) -> Optional[Token]:
        """查看词法单元，不移动位置"""
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return None
    
    def advance(self) -> Token:
        """前进一个词法单元"""
        token = self.current_token
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None
        return token
    
    def expect(self, token_type: TokenType) -> Token:
        """期望特定类型的词法单元"""
        if self.current_token.type != token_type:
            self.error(f"期望 {token_type}，但得到 {self.current_token.type}")
        return self.advance()
    
    def skip_newlines(self):
        """跳过换行符"""
        while self.current_token and self.current_token.type == TokenType.NEWLINE:
            self.advance()
    
    def parse(self) -> Program:
        """解析整个程序"""
        statements = []
        self.skip_newlines()
        
        while self.current_token and self.current_token.type != TokenType.EOF:
            if self.current_token.type == TokenType.NEWLINE:
                self.advance()
                continue
            
            statement = self.parse_statement()
            if statement:
                statements.append(statement)
            
            self.skip_newlines()
        
        return Program(statements)
    
    def parse_statement(self) -> Optional[ASTNode]:
        """解析语句"""
        if not self.current_token:
            return None
        
        # 变量声明
        if self.current_token.type == TokenType.VAR:
            return self.parse_variable_declaration()
        
        # 赋值语句
        if self.current_token.type == TokenType.IDENTIFIER:
            next_token = self.peek(1)
            if next_token and next_token.type == TokenType.ASSIGN:
                return self.parse_assignment()
        
        # if语句
        if self.current_token.type == TokenType.IF:
            return self.parse_if_statement()
        
        # while循环
        if self.current_token.type == TokenType.WHILE:
            return self.parse_while_statement()
        
        # for循环
        if self.current_token.type == TokenType.FOR:
            return self.parse_for_statement()
        
        # 函数定义
        if self.current_token.type == TokenType.FUNCTION:
            return self.parse_function_definition()
        
        # 返回语句
        if self.current_token.type == TokenType.RETURN:
            return self.parse_return_statement()
        
        # 打印语句
        if self.current_token.type == TokenType.PRINT:
            return self.parse_print_statement()
        
        # 表达式语句
        return self.parse_expression_statement()
    
    def parse_variable_declaration(self) -> VariableDeclaration:
        """解析变量声明"""
        self.expect(TokenType.VAR)
        name_token = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.ASSIGN)
        value = self.parse_expression()
        return VariableDeclaration(name_token.value, value)
    
    def parse_assignment(self) -> Assignment:
        """解析赋值语句"""
        name_token = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.ASSIGN)
        value = self.parse_expression()
        return Assignment(name_token.value, value)
    
    def parse_if_statement(self) -> IfStatement:
        """解析if语句"""
        self.expect(TokenType.IF)
        condition = self.parse_expression()
        self.skip_newlines()
        
        # 解析then分支
        then_body = []
        while (self.current_token and 
               self.current_token.type not in [TokenType.ELSE, TokenType.END, TokenType.EOF]):
            if self.current_token.type == TokenType.NEWLINE:
                self.advance()
                continue
            
            statement = self.parse_statement()
            if statement:
                then_body.append(statement)
            
            self.skip_newlines()
        
        # 解析else分支
        else_body = None
        if self.current_token and self.current_token.type == TokenType.ELSE:
            self.advance()
            self.skip_newlines()
            
            else_body = []
            while (self.current_token and 
                   self.current_token.type not in [TokenType.END, TokenType.EOF]):
                if self.current_token.type == TokenType.NEWLINE:
                    self.advance()
                    continue
                
                statement = self.parse_statement()
                if statement:
                    else_body.append(statement)
                
                self.skip_newlines()
        
        self.expect(TokenType.END)
        return IfStatement(condition, then_body, else_body)
    
    def parse_while_statement(self) -> WhileStatement:
        """解析while循环"""
        self.expect(TokenType.WHILE)
        condition = self.parse_expression()
        self.skip_newlines()
        
        body = []
        while (self.current_token and 
               self.current_token.type not in [TokenType.END, TokenType.EOF]):
            if self.current_token.type == TokenType.NEWLINE:
                self.advance()
                continue
            
            statement = self.parse_statement()
            if statement:
                body.append(statement)
            
            self.skip_newlines()
        
        self.expect(TokenType.END)
        return WhileStatement(condition, body)
    
    def parse_for_statement(self) -> ForStatement:
        """解析for循环"""
        self.expect(TokenType.FOR)
        variable_token = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.ASSIGN)
        iterable = self.parse_expression()
        self.skip_newlines()
        
        body = []
        while (self.current_token and 
               self.current_token.type not in [TokenType.END, TokenType.EOF]):
            if self.current_token.type == TokenType.NEWLINE:
                self.advance()
                continue
            
            statement = self.parse_statement()
            if statement:
                body.append(statement)
            
            self.skip_newlines()
        
        self.expect(TokenType.END)
        return ForStatement(variable_token.value, iterable, body)
    
    def parse_function_definition(self) -> FunctionDefinition:
        """解析函数定义"""
        self.expect(TokenType.FUNCTION)
        name_token = self.expect(TokenType.IDENTIFIER)
        
        # 解析参数列表
        self.expect(TokenType.LPAREN)
        parameters = []
        
        if self.current_token.type != TokenType.RPAREN:
            param_token = self.expect(TokenType.IDENTIFIER)
            parameters.append(param_token.value)
            
            while self.current_token.type == TokenType.COMMA:
                self.advance()
                param_token = self.expect(TokenType.IDENTIFIER)
                parameters.append(param_token.value)
        
        self.expect(TokenType.RPAREN)
        self.skip_newlines()
        
        # 解析函数体
        body = []
        while (self.current_token and 
               self.current_token.type not in [TokenType.END, TokenType.EOF]):
            if self.current_token.type == TokenType.NEWLINE:
                self.advance()
                continue
            
            statement = self.parse_statement()
            if statement:
                body.append(statement)
            
            self.skip_newlines()
        
        self.expect(TokenType.END)
        return FunctionDefinition(name_token.value, parameters, body)
    
    def parse_return_statement(self) -> ReturnStatement:
        """解析返回语句"""
        self.expect(TokenType.RETURN)
        
        value = None
        if (self.current_token and 
            self.current_token.type not in [TokenType.NEWLINE, TokenType.EOF]):
            value = self.parse_expression()
        
        return ReturnStatement(value)
    
    def parse_print_statement(self) -> PrintStatement:
        """解析打印语句"""
        self.expect(TokenType.PRINT)
        self.expect(TokenType.LPAREN)
        
        arguments = []
        if self.current_token.type != TokenType.RPAREN:
            arguments.append(self.parse_expression())
            
            while self.current_token.type == TokenType.COMMA:
                self.advance()
                arguments.append(self.parse_expression())
        
        self.expect(TokenType.RPAREN)
        return PrintStatement(arguments)
    
    def parse_expression_statement(self) -> ASTNode:
        """解析表达式语句"""
        return self.parse_expression()
    
    def parse_expression(self) -> ASTNode:
        """解析表达式"""
        return self.parse_or()
    
    def parse_or(self) -> ASTNode:
        """解析or表达式"""
        left = self.parse_and()
        
        while self.current_token and self.current_token.type == TokenType.OR:
            operator = self.advance().value
            right = self.parse_and()
            left = BinaryOperation(left, operator, right)
        
        return left
    
    def parse_and(self) -> ASTNode:
        """解析and表达式"""
        left = self.parse_equality()
        
        while self.current_token and self.current_token.type == TokenType.AND:
            operator = self.advance().value
            right = self.parse_equality()
            left = BinaryOperation(left, operator, right)
        
        return left
    
    def parse_equality(self) -> ASTNode:
        """解析等式表达式"""
        left = self.parse_comparison()
        
        while (self.current_token and 
               self.current_token.type in [TokenType.EQUAL, TokenType.NOT_EQUAL]):
            operator = self.advance().value
            right = self.parse_comparison()
            left = BinaryOperation(left, operator, right)
        
        return left
    
    def parse_comparison(self) -> ASTNode:
        """解析比较表达式"""
        left = self.parse_addition()
        
        while (self.current_token and 
               self.current_token.type in [TokenType.LESS, TokenType.GREATER, 
                                          TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL]):
            operator = self.advance().value
            right = self.parse_addition()
            left = BinaryOperation(left, operator, right)
        
        return left
    
    def parse_addition(self) -> ASTNode:
        """解析加减表达式"""
        left = self.parse_multiplication()
        
        while (self.current_token and 
               self.current_token.type in [TokenType.PLUS, TokenType.MINUS]):
            operator = self.advance().value
            right = self.parse_multiplication()
            left = BinaryOperation(left, operator, right)
        
        return left
    
    def parse_multiplication(self) -> ASTNode:
        """解析乘除表达式"""
        left = self.parse_unary()
        
        while (self.current_token and 
               self.current_token.type in [TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO]):
            operator = self.advance().value
            right = self.parse_unary()
            left = BinaryOperation(left, operator, right)
        
        return left
    
    def parse_unary(self) -> ASTNode:
        """解析一元表达式"""
        if (self.current_token and 
            self.current_token.type in [TokenType.MINUS, TokenType.NOT]):
            operator = self.advance().value
            operand = self.parse_unary()
            return UnaryOperation(operator, operand)
        
        return self.parse_primary()
    
    def parse_primary(self) -> ASTNode:
        """解析基本表达式"""
        if not self.current_token:
            self.error("意外的文件结束")
        
        # 数字
        if self.current_token.type == TokenType.NUMBER:
            token = self.advance()
            return NumberLiteral(token.value)
        
        # 浮点数
        if self.current_token.type == TokenType.FLOAT:
            token = self.advance()
            return NumberLiteral(token.value)
        
        # 字符串
        if self.current_token.type == TokenType.STRING:
            token = self.advance()
            return StringLiteral(token.value)
        
        # 布尔值
        if self.current_token.type == TokenType.BOOLEAN:
            token = self.advance()
            return BooleanLiteral(token.value)
        
        # 空值
        if self.current_token.type == TokenType.NULL:
            self.advance()
            return NullLiteral()
        
        # 标识符或函数调用
        if self.current_token.type == TokenType.IDENTIFIER:
            name_token = self.advance()
            
            # 检查是否是函数调用
            if self.current_token and self.current_token.type == TokenType.LPAREN:
                return self.parse_function_call(name_token.value)
            
            return Identifier(name_token.value)
        
        # 输入表达式
        if self.current_token.type == TokenType.INPUT:
            return self.parse_input_expression()
        
        # 括号表达式
        if self.current_token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        
        self.error(f"意外的词法单元: {self.current_token.type}")
    
    def parse_function_call(self, name: str) -> FunctionCall:
        """解析函数调用"""
        self.expect(TokenType.LPAREN)
        
        arguments = []
        if self.current_token.type != TokenType.RPAREN:
            arguments.append(self.parse_expression())
            
            while self.current_token.type == TokenType.COMMA:
                self.advance()
                arguments.append(self.parse_expression())
        
        self.expect(TokenType.RPAREN)
        return FunctionCall(name, arguments)
    
    def parse_input_expression(self) -> InputExpression:
        """解析输入表达式"""
        self.expect(TokenType.INPUT)
        self.expect(TokenType.LPAREN)
        
        prompt = None
        if self.current_token.type != TokenType.RPAREN:
            prompt = self.parse_expression()
        
        self.expect(TokenType.RPAREN)
        return InputExpression(prompt)

def parse(tokens: List[Token]) -> Program:
    """语法分析的便捷函数"""
    parser = Parser(tokens)
    return parser.parse()