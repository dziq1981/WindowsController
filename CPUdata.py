import subprocess

def clearStr(str2clear : str):
    newString = str(str2clear)     
    newString = newString.replace("b'","")
    newString = newString.replace("\\n'","")
    newString = newString.replace("'","")
    print(newString)
    return newString

def _executeCommand(command):
    return clearStr(subprocess.check_output(command, shell = True ))

def getCPUload():
    return _executeCommand("top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'")