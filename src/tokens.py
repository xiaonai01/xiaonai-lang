#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
词法单元定义
定义小奈语言的所有词法单元类型
"""
from enum import Enum, auto
from dataclasses import dataclass
from typing import Any

class TokenType(Enum):
    """词法单元类型"""
    # 字面量
    NUMBER = auto()      # 数字
    FLOAT = auto()       # 浮点数
    STRING = auto()      # 字符串
    BOOLEAN = auto()     # 布尔值
    NULL = auto()        # 空值
    
    # 标识符
    IDENTIFIER = auto()  # 标识符
    
    # 关键字
    VAR = auto()         # 变量
    IF = auto()          # 如果
    ELSE = auto()        # 否则
    WHILE = auto()       # 当
    FOR = auto()         # 对于
    FUNCTION = auto()    # 函数
    RETURN = auto()      # 返回
    PRINT = auto()       # 打印
    INPUT = auto()       # 输入
    TRUE = auto()        # 真
    FALSE = auto()       # 假
    AND = auto()         # 与
    OR = auto()          # 或
    NOT = auto()         # 非
    END = auto()         # 结束
    THEN = auto()        # 那么
    DO = auto()          # 做
    
    # 运算符
    PLUS = auto()        # +
    MINUS = auto()       # -
    MULTIPLY = auto()    # *
    DIVIDE = auto()      # /
    MODULO = auto()      # %
    ASSIGN = auto()      # =
    EQUAL = auto()       # ==
    NOT_EQUAL = auto()   # !=
    LESS = auto()        # <
    GREATER = auto()     # >
    LESS_EQUAL = auto()  # <=
    GREATER_EQUAL = auto() # >=
    BANG = auto()        # !
    
    # 分隔符
    LPAREN = auto()      # (
    RPAREN = auto()      # )
    LBRACKET = auto()    # [
    RBRACKET = auto()    # ]
    LBRACE = auto()      # {
    RBRACE = auto()      # }
    COMMA = auto()       # ,
    DOT = auto()         # .
    COLON = auto()       # :
    SEMICOLON = auto()   # ;
    
    # 特殊
    NEWLINE = auto()     # 换行
    EOF = auto()         # 文件结束
    
    # 注释
    COMMENT = auto()     # 注释

@dataclass
class Token:
    """词法单元"""
    type: TokenType
    value: Any
    line: int
    column: int
    
    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, line={self.line}, col={self.column})"

# 关键字映射
KEYWORDS = {
    '变量': TokenType.VAR,
    '如果': TokenType.IF,
    '否则': TokenType.ELSE,
    '当': TokenType.WHILE,
    '对于': TokenType.FOR,
    '函数': TokenType.FUNCTION,
    '返回': TokenType.RETURN,
    '打印': TokenType.PRINT,
    '输入': TokenType.INPUT,
    '真': TokenType.TRUE,
    '假': TokenType.FALSE,
    '与': TokenType.AND,
    '或': TokenType.OR,
    '非': TokenType.NOT,
    '结束': TokenType.END,
    '那么': TokenType.THEN,
    '做': TokenType.DO,
}

# 运算符映射
OPERATORS = {
    '+': TokenType.PLUS,
    '-': TokenType.MINUS,
    '*': TokenType.MULTIPLY,
    '/': TokenType.DIVIDE,
    '%': TokenType.MODULO,
    '=': TokenType.ASSIGN,
    '==': TokenType.EQUAL,
    '!=': TokenType.NOT_EQUAL,
    '<': TokenType.LESS,
    '>': TokenType.GREATER,
    '<=': TokenType.LESS_EQUAL,
    '>=': TokenType.GREATER_EQUAL,
    '!': TokenType.BANG,
}

# 分隔符映射
DELIMITERS = {
    '(': TokenType.LPAREN,
    ')': TokenType.RPAREN,
    '[': TokenType.LBRACKET,
    ']': TokenType.RBRACKET,
    '{': TokenType.LBRACE,
    '}': TokenType.RBRACE,
    ',': TokenType.COMMA,
    '.': TokenType.DOT,
    ':': TokenType.COLON,
    ';': TokenType.SEMICOLON,
}