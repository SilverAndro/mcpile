import os
from importlib import import_module
from inspect import signature

class returnStatus:
    def __init__(self, write:str=None, writeBefore:str=None, skiplines:int=0, keepgoing:bool=True):
        self.write = write
        self.writeBefore = writeBefore
        self.skiplines = skiplines
        self.keepgoing = keepgoing
    def __iter__(self):
        yield from [self.write, self.writeBefore, self.skiplines, self.keepgoing]

# How many sections are returned
validSugarTypeList = {
    "lineStart": 2,
    "lineInternal": 3,
    "startEndInternal": 4
}

sugarList = {
    "lineInternal": [],
    "startEndInternal": [],
    "lineStart": []
}

preparseList = []

def newPreparse(callback):
    preparseList.append(callback)

# Function creates new syntax handlers
def newSyntax(sugarType, brackets, callback):
    if sugarType in validSugarTypeList:
        paramCount = validSugarTypeList[sugarType]
        sig = signature(callback)
        sigParamCount = len(sig.parameters)

        if not hasattr(brackets, '__iter__'):
            raise ValueError("Brackets must be iterable")

        if paramCount == sigParamCount:
            def runIfMet(line, info):
                line = str(line)
                if sugarType == "lineStart":
                    if line.startswith(brackets[0]):
                        write, writeBefore, skiplines, keepgoing = callback(
                            info, line.replace(brackets[0] + " ", ""))
                        if keepgoing:
                            return (1, write, writeBefore, skiplines)
                        else:
                            return (2, write, writeBefore, skiplines)
                elif sugarType == "lineInternal":
                    index = line.find(brackets[0])
                    if index >= 0:
                        before = line[:index]
                        after = line[index + len(brackets[0]):]

                        write, writeBefore, skiplines, keepgoing = callback(
                            info, before, after)

                        if keepgoing:
                            return (1, write, writeBefore, skiplines)
                        else:
                            return (2, write, writeBefore, skiplines)
                elif sugarType == "startEndInternal":
                    indexStart = line.find(brackets[0])
                    if indexStart >= 0:
                        indexEnd = line[indexStart + len(brackets[0]):].find(brackets[1]) + indexStart + len(brackets[0])
                        if indexEnd >= 0:
                            before = line[:indexStart]
                            middle = line[indexStart +
                                          len(brackets[0]):indexEnd]
                            end = line[indexEnd + len(brackets[1]):]

                            write, writeBefore, skiplines, keepgoing = callback(
                                info, before, middle, end)

                            if keepgoing:
                                return (1, write, writeBefore, skiplines)
                            else:
                                return (2, write, writeBefore, skiplines)
                return (0, None, None, 0)
            sugarList[sugarType].append(runIfMet)
        else:
            raise SyntaxError("Incorrect amount of parameters in callback for type {} ({} instead of {})".format(
                sugarType, sigParamCount, paramCount))
    else:
        raise SyntaxError("Invalid sugar of type {}".format(sugarType))

# Runs through syntax and evals the functions passed if requirements matched
# Syntax are run through in creation order for each type


def handle(info, line, wasBefore):
    if len(line) > 0:
        keys = sugarList.keys()
        for key in keys:
            array = sugarList[key]
            for function in array:
                result, write, writeBefore, skiplines = function(line, info)
                if result:
                    return result, write, writeBefore, skiplines
    return (2, line, wasBefore, 0)

def preparse(info, filetext):
    text = filetext
    for prefunc in preparseList:
        text = prefunc(info, text)
    return text

# Default syntax, "IMPORT <module>", imports a module
# Use this to load modules into your file
# Works just like python import, but if the file has an "onImport"
# function it gets run


def importSugar(info, line):
    module = import_module("modules." + line)
    if hasattr(module, "onImport"):
        module.onImport(info)
    return None, None, 0, False

def doImports(info, filetext):
    for line in filetext.split("\n"):
        if line.startswith("IMPORT "):
            importSugar(info, line.split(" ")[1])
