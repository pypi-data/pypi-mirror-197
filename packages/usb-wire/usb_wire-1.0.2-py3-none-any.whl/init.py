import os
import string
import shutil

current_file_path = os.path.abspath(__file__)
current_dir_path = os.path.dirname(current_file_path)

class Driver:
    def get_all(driver=None):
        available_drives = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
        return available_drives

    def init(driver):
        try:
            os.mkdir(f"{driver}wire")
            with open(f"{driver}wire\\attr.wire", "w", encoding="utf-8") as f:
                f.write("")
            return True
        except:
            return print("Wire device is already inited.")

    def wait_for(what="connection", check=True):
        found = False
        while found is False:
            try:
                with open(f"{Driver.detect()}\\wire\\attr.wire", "r", encoding="utf-8") as f:
                    f.read()
                if check is True:
                    return Driver.detect() + "\\"
            except:
                pass

    def detect(driver=None):
        if driver is None:
            for drive in Driver.get_all():
                try:
                    with open(f"{drive}\\wire\\attr.wire", "r", encoding="utf-8") as f:
                        f.read()
                    return drive
                except:
                    pass

            return False

def execute(file):
    try:
        with open(file, "r", encoding='utf-8') as f:
            exec(f.read())
    except:
        raise "Cannot find file."

def transfer(from_path=Driver.detect(), to_path=current_dir_path, mode="file", cut=False):
    if from_path is False:
        raise "Auto-detected path is not foundable."

    if mode == "file":
        try:
            with open(from_path, "r", encoding='utf-8') as f:
                f.read()
            filename = os.path.basename(from_path)

            if cut is False:
                shutil.copy(from_path, to_path + rf"\{filename}")
            else:
                shutil.move(from_path, to_path + rf"\{filename}")
        except:
            raise "File is not foundable."
    elif mode == "directory":
        try:
            filename = os.path.basename(from_path)
            if cut is False:
                shutil.copytree(from_path, to_path + rf"\{filename}")
            else:
                shutil.move(from_path, to_path + rf"\{filename}")
        except:
            raise "Directory is not foundable."


def attributes(drive, method="get", args=None):
    if method == "get":
        try:
            with open(f"{drive}wire\\attr.wire", "r", encoding="utf-8") as f:
                return f.read().split("\n")
        except:
            raise "Device is not compatible with Wire."
    elif method == "write" and args is not None:
        try:
            with open(f"{drive}wire\\attr.wire", "w", encoding="utf-8") as f:
                f.write(args)
            return True
        except:
            raise "Device is not compatible with Wire."
    elif method == "add" and args is not None:
        try:
            with open(f"{drive}wire\\attr.wire", "a", encoding="utf-8") as f:
                f.write(f"\n{args}")
            return True
        except:
            raise "Device is not compatible with Wire."