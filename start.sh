AMOUNT=${1:-1}

find_python() {
  if command -v python3.10 >/dev/null 2>&1; then
    echo "python3.10"
  elif command -v python3 >/dev/null 2>&1; then
    echo "python3"
  elif command -v python >/dev/null 2>&1; then
    echo "python"
  else
    echo "No suitable Python version found. Please install Python."
    exit 1
  fi
}

PYTHON=$(find_python)

for (( i=1; i<=AMOUNT; i++ ))
do
  $PYTHON main.py
done

rm -rf temp