# AiiDA resource registry

**THIS IS WORK IN PROGRESS - PULL REQUESTS & [SUGGESTIONS](https://github.com/aiidateam/aiida-resource-registry/issues) HIGHLY WELCOME**

This repository collects configurations of compute resources and code for quick and easy setup in AiiDA.

The registry computers and codes database are released as JSON files on: https://aiidateam.github.io/aiida-resource-registry/

## Using the AiiDA resource registry

In the following we'll take the example of [Piz Daint](https://www.cscs.ch/computers/piz-daint/), a HPC system at the Swiss National Supercomputing Centre.

### On AiiDAlab with resource setup widget

The easiest way to set up a computer and code is to use the resource setup widget in AiiDAlab.

 1. Open the AiiDAlab sidebar
 2. Click on the "Resource setup" button
 3. Select the computer and code you would like to set up

<!-- Placeholder for the gif screen record -->


### On a local AiiDA installation

Note: Not yet support template of configuration files for local AiiDA installation.

#### `verdi computer setup`

 1. Navigate to the [`daint.cscs.ch`](./daint.cscs.ch) folder in the GitHub web interface
 2. Select the partition you would like to run on, for example [`hybrid`](./daint.cscs.ch/hybrid)
 3. Click on the `computer-setup.yaml` file and click on the "Raw" button to get a direct link to the file

Now use this link to set up the computer directly via the `verdi` command line:
```
verdi computer setup --config https://raw.githubusercontent.com/aiidateam/aiida-code-registry/master/daint.cscs.ch/hybrid/computer-setup.yaml
```

You can overwrite any of the parameters provided in the yaml file by appending the corresponding option to the command, e.g. `--label my-computer-label` to overwrite the default computer label `daint-hybrid`.

Note: Alternatively, you can first create a local clone of the `aiida-code-registry` and pass the the local file path of the yaml file to the `--config` option.

#### `verdi computer configure`

Some computers require specific configuration options (e.g. to jump over a login node) and provide a dedicated `computer-configure.yaml` file.

You'll find it in the same folder:

```
verdi computer configure ssh daint-hybrid --config https://raw.githubusercontent.com/aiidateam/aiida-code-registry/master/daint.cscs.ch/hybrid/computer-configure.yaml
```

At this point, you should be able to successfully run:
```
verdi computer test daint-hybrid
```

#### `verdi code setup`

The [`daint.cscs.ch`](./daint.cscs.ch/) folder contains a [`codes`](./daint.cscs.ch/codes) subfolder with configuration files for individual codes.

Just pick the ones you need and set them up:

```
verdi code setup --config https://raw.githubusercontent.com/aiidateam/aiida-code-registry/master/daint.cscs.ch/codes/cp2k-8.1-hybrid.yaml
```

Note: You will be prompted for the computer label (which you can avoid by appending `--computer daint-hybrid` to the command).

## Contributing to this repository

We highly appreciate help in keeping the configurations up to date and adding new simulation codes & computers.

 1. Fork this repository
 2. Add your computer / code
 3. Create a Pull Request

 In order to test if your configuration and file/folder structure is correct, you can generate the JSON files locally:

```bash
pip install -r scripts/requirements.txt
python scripts/generate_json.py
```
