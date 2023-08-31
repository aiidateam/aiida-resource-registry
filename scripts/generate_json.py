from __future__ import annotations

import yaml
import json
import copy
from pathlib import Path

# Define the path to the repo folder.
root_path = Path.resolve(Path(__file__) / '..' / '..')

# Define the path to exclude from the parsing.
EXCLUDE_DOMAIN_FOLDER_LIST = ['scripts', '.github', '.git']
EXCLUDE_COMPUTER_FOLDER_LIST = ['default', 'codes']

def is_yaml_file(file_path: Path) -> bool:
    """Check if the file is a YAML file."""
    if file_path.suffix not in ['.yml', '.yaml']:
        return False

    if not file_path.is_file():
        return False

    # validate the YAML file
    try:
        yaml.safe_load(file_path.read_text())
    except Exception:
        raise Exception(f"Invalid YAML file: {file_path}")

    return True

def parse_config(folder_path, exclude: None | list=None):
    """Go through the folder and parse all the YAML files."""
    if exclude is None:
        exclude = []

    # XXX: using is_yaml_file() to check if the file is YAML file
    yml_file_lst = [f for f in Path.iterdir(folder_path) if is_yaml_file(f) and f.name not in exclude]

    data = dict()
    for f in yml_file_lst:
        with open(f) as fh:

            data[f.name] = yaml.load(fh, Loader=yaml.FullLoader)

    return data

def main():
    # Extract all the data.
    # Get all the available domains and initialize the final dictionary.
    data = dict()

    for domain_path in Path.iterdir(root_path):
        domain = domain_path.name

        if domain in EXCLUDE_DOMAIN_FOLDER_LIST or domain_path.is_file():
            # skip the excluded folders and files
            continue

        domain_data = dict()
        for computer_path in Path.iterdir(domain_path):

            computer = computer_path.name

            if computer in EXCLUDE_COMPUTER_FOLDER_LIST or computer_path.is_file():
                # skip the excluded folders and files
                continue

            domain_data[computer] = dict()
            domain_data[computer]["computer"] = parse_config(computer_path)
            domain_data[computer]["codes"] = parse_config(computer_path / "codes")

        # Extract the default computer
        link = domain_path / 'default'
        if link.exists() and link.is_symlink():
            domain_data['default'] = Path.readlink(link).name

        data[domain] = domain_data

    # Store the data in a JSON file.
    with open(root_path/ 'database.json', 'w') as filep:
        json.dump(data, filep, indent=4)



if "__main__" == __name__:
    main()