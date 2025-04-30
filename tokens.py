class Location:
    def __init__(self, line_number: int, col: int, source_code_path: str, line: str):
        self.line_number = line_number
        self.col = col
        self.source_code_path = source_code_path
        self.line = line

    def __str__(self) -> str:
        return f"Line number: {self.line_number}\nCol: {self.col}\nSource code path: {self.source_code_path}\nLine: {self.line}"
    
KEYWORDS = ["print"]

class TokenKind:
    NUM = "number"
    IDENT = "identifier"
    KEYWORD = "keyword"
    
    NUM_ANNOT = "number annotation"

    EQUALS = "equals to"
    SEMICOLON = "semicolon"

class Token:
    def __init__(self, kind: TokenKind, value: str, location: Location):
        self.kind = kind
        self.value = value
        self.location = location
    
    def __str__(self) -> str:
        return f"==== Token =========\nKind: {self.kind}\nValue: {self.value}\n==== Location ======\n{str(self.location)}\n===================="