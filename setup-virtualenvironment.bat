set "env_dirname=venv"
set "pip_modules=requests sqlalchemy beautifulsoup4"

python envbuilder.py %env_dirname%

call "%env_dirname%/Scripts/activate.bat"

echo call %env_dirname%/Scripts/activate.bat > venv_activate.bat
echo call %env_dirname%/Scripts/deactivate.bat > venv_deactivate.bat

call venv_activate.bat

pip install %pip_modules%
