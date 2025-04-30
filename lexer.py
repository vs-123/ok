from typing import List
from tokens import KEYWORDS, Location, Token, TokenKind

class Lexer:
    def __init__(self, source_code_path: str):
        source_code = ""
        try:
            with open(source_code_path, "r") as input_file:
                source_code = input_file.read()
        except Exception as error:
            print(f"[Error] Could not open/read file `{source_code_path}`")
            print(f"[Reason] {error.args[1]}")
            exit(1)

        self.source_code = source_code
        self.output_tokens: List[Token] = []

        self.source_code_path = source_code_path
        self.current_char_index = 0
        self.current_line_number = 1
        self.current_col = 1

    def lex(self):
        while self.current_char_index < len(self.source_code):
            match self.__current_char():
                case " "|"\r"|"\n":
                    pass
                
                case "#":
                    self.__push(Token(
                        TokenKind.NUM_ANNOT, self.__current_char(),
                        Location(
                            self.current_line_number,
                            self.current_col,
                            self.source_code_path,
                            self.__current_line(),
                        )
                    ))

                case "=":
                    self.__push(Token(
                        TokenKind.EQUALS, self.__current_char(),
                        Location(
                            self.current_line_number,
                            self.current_col,
                            self.source_code_path,
                            self.__current_line(),
                        )
                    ))
                
                case ";":
                    self.__push(Token(
                        TokenKind.SEMICOLON, self.__current_char(),
                        Location(
                            self.current_line_number,
                            self.current_col,
                            self.source_code_path,
                            self.__current_line(),
                        )
                    ))
                
                case char if char.isalpha():
                    eaten_identifier = ""
                    while self.__current_char().isalnum():
                        eaten_identifier += self.__current_char()
                        if self.__is_last_char():
                            break
                        self.__advance()

                    self.current_char_index -= 1

                    token_kind = TokenKind.IDENT
                    
                    if eaten_identifier in KEYWORDS:
                        token_kind = TokenKind.KEYWORD

                    self.__push(Token(
                        token_kind, eaten_identifier,
                        Location(
                            self.current_line_number,
                            self.current_col,
                            self.source_code_path,
                            self.__current_line(),
                        )
                    ))

                case char if char.isnumeric():
                    eaten_identifier = ""
                    while self.__current_char().isnumeric():
                        eaten_identifier += self.__current_char()
                        if self.__is_last_char():
                            break
                        self.__advance()

                    self.current_char_index -= 1

                    self.__push(Token(
                        TokenKind.NUM, eaten_identifier,
                        Location(
                            self.current_line_number,
                            self.current_col,
                            self.source_code_path,
                            self.__current_line(),
                        )
                    ))
                
                case other:
                    self.__throw_err(f"Unknown character '{other}'")
                    pass

            if self.__is_last_char():
                break
            self.__advance()
    
    def __current_char(self) -> str:
        return self.source_code[self.current_char_index]

    def __current_line(self) -> str:
        return self.source_code.splitlines()[self.current_line_number-1]

    def __is_last_char(self) -> bool:
        return self.current_char_index == len(self.source_code)-1
            
    def __advance(self):
        self.current_char_index += 1
        self.current_col += 1
        if self.__current_char() == '\n':
            self.current_line_number += 1
            self.current_col = 1

    def __push(self, token: Token):
        self.output_tokens.append(token)
    
    def __throw_err(self, msg: str):
        print(f"[Error] {msg}")
        print(f"[Location] {self.source_code_path}:{self.current_line_number}:{self.current_col}")
        print("[Code]")
        print(f" {self.current_line_number} | {self.__current_line()}")
        exit(1)