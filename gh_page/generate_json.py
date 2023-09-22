from __future__ import annotations

import yaml
import json
from jsonschema import validate
from pathlib import Path

# Define the path to the repo folder.
root_path = Path.resolve(Path(__file__) / '..' / '..')

# Define the path to exclude from the parsing.
EXCLUDE_DOMAIN_FOLDER_LIST = ['gh_page', '.github', '.git']
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

    yml_file_lst = [f for f in Path.iterdir(folder_path) if is_yaml_file(f) and f.name not in exclude]

    data = dict()
    for f in yml_file_lst:
        with open(f) as fh:
            # key is the file name without the extension
            suffix = f.suffix
            key = f.name[:-len(suffix)]
            data[key] = yaml.load(fh, Loader=yaml.FullLoader)

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
        else:
            domain_data['default'] = list(domain_data.keys())[0]

        data[domain] = domain_data


    # Validate the data.
    schema = json.loads((root_path / 'gh_page' / 'resource.schema.json').read_text())
    for domain, domain_data in data.items():
        try:
            validate(instance=domain_data, schema=schema)
        except Exception as e:
            raise Exception(f"Invalid data for domain: {domain}") from e

        # I use for iteration to walk through all the keys in the domain_data, but more efficient way is to
        # treat it as database.
        for metadata in extract_nested_metadata(domain_data):
            for value in metadata.values():
                try:
                    validata_metadata(value)
                except Exception as e:
                    raise Exception(f"Invalid metadata in {domain}: {value}") from e

    # Store the data in a JSON file.
    with open(root_path/ 'gh_page' / 'out' / 'database.json', 'w') as filep:
        json.dump(data, filep, indent=4)

    # Schema to out
    with open(root_path / 'gh_page' / 'out' / 'resource.schema.json', 'w') as filep:
        json.dump(schema, filep, indent=4)

def validata_metadata(data: dict):
    """validata the metadata for deep logic.
    For example, if the type is a list, then the default value should be in the list.
    """
    if isinstance(data, str):
        return
    if data.get("type") == "list":
        if "options" not in data:
            raise Exception(f"Invalid metadata: {data}, options not in list type matadata.")

        if "default" in data and data["default"] not in data["options"]:
            raise Exception(f"""Invalid metadata: {data}, default value "{data['default']}" not in options.""")

def extract_nested_metadata(data: dict):
    """Extract the nested metadata from the data."""
    for key, value in data.items():
        if key == "metadata":
            yield value
        elif isinstance(value, dict):
            yield from extract_nested_metadata(value)
        else:
            continue


if "__main__" == __name__:
    main()