# This is the main file to run
import os
import shutil
import sys
import time
import tempfile as tmpf

import state
import sugar

dir_path = os.path.dirname(os.path.realpath(__file__))


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


# Get input, output, namepsace
outputFile = "data"
if len(sys.argv) > 1:
    inputFile = sys.argv[1]
    try:
        namespace = sys.argv[3]
    except:
        namespace = "defaultnamespace"
else:
    inputFile = input("Input file: ")
    namespace = input("Namespace: ")
    if len(namespace) == 0:
        namespace = "defaultnamespace"

startTime = time.time()

outdir = os.path.join(dir_path, outputFile, namespace)

# Create out directory
try:
    shutil.rmtree(os.path.join(dir_path, outputFile))
except:
    None
createFolder(os.path.join(outdir, "functions"))
createFolder(os.path.join(outdir, "tags", "functions"))
createFolder(os.path.join(dir_path, outputFile,
                          "minecraft", "tags", "functions"))


def handleLine(line, wasBefore=None):
    status, write, writeBefore, skiplines = sugar.handle(info, line, wasBefore)
    if status == 1:  # Reparse
        if write != None:
            lines = write.split("\n")

            for line in lines:
                handleLine(line, writeBefore)
    elif status == 2:  # Push to output
        if write != None and len(write) > 0:
            info.writeFunction(os.path.join(
                outdir, "functions", info.stack[-1]), write)
        if writeBefore != None and len(writeBefore) > 0:
            info.writeFunction(os.path.join(
                outdir, "functions", info.stack[-2]), writeBefore)


info = state.State(['main'])

info.infile = inputFile
info.outdir = outdir
info.minecraftTagOut = os.path.join(
    dir_path, outputFile, "minecraft", "tags", "functions")
info.defaultTagOut = os.path.join(outdir, "tags", "functions")
info.tmpFile = tmpf.TemporaryFile(mode="w+t", prefix="mcpile_")
info.namespace = namespace

with open(inputFile, "r") as f:
    print("Importing modules...")
    program = f.read()
    sugar.doImports(info, program)

    print("Preparsing file...")
    final = sugar.preparse(info, program)

    print("Final parsing of file...")
    lines = []
    skiplines = 0

    for line in final.split("\n"):
        lines.append(line)

    for lineIndex in range(len(lines)):
        count = int(((lineIndex + 1) / len(lines)) * 50)
        sys.stdout.write(
            f"\r{lineIndex + 1}/{len(lines)} |" + "#" * count + " " * (50-count) + "|")
        sys.stdout.flush()
        if skiplines > 0:
            skiplines -= 1
        else:
            line = lines[lineIndex]
            line = line.strip()
            handleLine(line)

endTime = time.time()
deltaTime = endTime - startTime
print("\nFinished compiling in {:0.2f} seconds.".format(deltaTime))

info.tmpFile.close()