#!/usr/bin/env bash

if [[ $# -eq 0 ]]; then
  echo "Python binary was not specified!"
  exit 1
fi

PROJECT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
echo "Initializing a virtual environment..."
$1 -m venv venv
source "$PROJECT_DIR/venv/bin/activate"
echo "Done! Installing pip dependencies..."
"$PROJECT_DIR/venv/bin/pip" install -r requirements.txt
echo "Done! Setup completed."
