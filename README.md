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

`-k` The key file

`-l` Line location in the key file of the key

`-o` The name of the output file (does not have to exist)

`-f` List of fields to decrypt

&nbsp;

Usage:

`python main.py -c=path/to/file.csv -d=";" -k=path/to/key.pem -f field1 field2 -o=output_file_name.csv`
