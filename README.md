# Batch-Manager
Generate and Submit Batches to Coulson, Receive and Delete Batches from Coulson.

## Setup
### Configuration
You can optionally set the following in config.csv:
* _Coulson Username_ - The username used to SSH into Coulson when running batches (defaults to your current system username)
* _Receive Output Path_ - The path where output files are transferred to once the batch run has comlpeted (defaults to _output_files_)

### Running the program
The program has the following dependencies (which can be installed via `pip install [package_name]`):
* paramiko
* numpy
* datetime
* zipfile

You must have an SSH key for Coulson added to your SSH agent, as password functionality has been removed for simplicity.
You must also be able to access Coulson, either via local network or via the University VPN.

The program can be run with `python main.py`

## Interface
The program uses an integer-based menu system. Your inital options are:
### Generate Batches
Here you can choose to make either NetMC or Triangle Raft batches.

You can vary up to 10 variables in the input files (I wouldn't recommend exceeding 3).
When chosing a variable, the table presented tells you the variable type and allowed values on the right (which are input validated later).
If a variable is not chosen to be varied, it will remain constant at the given _value_ in the corresponding template csv file which you can edit in _common_files_

There are various modes of varying variables which are hopefully self explanatory. 

The batch will be saved as a _.zip_ file in the _batches_ directory, the structure of which is automatically generated job names with a single input file within to save transferring over uneccessary data to Coulson.

### Submit Batches
Here you can submit batches to Coulson.
You will be presented with a table that shows information for batches you've generated: the number of jobs within, the number of times submitted and the last time submitted.
This table is sorted by most recently submitted for your convenience.

When you submit a batch, __there is no confirmation__, so be sure you really want to send it off. 
The program checks to see if you have the necessary remote files in your Coulson home directory, and if not, unzips the file _common_files/Batch-Manager-Remote.zip_ to your Coulson home directory.

A detatched daemon process is then initiated to handle all the submission and receiving for you, so you can safely exit the program should your batch take hours to complete.
The daemon process sends over the local batch zip and executes a remote python script on Coulson.
This remote python script unzips the batch and for each job does the following:
* Adds the executable
* Generates and adds a unique _job_submission_script.sh_
* If the batch type is triangle raft, adds the seed to each job, and if the seed does not exist, runs _remote_management/seeds/make_poly_seed.py_ to generate it
* Runs `qsub job_submission_script.sh` for each job

The remote script then checks `qstat -u [username] -r` to see if the batch has finished running (ie, _batch_desc_ is not found)
Finally, the remote script zips up all relevent files (ie, __not__ the executable, _job_submission_script.sh_ or seed files) and deletes the batch folder

Meanwhile, the detatched daemon process has been checking to see if said zip file has been created every 5 seconds.
Once detected, the zip is transferred to _Receive Output Path_, unzipped, and deleted on Coulson to save space.

### Analyse Batches
Not yet implemented

## Troubleshooting
### Batches don't seem to submit
* Make sure you've configued your _Coulson Username_ in _config.csv_ correctly
* Make sure you have an SSH key for Coulson

## Future Development
* Currently working on implementing [Oliver Whitaker's](https://github.com/oliwhitg) NetMC Pores program
* Add option to cancel a batch submission
* Add warning to user if not connected to Coulson
* Add feature to make sure you cannot create two batches of the same name
