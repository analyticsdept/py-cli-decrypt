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
    parser.add_argument('--line', '-l', help="key line number", type=int)
    parser.add_argument('--output', '-o', help="output file name", type=str)
    parser.add_argument('--error', '-e', help="error output file name", type=str)
    parser.add_argument('--fields', '-f', help="encrypted fields", nargs="+")
    return parser.parse_args()

def read_key(key, line):
    if os.path.exists(key):
        with open(key, 'r') as _file:
            _read_key = _file.read()
            _read_key = _read_key.splitlines()[line]
    else:
        _read_key = key
    return literal_eval(_read_key)

def run():

    _folder = ""

    _c = MetaCrypt()
    _line = args.line if args.line else 0
    _key = read_key(args.key, _line) if args.key else deferred_raise('missing key')
    _file = args.csv if args.csv else deferred_raise('missing csv file')
    _error_file = args.error if args.error else f'{args.csv.replace(".csv", "")}_errors.csv'
    _delimiter = args.delimiter if args.delimiter else ','
    _output = args.output if args.output else deferred_raise('missing output file path')
    _fields = args.fields if isinstance(args.fields, list) else deferred_raise('missing fields list')

    if not os.path.exists(_file):
        raise Exception('input file does not exist')
    else:
        _folder = os.path.dirname(os.path.abspath(_file))
        _output = f"{_folder}/{_output}" if "/" not in _output else _output

    if os.path.exists(_output):
        raise Exception('output file already exists, cannot overwrite')

    _errors = []

    with open(args.csv) as _file:
        _csv = csv.DictReader(_file, delimiter=_delimiter)
        with open(_output, 'w+') as _writer:
            writer = csv.DictWriter(_writer, _csv.fieldnames)
            writer.writeheader()
            for line in _csv:
                _is_error = False
                for field in _fields:
                    if field in line.keys():
                        try: line[field] = _c.decrypt_symmetric_siv(data=base64.b64decode(line[field]), key=_key).decode("utf-8")
                        except Exception as e: 
                            _errors.append({'field': field, 'value': line[field], 'error_type': type(e), 'error_message': str(e)})
                            _is_error = True
                if not _is_error:
                    writer.writerow(line)

    if len(_errors) > 0:
        with open(_error_file, 'w+') as _file:
            _file.write(f'field{_delimiter}value{_delimiter}error_type{_delimiter}error_message\n')
            for error in _errors:
                _file.write(f'{error.get("field")}{_delimiter}{error.get("value")}{_delimiter}{error.get("error_type")}{_delimiter}{error.get("error_message")}\n')
            _file.close()
        print(f"errors written to {_error_file}")

if __name__ == "__main__":
    
    args = make_arguments()

    try: run()
    except Exception as e: print(str(e))