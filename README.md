# py-cli-decrypt

## Installation

&nbsp;

### **Setup**

&nbsp;

Run `python -m venv env` to create a new environment

Run `source env/bin/activate` to launch the environment

Run `pip install -r requirements.txt` to install packages

Run `deactivate` to close the environment when the task is completed

&nbsp;

### **Decrypt**

&nbsp;

The program `main.py` takes the following arguments:

`-c` The input CSV file

`-d` CSV delimiter; defaults to comma

`-o` The name of the output file (must not exist)

`-k` The key file

`-l` Line number in the key file of the key (zero-indexed, defaults to zero)

`-f` List of fields to decrypt

&nbsp;

Usage:

```
python main.py
-c=path/to/file.csv -d=";"
-o=output_file_name.csv
-k=path/to/key.pem -l=1
-f field1 field2
```
