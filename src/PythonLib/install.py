#%%
import os
import subprocess

if "install.py" not in os.listdir("."):
    raise BaseException("Please execute Python script inside the PythonLib folder")

virtual_environment_dir = os.path.abspath(".venv")
if not os.path.isdir(virtual_environment_dir):
    print("- Creating virtual environment path: ")
    os.mkdir(virtual_environment_dir)
    print(virtual_environment_dir)
    print("\n\n")

#%%

print("-Installing python dependencies:\n")
print(subprocess.check_output(['pipenv', 'install']).decode('utf-8'))
print("\n\n")

#%%
# Get the Python interpreter path
result = subprocess.check_output('pipenv run python -c "import sys; print(sys.executable)"', shell=True)
python_interpreter = result.decode('utf-8').strip()


#%%
print("- Adding utils folder to python environment:\n")
os.chdir("lib/utils")
print(subprocess.run([python_interpreter, 'add_package.py'],
                     capture_output=True,
                     text=True).stdout)

# %%
