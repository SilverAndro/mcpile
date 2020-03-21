# Just a small useful class
# This gets passed around, holds our "stack" and any other data modules want to put on it
import os
import json

class State:
    def __init__(self, stack):
        self.stack = stack
        self.pushCount = 0
        self.tags = []

    def push(self, value):
        value = str(value)
        self.stack.append(value)
        self.pushCount += 1

    def pop(self):
        return self.stack.pop()

    def writeFunction(self, functiondir, writedata):
        seperated = functiondir.split(os.path.sep)
        writtenFile = seperated[-1]

        for tag in self.tags:
            if not tag.startswith("minecraft:"):
                try:
                    f = open(os.path.join(self.defaultTagOut, f"{tag}.json"))
                    data = json.load(f)
                    f.close()
                    data["values"].append(f"{self.namespace}:{writtenFile}")

                    jsoned = json.dumps(data, indent=2)

                    with open(os.path.join(self.defaultTagOut, f"{tag}.json"), "w") as f:
                        f.write(jsoned)

                except Exception as ex:
                    obj = {
                        "values": [
                            f"{self.namespace}:{writtenFile}"
                        ]
                    }
                    jsoned = json.dumps(obj, indent=2)

                    with open(os.path.join(self.defaultTagOut, f"{tag}.json"), "w") as f:
                        f.write(jsoned)
            else:
                tag = tag.split(":")[1]
                try:
                    f = open(os.path.join(self.minecraftTagOut, f"{tag}.json"))
                    data = json.load(f)
                    f.close()
                    data["values"].append(f"{self.namespace}:{writtenFile}")

                    jsoned = json.dumps(data, indent=2)

                    with open(os.path.join(self.minecraftTagOut, f"{tag}.json"), "w") as f:
                        f.write(jsoned)

                except Exception as ex:
                    obj = {
                        "values": [
                            f"{self.namespace}:{writtenFile}"
                        ]
                    }
                    jsoned = json.dumps(obj, indent=2)

                    with open(os.path.join(self.minecraftTagOut, f"{tag}.json"), "w") as f:
                        f.write(jsoned)

        self.tags = []

        with open(functiondir + ".mcfunction", 'a') as f:
                f.write(writedata + "\n")
