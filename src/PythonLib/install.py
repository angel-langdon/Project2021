#%%
import os
import subprocess


def check_correct_working_dir():
    if "install.py" not in os.listdir("."):
        raise BaseException("Please execute Python script inside the PythonLib folder")

def create_virtual_environment_folder():
    virtual_environment_dir = os.path.abspath(".venv")
    if not os.path.isdir(virtual_environment_dir):
        print("- Creating virtual environment path: ")
        os.mkdir(virtual_environment_dir)
        print(virtual_environment_dir)
        print("\n\n")


def install_packages():
    print("-Installing python dependencies:\n")
    print(subprocess.check_output(['pipenv', 'install']).decode('utf-8'))
    print("\n\n")

def get_python_interpreter():
    result = subprocess.check_output('pipenv run python -c "import sys; print(sys.executable)"', shell=True)
    python_interpreter = result.decode('utf-8').strip()
    return python_interpreter

def add_packages():
    print("- Adding utils folder to python environment:\n")
    os.chdir("./lib/utils")
    print(subprocess.run([python_interpreter, 'add_package.py'],
                         capture_output=True,
                         text=True).stdout)


#%%

if __name__ == "__main__":
    check_correct_working_dir()
    create_virtual_environment_folder()
    install_packages()
    python_interpreter = get_python_interpreter()
    add_packages()
