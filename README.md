# AiiDA resource registry

**THIS IS WORK IN PROGRESS - PULL REQUESTS & [SUGGESTIONS](https://github.com/aiidateam/aiida-resource-registry/issues) HIGHLY WELCOME**

This repository collects configurations of compute resources and code for quick and easy setup in AiiDA.

The registry computers and codes database are released as JSON files on: https://aiidateam.github.io/aiida-resource-registry/

## Using the AiiDA resource registry

In the following, we'll take the example of [Piz Daint](https://www.cscs.ch/computers/piz-daint/), an HPC system at the Swiss National Supercomputing Centre.

### On AiiDAlab with resource setup widget

The easiest way to set up a computer and code is to use the resource setup widget in AiiDAlab.

 1. Open the AiiDAlab sidebar
 2. Click on the "Resource setup" button
 3. Select the computer and code you would like to set up

<!-- Placeholder for the gif screen record -->

## Contributing to this repository

We highly appreciate help in keeping the configurations up to date and adding new simulation codes & computers.

 1. Fork this repository
 2. Add your computer/code
 3. Create a Pull Request

 In order to test if your configuration and file/folder structure is correct, you can generate the JSON files locally:

```bash
pip install -r gh_page/requirements.txt
python gh_page/generate_json.py
```
