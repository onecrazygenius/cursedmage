# Cursed Mage - A game made with pygame

## Install
To get started, clone the repository and install the dependencies in a virtual environment.
#### Clone the repository
```bash
mkdir cursedmage
cd cursedmage
git clone https://github.com/onecrazygenius/cursedmage.git .
```
#### Create a virtual environment
```bash
python -m venv venv
```

#### Activate the virtual environment
1. Windows
```bash
venv\Scripts\activate.bat
```
2. Linux
```bash
source venv/bin/activate
```

#### Install the dependencies
```bash
pip install -e .
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