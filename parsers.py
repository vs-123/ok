from typing import List
from contextvars import Token

from nodes import Node, PrintStmt, VarDecl
from tokens import TokenKind

class Parser:
    def __init__(self, input_tokens: List[Token]):
        self.input_tokens = input_tokens
        self.current_token_index = 0
        self.output_nodes: List[Node] = []

    def parse(self):
        while self.current_token_index < len(self.input_tokens):
            match self.__current_token().kind:
                # Numeric variables
                case TokenKind.NUM_ANNOT:
                    var_name = ""
                    value = ""

                    self.__expect(TokenKind.EQUALS)
                    self.__advance()

                    self.__expect(TokenKind.IDENT)
                    self.__advance()

                    var_name = self.__current_token().value

                    self.__expect_either([TokenKind.NUM, TokenKind.IDENT])
                    self.__advance()

                    value = self.__current_token().value

                    self.__expect(TokenKind.SEMICOLON)
                    self.__advance()

                    self.__push(VarDecl(TokenKind.NUM_ANNOT, var_name, value, self.__current_token().location))

                # Keywords
                case TokenKind.KEYWORD:
                    match self.__current_token().value:
                        case "print":
                            self.__expect_either([TokenKind.IDENT, TokenKind.NUM])
                            self.__advance()

                            value = self.__current_token().value

                            self.__expect(TokenKind.SEMICOLON)
                            self.__advance()

                            self.__push(PrintStmt(self.__current_token().kind, value, self.__current_token().location))

                        case other:
                            self.__throw_err(f"Unimplemented keyword `{self.__current_token().value}`")

                case other:
                    self.__throw_err(f"Unimplemented token kind {other} (value: {self.__current_token().value})")

            self.__advance()

    def __advance(self):
        self.current_token_index += 1
    
    def __push(self, node: Node):
        self.output_nodes.append(node)

    def __is_last_token(self) -> bool:
        return self.current_token_index == len(self.input_tokens) - 1

    def __current_token(self) -> Token:
        return self.input_tokens[self.current_token_index]

    def __peek(self) -> Token:
        return self.input_tokens[self.current_token_index+1]
    
    def __expect(self, expected_kind: TokenKind):
        if self.__is_last_token():
            self.__throw_err(f"Expected a(n) {expected_kind} after `{self.__current_token().value}`, but is end of the file")
        
        if self.__peek().kind != expected_kind:
            self.__throw_err(f"Expected a(n) {expected_kind} after `{self.__current_token().value}`, but found `{self.__peek().value}` which is a(n) {self.__peek().kind}")

    def __expect_either(self, expected_kinds: List[TokenKind]):
        if self.__is_last_token():
            self.__throw_err(f"Expected one of {expected_kinds} after `{self.__current_token().value}`, but is end of the file")
        
        if self.__peek().kind not in expected_kinds:
            self.__throw_err(f"Expected one of {expected_kinds} after `{self.__current_token().value}`, but found `{self.__peek().value}` which is a(n) {self.__peek().kind}")
    
    def __throw_err(self, msg: str):
        location = self.__current_token().location
        print(f"[Error] {msg}")
        print(f"[Location] {location.source_code_path}:{location.line_number}:{location.col}")
        print("[Code]")
        print(f" {location.line_number} | {location.line}")
        exit(1)