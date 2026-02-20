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

    def __repr__(self) -> str:
        return f"{self.name}:{self.includes}"

    def __str__(self) -> str:
        return f"{self.name}:{self.includes}"

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
        self.pchheader:str = None
        self.pchsource:str = None

class PremakeCallContext(object):

    class VisitContext(IntEnum):
        GLOBAL = 0
        WORKSPACE = 1
        PROJECT = 2

    def __init__(self) -> None:
        self.writing_group:bool = False
        self.group_context:PGuiGroup = None
        self.visit_context:int = self.VisitContext.GLOBAL

class PremakeCallVisitor(ast.ASTVisitor):

    GENERAL_KEYS = {"include"}
    WORKSPACE_KEYS = {"architecture", "configurations", "startproject", "group"}
    PROJECT_KEYS = {"kind", "language", "characterset", "cppdialect", "pchheader", "pchsource", "files", "includedirs", "defines", "links", "postbuildcommands"}

    def __init__(self) -> None:
        self.includes = []
        self.globals = None
        self.workspace = None
        self.project = None
        self.call_context = PremakeCallContext()

    def __get_working_ctx(self) -> None:
        work_ctx = None
        if self.call_context.visit_context == PremakeCallContext.VisitContext.GLOBAL:
            work_ctx = self.globals
        elif self.call_context.visit_context == PremakeCallContext.VisitContext.WORKSPACE:
            work_ctx = self.workspace
        elif self.call_context.visit_context == PremakeCallContext.VisitContext.PROJECT:
            work_ctx = self.workspace

        return work_ctx

    def __handle_workspace_key(self, func_name:str, arg:str) -> None:
        if func_name == "architecture": self.workspace.architecture = arg.s
        elif func_name == "configurations": self.workspace.configurations = convert_lua_table_to_pytable(arg)
        elif func_name == "startproject": self.workspace.startproject = arg.s
        elif func_name == "group":
            if arg.s == "":
                self.call_context.group_context = None
                self.call_context.writing_group = False
                return

            group_obj = PGuiGroup(arg.s)
            self.call_context.group_context = group_obj
            self.call_context.writing_group = True
            self.workspace.groups.append(group_obj)

    def __handle_general_key(self, func_name:str, arg:str) -> None:
        work_ctx = self.__get_working_ctx()
        if func_name == "include":
            if self.call_context.writing_group:
                group_object:PGuiGroup = self.call_context.group_context
                group_object.includes.append(arg.s)

    def __handle_project_key(self, func_name:str, arg:str) -> None:
        if func_name == "kind": self.project.kind = arg.s
        elif func_name == "language": self.project.language = arg.s
        elif func_name == "characterset": self.project.characterset = arg.s
        elif func_name == "cppdialect": self.project.cppdialect = arg.s
        elif func_name == "pchheader": self.project.pchheader = arg.s
        elif func_name == "pchsource": self.project.pchsource = arg.s

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
                self.call_context.visit_context = PremakeCallContext.VisitContext.WORKSPACE
                continue
            if func_name == "project":
                self.project = PGuiProject(arg.s)
                self.call_context.visit_context = PremakeCallContext.VisitContext.PROJECT
                continue

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
