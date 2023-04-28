## Installing requirements
import subprocess
import platform

user_os = platform.system()
err = 0

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

ret = '\n'.join(f"-> {req}" for req in requirements)
print(f"Installing the following requirements: \n{ret}")

if user_os == "Darwin":
    pip = "pip3"
elif user_os == "Linux" or user_os == "Windows":
    pip = "pip"
    
for requirement in requirements:
    print("====================================================================================")
    try:
        subprocess.check_call([pip, "install", requirement])
        # ugly if ure not running it by double clicking through file explorer
        
    except subprocess.CalledProcessError as e:
        err += 1
        print(e)
        continue
        
print("====================================================================================")
input(f"/!\ Installing required modules finished with {err} errors. Press Enter to exit.\t")

