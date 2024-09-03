# SyncFolder

#### A program that synchronizes two folders: source and replica
* File creation/copying/removal operations should be logged to a file and to the console output;
* Synchronization is performed periodically;
* Folder paths, synchronization interval and log file path are provided using command line arguments.   

## Requirements
* Python 3.x
* Libraries: hashlib, os, time, shutil, argparse, logging

## How to Use

1. Ensure you have Python 3.x installed on your system.
2. Download or clone this repository to your local machine.

## Usage

```
python syncFolder.py [--src SOURCE] [--dst REPLICA] [--log-file LOG_FILE] [--delay DELAY]
```
- `--src`: Path to the source folder to be synchronized (required).
- `--dst`: Path to the replica folder that will be updated to match the source folder (default: "replica").
- `--log-file`: Path to the log file (default: "log.txt").
- `--delay`: Delay for synchronization in seconds (Default: 10).

## Example

To synchronize a folder named "ORIGIN" to "DESTINATION" with a delay of 25 seconds and log the synchronization process to "syncFolder_log.txt", run the following command:

```
python syncFolder.py --src ORIGIN --dst DESTINATION --log-file syncFolder_log.txt --delay 25
```

```
1900-01-01 00:00:44,382 [DEBUG]: Starting synchronization...
Src: C:\Users\Testing\Projects\SyncFolder\ORIGIN
Dst: C:\Users\Testing\Projects\SyncFolder\REPLICA
Sync time: 25
1900-01-01 00:00:44,405 [UP_TO_DATE]: C:\Users\Testing\Projects\SyncFolder\ORIGIN\portrait1.jpg
1900-01-01 00:00:44,406 [UP_TO_DATE]: C:\Users\Testing\Projects\SyncFolder\ORIGIN\test.txt
1900-01-01 00:00:44,406 [DEBUG]: Synchronization completed.
1900-01-01 00:01:09,421 [UP_TO_DATE]: C:\Users\Testing\Projects\SyncFolder\ORIGIN\portrait1.jpg
1900-01-01 00:01:09,421 [COPIED]: C:\Users\Testing\Projects\SyncFolder\ORIGIN\random.jpg
1900-01-01 00:01:09,422 [UP_TO_DATE]: C:\Users\Testing\Projects\SyncFolder\ORIGIN\test.txt
1900-01-01 00:01:09,422 [DEBUG]: Synchronization completed.
1900-01-01 00:01:34,432 [UP_TO_DATE]: C:\Users\Testing\Projects\SyncFolder\ORIGIN\random.jpg
1900-01-01 00:01:34,438 [UP_TO_DATE]: C:\Users\Testing\Projects\SyncFolder\ORIGIN\portrait1.jpg
1900-01-01 00:01:34,438 [DELETED]: REPLICA\test.txt
1900-01-01 00:01:34,439 [DEBUG]: Synchronization completed.
1900-01-01 00:01:37,114 [ERROR]: Synchronization stopped manually.
1900-01-01 00:01:37,114 [DEBUG]: Exiting the synchronization script.
```


## Considerations
- Files are compared by doing a MD5 hash. Modifying the filename will be considered a new file.
- If the replica folder does not exist, the script will create it.
- If the source folder does not exist, the script will raise an error.
- The script will continuously monitor the source folder and synchronize it with the replica folder based on the specified delay.
- To stop the script manually, use the keyboard interrupt (CTRL+C).
- The logger levels were customized for better actions identification on console output and log file.

| Level    | Keyword    | Usage               |
|----------|------------|---------------------|
| DEBUG    | (n/a)      | Information         |
| WARNING  | COPIED     | file/folder created |
| INFO     | UP_TO_DATE | file already exists and **not** modified |
| CRITICAL | UPDATED    | file already exists and **was** modified|
| 21       | DELETED    | file/folder removed |

