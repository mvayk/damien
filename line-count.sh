find . \
  -path "./venv" -prune -o \
  -path "./.venv" -prune -o \
  -path "./__pycache__" -prune -o \
  -name "*.py" -print | xargs wc -l
