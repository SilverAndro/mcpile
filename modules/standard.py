import os
import json
import re

from sugar import newSyntax, newPreparse, returnStatus

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


def onImport(info):
    info.whileCommands = []
    info.functionDict = {}

def ignoreComment(info, line):
    return returnStatus(keepgoing=False)

def registerSubstitution(info, line):
    split = line.split("[=]")
    
    seperated = list(map(lambda string: string.strip(), split))

    key = seperated[0]
    value = seperated[1]

    def replace(info, before, after):
        return returnStatus(write=before + value + after)

    newSyntax("lineInternal", [key], replace)

    return returnStatus(keepgoing=False)


def activeTagManager(info, line):
    seperated = line.split(" ")

    tagID = seperated[0]
    
    info.tags.append(tagID[1:])

    return returnStatus(keepgoing=False)

def passiveTagManager(info, text:str):
    split = text.split("openTagFile")
    combosplit = [final.strip() for group in split for final in group.split("closeTagFile")]
    for i in range(len(combosplit)):
        if (i + 1) % 2 == 0:
            # Handle good group
            lines = combosplit[i].split("\n")

            tagFileInfo = lines[0]

            print(tagFileInfo)

            for line in lines[1:]:
                if len(line) > 0:
                    print(line)
    return text

def executeDepth(info, line):
    line = 'execute ' + line
    if line[-1] == "{":
        command = line[:-2]
        info.push(str(info.pushCount) + "execute")
        toRun = command + \
            " run function {}:{}".format(info.namespace, info.stack[-1])
        return returnStatus(writeBefore=toRun, keepgoing=False)
    else:
        return returnStatus()


def whileDepth(info, line):
    line = 'execute ' + line
    if line[-1] == "{":
        command = line[:-2]
        info.push(str(info.pushCount) + "while")
        toRun = command + \
            " run function {}:{}".format(info.namespace, info.stack[-1])
        info.whileCommands.append(
            command + " run function {}:{}".format(info.namespace, info.stack[-1]))
        return returnStatus(writeBefore=toRun, keepgoing=False)
    else:
        return returnStatus()

def functionGen(info, line):
    cleanline = line.replace(" ", "").replace("{", "")
    if line[-1] == "{":
        functionName = line[0:-2]
        info.functionDict[functionName] = str(info.pushCount) + cleanline
        info.push(str(info.pushCount) + cleanline)
        return returnStatus(keepgoing=False)
    else:
        return returnStatus()

def callfunction(info, line:str):
    if ":" in line:
        return returnStatus(write=f"function {line}", keepgoing=False)
    else:
        return returnStatus(write=f"function {info.namespace}:{info.functionDict[line]}", keepgoing=False)

def doDepth(info, line):
    line = 'execute ' + line
    if line[-1] == "{":
        command = line[:-2]
        info.push(str(info.pushCount) + "do")
        toRun = "run function {}:{}".format(info.namespace, info.stack[-1])
        info.whileCommands.append(
            command + " run function {}:{}".format(info.namespace, info.stack[-1]))
        return returnStatus(writeBefore=toRun, keepgoing=False)


def leaveWhile(info, line):
    info.writeFunction(os.path.join(info.outdir, "functions", info.stack[-1]), info.whileCommands.pop())
    info.pop()
    return returnStatus(keepgoing=False)


def leaveExecute(info, line):
    info.pop()
    return returnStatus(keepgoing=False)

def leaveFunction(info, line):
    info.pop()
    return returnStatus(keepgoing=False)


def handleLeave(info, line):
    data = info.stack[-1]
    ident = re.search(r"([a-zA-Z]+)", data).group(0)
    if ident == "execute":
        leaveExecute(info, line)
    elif ident == "while" or ident == "do":
        leaveWhile(info, line)
    elif ident in info.functionDict.keys():
        leaveFunction(info, line)
    return returnStatus(keepgoing=False)


newSyntax("lineStart", ["REPLACE"], registerSubstitution)
newSyntax("lineStart", ["*"], activeTagManager)
newSyntax("lineStart", ["//"], ignoreComment)
newSyntax("lineStart", [":execute"], executeDepth)
newSyntax("lineStart", [":while"], whileDepth)
newSyntax("lineStart", [":do"], doDepth)
newSyntax("lineStart", [":function"], functionGen)
newSyntax("lineStart", [":run"], callfunction)
newSyntax("lineStart", ["}"], handleLeave)

newPreparse(passiveTagManager)