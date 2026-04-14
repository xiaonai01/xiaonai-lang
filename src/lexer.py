#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
词法分析器
将源代码分解成词法单元
"""
from typing import List, Optional
from tokens import Token, TokenType, KEYWORDS, OPERATORS, DELIMITERS

class LexerError(Exception):
    """词法分析错误"""
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"词法错误 第{line}行第{column}列: {message}")

class Lexer:
    """词法分析器"""
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    def error(self, message: str):
        """抛出词法错误"""
        raise LexerError(message, self.line, self.column)
    
    def peek(self, offset: int = 0) -> Optional[str]:
        """查看字符，不移动位置"""
        pos = self.pos + offset
        if pos < len(self.source):
            return self.source[pos]
        return None
    
    def advance(self) -> str:
        """前进一个字符"""
        char = self.source[self.pos]
        self.pos += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char
    
    def skip_whitespace(self):
        """跳过空白字符"""
        while self.pos < len(self.source) and self.source[self.pos] in ' \t\r':
            self.advance()
    
    def skip_comment(self):
        """跳过注释"""
        if self.peek() == '#':
            while self.pos < len(self.source) and self.source[self.pos] != '\n':
                self.advance()
    
    def read_number(self) -> Token:
        """读取数字"""
        start_line = self.line
        start_column = self.column
        result = []
        has_dot = False
        
        while self.pos < len(self.source) and (self.source[self.pos].isdigit() or self.source[self.pos] == '.'):
            if self.source[self.pos] == '.':
                if has_dot:
                    self.error("数字中不能有两个小数点")
                has_dot = True
            result.append(self.advance())
        
        number_str = ''.join(result)
        if has_dot:
            return Token(TokenType.FLOAT, float(number_str), start_line, start_column)
        else:
            return Token(TokenType.NUMBER, int(number_str), start_line, start_column)
    
    def read_string(self) -> Token:
        """读取字符串"""
        start_line = self.line
        start_column = self.column
        quote_char = self.advance()  # 跳过开始的引号
        result = []
        
        while self.pos < len(self.source) and self.source[self.pos] != quote_char:
            if self.source[self.pos] == '\\':
                # 处理转义字符
                self.advance()
                if self.pos >= len(self.source):
                    self.error("字符串未结束")
                
                escape_char = self.advance()
                if escape_char == 'n':
                    result.append('\n')
                elif escape_char == 't':
                    result.append('\t')
                elif escape_char == '\\':
                    result.append('\\')
                elif escape_char == quote_char:
                    result.append(quote_char)
                else:
                    self.error(f"未知的转义字符: \\{escape_char}")
            else:
                result.append(self.advance())
        
        if self.pos >= len(self.source):
            self.error("字符串未结束")
        
        self.advance()  # 跳过结束的引号
        return Token(TokenType.STRING, ''.join(result), start_line, start_column)
    
    def read_identifier(self) -> Token:
        """读取标识符或关键字"""
        start_line = self.line
        start_column = self.column
        result = []
        
        while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
            result.append(self.advance())
        
        identifier = ''.join(result)
        
        # 检查是否是关键字
        if identifier in KEYWORDS:
            return Token(KEYWORDS[identifier], identifier, start_line, start_column)
        
        # 检查是否是布尔值
        if identifier.lower() in ['true', '真']:
            return Token(TokenType.BOOLEAN, True, start_line, start_column)
        if identifier.lower() in ['false', '假']:
            return Token(TokenType.BOOLEAN, False, start_line, start_column)
        
        # 检查是否是null
        if identifier.lower() in ['null', '空']:
            return Token(TokenType.NULL, None, start_line, start_column)
        
        return Token(TokenType.IDENTIFIER, identifier, start_line, start_column)
    
    def tokenize(self) -> List[Token]:
        """进行词法分析"""
        while self.pos < len(self.source):
            # 跳过空白字符
            self.skip_whitespace()
            
            if self.pos >= len(self.source):
                break
            
            char = self.source[self.pos]
            
            # 处理换行
            if char == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, '\\n', self.line, self.column))
                self.advance()
                continue
            
            # 处理注释
            if char == '#':
                self.skip_comment()
                continue
            
            # 处理数字
            if char.isdigit():
                self.tokens.append(self.read_number())
                continue
            
            # 处理字符串
            if char in ['"', "'"]:
                self.tokens.append(self.read_string())
                continue
            
            # 处理标识符和关键字
            if char.isalpha() or char == '_':
                self.tokens.append(self.read_identifier())
                continue
            
            # 处理运算符
            if char in OPERATORS:
                start_line = self.line
                start_column = self.column
                
                # 检查双字符运算符
                if self.pos + 1 < len(self.source):
                    two_char = char + self.source[self.pos + 1]
                    if two_char in OPERATORS:
                        self.advance()
                        self.advance()
                        self.tokens.append(Token(OPERATORS[two_char], two_char, start_line, start_column))
                        continue
                
                # 单字符运算符
                self.advance()
                self.tokens.append(Token(OPERATORS[char], char, start_line, start_column))
                continue
            
            # 处理分隔符
            if char in DELIMITERS:
                start_line = self.line
                start_column = self.column
                self.advance()
                self.tokens.append(Token(DELIMITERS[char], char, start_line, start_column))
                continue
            
            # 未知字符
            self.error(f"未知字符: {char}")
        
        # 添加EOF标记
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens

def lex(source: str) -> List[Token]:
    """词法分析的便捷函数"""
    lexer = Lexer(source)
    return lexer.tokenize()