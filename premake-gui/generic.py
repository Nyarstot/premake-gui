import os

def premake_executable_exists(path:str):
    full_path = os.path.join(path, "premake5.exe")
    if not os.path.exists(full_path):
        return False
    return True

def premake_configfile_exists(path:str):
    full_path = os.path.join(path, "premake5.lua")
    if not os.path.exists(full_path):
        return False
    return True

class PGuiVersionString(object):
    
    def __init__(self, major:int, minor:int, patch:int, addition:str="") -> None:
        self.major:int = major
        self.minor:int = minor
        self.patch:int = patch

        self.addition:str = ""
        self.__has_addition:bool = False
        if addition:
            self.__has_addition = True
            self.addition = f"-{addition}"

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}{self.addition}"

class PGuiPremakeController(object):

    def __init__(self) -> None:
        self.premake_path:str = None
        self.source_path:str = None
        self.build_path:str = None