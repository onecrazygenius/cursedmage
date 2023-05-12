# Cursed Mage - A game made with pygame

## Install
To get started, clone the repository and setup using poetry
#### Clone the repository
```bash
mkdir cursedmage
cd cursedmage
git clone https://github.com/onecrazygenius/cursedmage.git .
```
#### Install Poetry
Install [Poetry](https://python-poetry.org/docs/#installation)
1. On Linux or MacOS run the following command
```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```
2. On Windows run the following command in PowerShell
```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -
```

#### Install dependencies
```bash
poetry install
```

#### Spawn a shell
```bash
poetry shell
```

#### Run
```bash
python app/main.py
```

## Run tests
```bash
pytest
```

## Build the game
```bash
pyinstaller build.spec
```