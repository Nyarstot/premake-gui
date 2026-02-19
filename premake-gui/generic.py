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
