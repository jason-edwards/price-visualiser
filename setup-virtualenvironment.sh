#!/bin/bash
ENV_DIRNAME=venv
PIP_MODULES="requests sqlalchemy beautifulsoup4 nltk"

python envbuilder.py $ENV_DIRNAME

bash $ENV_DIRNAME/Scripts/activate.sh

echo "bash $ENV_DIRNAME/Scripts/activate.sh" > venv_activate.sh
echo "bash $ENV_DIRNAME/Scripts/deactivate.sh" > venv_deactivate.sh

bash venv_activate.sh

pip install $PIP_MODULES
