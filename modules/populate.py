from sugar import newPreparse, returnStatus
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

def populate(info, text):
    split = text.split("$")
    out = ""

    for i in range(len(split)):
        if (i + 1) % 2 == 0:
            clean = split[i].strip()
            resplit = clean.split(" ")
            populateList = resplit[0]
            toFill = " ".join(resplit[1:])
            filled = []

            with open(os.path.join(dir_path, "PopulateFiles", populateList)) as f:
                for entry in f.readlines():
                    entry = entry.strip()
                    filled.append(toFill.replace("{}", entry).strip())

            for filledText in filled:
                out += filledText + "\n"
        else:
            out += split[i]
    return out

newPreparse(populate)