python -m venv venv

### Windows
.\venv\Scripts\activate
### Linux
source venv/bin/activate

```bash
pip install -r requirements.txt
```

## Run
```bash
python app/main.py
```

## Build
```bash
pyinstaller build.spec
```