from ast import literal_eval
from deferred_raise import deferred_raise
from metacrypt import MetaCrypt
import argparse
import base64
import csv
import os

def make_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', '-c', help="csv file", type=str)
    parser.add_argument('--delimiter', '-d', help="csv delimiter", type=str)
    parser.add_argument('--key', '-k', help="key string or file", type=str)
    parser.add_argument('--output', '-o', help="output file name", type=str)
    parser.add_argument('--fields', '-f', help="encrypted fields", nargs="+")
    return parser.parse_args()

def read_key(key):
    if os.path.exists(key):
        with open(key, 'r') as _file:
            _read_key = _file.read()
            _read_key.splitlines()[0]
    else:
        _read_key = key
    return literal_eval(_read_key)

def run():

    _c = MetaCrypt()

    _key = read_key(args.key) if args.key else deferred_raise('missing key')
    _file = args.csv if args.csv else deferred_raise('missing csv file')
    _delimiter = args.delimiter if args.delimiter else ','
    _output = args.output if args.output else deferred_raise('missing output file path')
    _fields = args.fields if isinstance(args.fields, list) else deferred_raise('missing fields list')

    if not os.path.exists(_file):
        raise Exception('input file does not exist')

    if os.path.exists(_output):
        raise Exception('output file already exists, cannot overwrite')

    with open(args.csv) as _file:
        _csv = csv.DictReader(_file, delimiter=_delimiter)
        with open(_output, 'w+') as _writer:
            writer = csv.DictWriter(_writer, _csv.fieldnames)
            writer.writeheader()
            for line in _csv:
                for field in _fields:
                    if field in line.keys():
                        line[field] = _c.decrypt_symmetric_siv(data=base64.b64decode(line[field]), key=_key).decode("utf-8")
                writer.writerow(line)

if __name__ == "__main__":
    
    args = make_arguments()

    try: run()
    except Exception as e: print(str(e))