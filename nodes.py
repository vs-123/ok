from tokens import Location, TokenKind


class Node:
    pass

class VarDecl(Node):
    def __init__(self, type: TokenKind, var_name: str, value: str, location: Location):
        self.type = type
        self.var_name = var_name
        self.value = value
        self.location = location
    
    def __str__(self) -> str:
        return f"Variable Declaration\n====================\nType: {self.type}\nName: {self.var_name}\nValue: {self.value}\n========\nLocation\n========\n{self.location}\n"
    
class PrintStmt(Node):
    def __init__(self, type: TokenKind, value: str, location: Location):
        self.type = type
        self.value = value
        self.location = location
    
    def __str__(self) -> str:
        return f"Print\n=====\nType: {self.type}\nValue: {self.value}\n========\nLocation\n========\n{self.location}\n"