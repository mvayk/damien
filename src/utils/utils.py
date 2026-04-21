from pathlib import Path

def load_file_contents(path):
    base = Path(__file__).parent.parent
    absolute = (base / path).resolve()

    return absolute.read_text(encoding='utf8')
    # return Path(path).read_text(encoding='utf8')
