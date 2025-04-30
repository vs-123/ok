from typing import List, TypedDict

from nodes import Node, VarDecl, PrintStmt
from tokens import Location, TokenKind

class Interpreter:
    def __init__(self, input_nodes: List[Node]):
        self.input_nodes = input_nodes
        self.current_node_index = 0

        self.stored_variables: dict[str, tuple[TokenKind, str]] = {}

    def interpret(self):
        while self.current_node_index < len(self.input_nodes):
            current_node = self.__current_node()

            if isinstance(current_node, VarDecl):
                self.stored_variables[current_node.var_name] = (current_node.type, current_node.value)
            elif isinstance(current_node, PrintStmt):
                print(self.__value(current_node))

            self.__advance()
        
    def __current_node(self):
        return self.input_nodes[self.current_node_index]

    def __is_last_node(self) -> bool:
        return self.current_node_index == len(self.input_nodes) - 1

    def __advance(self):
        self.current_node_index += 1

    def __value(self, current_node: Node) -> str:
        if current_node.value.isalnum():
            if current_node.value in self.stored_variables:
                return self.stored_variables[current_node.value][1]
            else:
                self.__throw_err(f"Variable `{current_node.value}` does not exist") 
        
        return current_node.value

    def __throw_err(self, msg: str):
        location = self.__current_node().location
        print(f"[Error] {msg}")
        print(f"[Location] {location.source_code_path}:{location.line_number}")
        print("[Code]")
        print(f" {location.line_number} | {location.line}")
        exit(1)