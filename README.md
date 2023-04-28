python -m venv venv

### Windows
.\venv\Scripts\activate
### Linux
source venv/bin/activate

```bash
pip install -e .
```

## Run
```bash
python app/main.py
```

## Build
```bash
pyinstaller build.spec
```