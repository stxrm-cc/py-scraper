## Installing requirements
import subprocess
import platform

user_os = platform.system()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

ret = '\n'.join(f"-> {req}" for req in requirements)
print(f"Installing the following requirements: {ret}")

if user_os == "Darwin":
    pip = "pip3"
elif user_os == "Linux" or user_os == "Windows":
    pip = "pip"
    
for requirement in requirements:
    try:
        subprocess.check_call([pip, "install", requirement])
        # ugly if ure not running it by double clicking through file explorer
        print("====================================================================================")
    except subprocess.CalledProcessError as e:
        print(e)
        continue

input("/!\ Installing required modules done. Press Enter to exit.\t")

