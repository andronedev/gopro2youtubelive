import os

def save_prefs(key, value):
    if not os.path.isfile("prefs.txt"):
        with open("prefs.txt", "w") as f:
            f.write("")
    found = False
    with open("prefs.txt", "r") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if lines[i].startswith(key):
                lines[i] = key + "=" + value + "\n"
                found = True
                break
    if not found:
        lines.append(key + "=" + value + "\n")
    with open("prefs.txt", "w") as f:
        f.writelines(lines)

def get_prefs(key):
    if not os.path.isfile("prefs.txt"):
        return None
    with open("prefs.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith(key):
                return line.split("=")[1].strip()
    return None