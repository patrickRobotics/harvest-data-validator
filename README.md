# Python harvest data validator command-line app

Project to build functional command line application (CLI) using Python and [Typer](https://typer.tiangolo.com/), 
to review all the data and to flag potential issues with the data.

## Project Overview
### Application requirements
The CLI program should take the `path` to the unzipped data directory 
(which includes `farm_data.json` and the set of `photographs`) as an argument. 

The output should include the **details** of all data points that `violate the rules` & `which rules they violate`.

### The issues that have been checked are listed below:
1. Flag all submissions where there are multiple measurements for the same crop in a single farm
2. Flag all submissions where the dry weight measurement exceeds the corresponding wet weight measurement
3. Flag all submissions where the dry weight is outside the standard deviation of all other submissions for the same crop
4. Flag all submissions where the GPS coordinates of one farm are within 200 meters of another recorded farm
5. Flag all submissions where the photo submitted is a duplicate of another photo that was submitted.

## Tools and libraries used
The following stack has been used to build the application:
- `Typer` to build the to-do application’s CLI
- Python’s `json` module to parse json file containing harvest measurements
- `Panda` for easy data processing for the json data.
- `Numpy` for complex computations like getting standard deviations of weights measurements

### Step 1: Set Up the Project
Setting up Python virtual environment [this project is built using Python3]
```shell
$ cd harvest-data-validator/
$ python3 -m venv ./venv
$ source venv/bin/activate
```
Now that you have a working virtual environment, you need to install project's requirements.
To install project's requirements, run the following command:

`(venv) $ python -m pip install -r requirements.txt`

### Step 2: Run the application
To start off, this CLI provides the following global options:
- `-v` or `--version` shows the current version and exits the application.
- `--help` shows the global help message for the entire application.

Showing application version:
```shell
(venv) $ python -m data_validator -v 
     
harvest-data_validator v0.1.0
```
Showing application help:
```shell
(venv) $ python -m data_validator --help

Usage: harvest-data_validator [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --version         Show the application's version and exit.
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or
                        customize the installation.

  --help                Show this message and exit.

Commands:
  validate
```
Show help docs of the available commands:
```shell
(venv) $ python -m data_validator validate --help

Usage: harvest-data_validator validate [OPTIONS]

Options:
  -dir, --data_directory PATH
  --help                       Show this message and exit.

```

To run the main CLI command, have a directory/folder that has your harvest measurements data.
Run the following command to analyze the data:

`python -m data_validator validate -dir /path_to/harvest_data_dir`

If you run this command and have valid data in the folder, then you get the following output:
```shell
(venv) $ python -m data_validator validate -dir /path_to/harvest_data_dir

**************** Processing farm data start ***************
Harvest data analysis results:
{"violated_rule": "Multiple measurements for the same crop in a single farm", "data_point": [{"farm_id": "76111112", "crop": "wheat", "location": "-1.079809736235451, 36.8871736391618", "wet_weight": 19.01, "dry_weight": 17.64}, {"farm_id": "76111112", "crop": "wheat", "location": "-1.079809736235451, 36.8871736391618", "wet_weight": 22.37, "dry_weight": 19.74}]}
{"violated_rule": "Dry weight measurement exceeds the corresponding wet weight measurement", "data_point": [{"farm_id": "91a23192111b", "crop": "sorghum", "location": "-1.1907708187237365, 36.81878372676805", "wet_weight": 41.04, "dry_weight": 42.21}]}
{"violated_rule": "Dry weight is outside SD of all other submissions for the same crop", "data_point": [{"farm_id": "12939411", "crop": "wheat", "location": "-1.1258585951680524, 36.89355167019951", "wet_weight": 301.11, "dry_weight": 203.19}]}
{"violated_rule": "GPS coordinates of farm within 200 meters of another recorded farm", "data_point": ["[{'farm_id': '819128', 'crop': 'sorghum', 'location': '-1.1913500507796262, 36.81766792763339', 'wet_weight': 21.54, 'dry_weight': 13.21} ** is near ** {'farm_id': '91a23192111b', 'crop': 'sorghum', 'location': '-1.1907708187237365, 36.81878372676805', 'wet_weight': 41.04, 'dry_weight': 42.21}]", "[{'farm_id': '91a23192111b', 'crop': 'sorghum', 'location': '-1.1907708187237365, 36.81878372676805', 'wet_weight': 41.04, 'dry_weight': 42.21} ** is near ** {'farm_id': '819128', 'crop': 'sorghum', 'location': '-1.1913500507796262, 36.81766792763339', 'wet_weight': 21.54, 'dry_weight': 13.21}]"]}

******** Farm data harvest validation completed ***********
```
If your folder doesn't have any of the files needed for this projects, you'll get the following output:
```shell
(venv) $ python -m data_validator validate -dir /path_to/harvest_data_dir

**************** Processing farm data start ***************
Getting files from /Users/user/Downloads/harvest_data_empty failed with parsing directory files error
```
If you don't provide directory/folder to the above command, you will get the following output:
```shell
(venv) $ python -m data_validator validate -dir /path_to/harvest_data_dir

Getting data directory /Users/user/Downloads/DL.pdf failed with data directory error
```
If you omit `-dir` or `--data_directory` argument, you'll be prompted to enter it to continue:
```shell
(venv) $ python -m data_validator validate

path to unzipped data directory?:
path to unzipped data directory?:
```
```shell
(.env) $ python -m data_validator validate
path to unzipped data directory?: /path_to/harvest_data_dir
**************** Processing farm data start ***************
Harvest data analysis results:
{"violated_rule": "Multiple measurements for the same crop in a single farm", "data_point": [{"farm_id": "76111112", "crop": "wheat", "location": "-1.079809736235451, 36.8871736391618", "wet_weight": 19.01, "dry_weight": 17.64}, {"farm_id": "76111112", "crop": "wheat", "location": "-1.079809736235451, 36.8871736391618", "wet_weight": 22.37, "dry_weight": 19.74}]}
{"violated_rule": "Dry weight measurement exceeds the corresponding wet weight measurement", "data_point": [{"farm_id": "91a23192111b", "crop": "sorghum", "location": "-1.1907708187237365, 36.81878372676805", "wet_weight": 41.04, "dry_weight": 42.21}]}
{"violated_rule": "Dry weight is outside SD of all other submissions for the same crop", "data_point": [{"farm_id": "12939411", "crop": "wheat", "location": "-1.1258585951680524, 36.89355167019951", "wet_weight": 301.11, "dry_weight": 203.19}]}
{"violated_rule": "GPS coordinates of farm within 200 meters of another recorded farm", "data_point": ["[{'farm_id': '819128', 'crop': 'sorghum', 'location': '-1.1913500507796262, 36.81766792763339', 'wet_weight': 21.54, 'dry_weight': 13.21} ** is near ** {'farm_id': '91a23192111b', 'crop': 'sorghum', 'location': '-1.1907708187237365, 36.81878372676805', 'wet_weight': 41.04, 'dry_weight': 42.21}]", "[{'farm_id': '91a23192111b', 'crop': 'sorghum', 'location': '-1.1907708187237365, 36.81878372676805', 'wet_weight': 41.04, 'dry_weight': 42.21} ** is near ** {'farm_id': '819128', 'crop': 'sorghum', 'location': '-1.1913500507796262, 36.81766792763339', 'wet_weight': 21.54, 'dry_weight': 13.21}]"]}

******** Farm data harvest validation completed ***********
```

## Assumptions made
This program has been developed with the following assumptions:
1. Apart from the default argument to the main command; `validate /path_to/harvest_data_dir`; there no other arguments 
   a user can pass to the command when interacting with the application.
2. The program run once and doesn't need other user's input to control exiting.
3. The program output is in-memory and not persisted (in disk).
4. The program assume the file sizes provided to the program are of small sizes (file size limits).
