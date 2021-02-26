### PythonLib folder explanation

PythonLib folder is the folder where all the python libraries
logic will be handled. We are going to use pipenv to install libraries, this way code distribution between people will be much easier.

### How to use pipenv

Chose pip3 or pip depending on your system

1º Install Pipenv

- pip3/pip install pipenv

2º Install all necessary packages:

- Open a terminal/CMD
- cd to PythonLib folder
- pipenv install # this will install all necessary packages automatically

3º From visual studio code select python interpreter

- For MAC users: - Project2021/src/PythonLib/.venv/bin/python3.8
- For Windows users: - Project2021/src/PythonLib/scripts/python.exe

Now you are ready to use python from VSCode

If you need to install other packages, you have to go to PythonLib folder and then do this:

- pipenv install package_name

For example:

- pipenv install pandas
