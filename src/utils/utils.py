from pathlib import Path

def load_file_contents(path):
    return Path(path).read_text(encoding='utf8')
