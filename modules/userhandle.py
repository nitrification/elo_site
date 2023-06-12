#Database processing code
import json
import time

def openfile(fp):
    return json.load(open(fp, "r"))

print(openfile("test.json"))
