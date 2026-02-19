from enum import IntEnum
from luaparser import ast
from luaparser import astnodes

def parse_premake_file_to_ast(path:str) -> ast.Chunk:
    try:
        with open(path, 'r', encoding='utf-8') as file:
            source = file.read()
            return ast.parse(source)
    except FileNotFoundError:
        print(f"File '{path}' was not found.")
    except Exception as err:
        print(f"An error occurred: {err}")

def convert_lua_table_to_pytable(luatable:astnodes.Table) -> dict:
    if len(luatable.fields) == 0: return []
    
    result = None
    if isinstance(luatable.fields[0].key, astnodes.Number):
        result:list = []
        for field in luatable.fields:
            result.append(field.value.s)

    elif isinstance(luatable.fields[0].key, astnodes.String):
        result:dict = {}
        for field in luatable.fields:
            result[field.key.s] = field.value.s

    return result

# def create_group_object(luagroup)

class PGuiGroup(object):

    def __init__(self, name:str) -> None:
        self.name:str = name
        self.includes:list[str] = []

    def __str__(self) -> str:
        return f"group {self.name}:{self.includes}"

class PGuiWorkspace(object):

    def __init__(self, name:str) -> None:
        self.name:str = name
        self.architecture:str = None
        self.configurations:list[str] = []
        self.startproject:str = None
        self.groups:list[PGuiGroup] = []

    def __str__(self) -> str:
        return f"workspace: {self.name}\n\
        architecture: {self.architecture}\n\
        configurations: {self.configurations}\n\
        startproject: {self.startproject}\n\
        groups: {self.groups}"

class PGuiProject(object):

    def __init__(self, name:str) -> None:
        self.name:str = name
        self.kind:str = None
        self.language:str = None
        self.characterset:str = None
        self.cppdialect:str = None

class PremakeCallContext(object):

    def __init__(self, name:str) -> None:
        self.name = name

class PremakeCallVisitor(ast.ASTVisitor):

    GENERAL_KEYS = {"include"}
    WORKSPACE_KEYS = {"architecture", "configurations", "startproject", "group"}
    PROJECT_KEYS = {"kind", "language", "characterset", "cppdialect"}

    class CallContext(IntEnum):
        GLOBAL = 0
        WORKSPACE = 1
        PROJECT = 2

    def __init__(self) -> None:
        self.includes = []
        self.globals = None
        self.workspace = None
        self.project = None
        self.current_context = self.CallContext.GLOBAL

    def __get_working_ctx(self) -> None:
        work_ctx = None
        if self.current_context == self.CallContext.GLOBAL:
            work_ctx = self.globals
        elif self.current_context == self.CallContext.WORKSPACE:
            work_ctx = self.workspace
        elif self.current_context == self.CallContext.PROJECT:
            work_ctx = self.workspace

        return work_ctx

    def __handle_workspace_key(self, func_name:str, arg:str) -> None:
        if func_name == "architecture": self.workspace.architecture = arg.s
        elif func_name == "configurations": self.workspace.configurations = convert_lua_table_to_pytable(arg)
        elif func_name == "startproject": self.workspace.startproject = arg.s
        elif func_name == "group": print(arg)

    def __handle_general_key(self, func_name:str, arg:str) -> None:
        work_ctx = self.__get_working_ctx()
        if func_name == "include": print(arg.s)

    def __handle_project_key(self, func_name:str, arg:str) -> None:
        if func_name == "kind": self.project.kind = arg.s
        elif func_name == "language": self.project.language = arg.s
        elif func_name == "characterset": self.project.characterset = arg.s
        elif func_name == "cppdialect": self.project.cppdialect = arg.s

    def visit_Call(self, node:ast.Call):
        func_name = ""

        # Parse names

        if isinstance(node.func, astnodes.Name):
            func_name = node.func.id
        if isinstance(node.func, astnodes.Index):
            func_name = node.func.idx

        # Parse arguments

        for arg in node.args:
            if func_name == "workspace":
                self.workspace = PGuiWorkspace(arg.s)
                self.current_context = self.CallContext.WORKSPACE
                continue
            if func_name == "project":
                self.project = PGuiProject(arg.s)
                self.current_context = self.CallContext.PROJECT
                continue
            
            if isinstance(arg, astnodes.Table):
                convert_lua_table_to_pytable(arg)

            if func_name in PremakeCallVisitor.GENERAL_KEYS:
                self.__handle_general_key(func_name, arg)
            elif func_name in PremakeCallVisitor.WORKSPACE_KEYS:
                self.__handle_workspace_key(func_name, arg)
            elif func_name in PremakeCallVisitor.PROJECT_KEYS:
                self.__handle_project_key(func_name, arg)


visitor = PremakeCallVisitor()
visitor.visit(parse_premake_file_to_ast("./premake5.lua"))
print(visitor.workspace)
# print(ast.toPrettyStr(parse_premake_file_to_ast("./premake5.lua")))
