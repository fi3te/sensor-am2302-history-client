# sensor-am2302-history-client

The application sensor-am2302-history-client can be used to fetch and visualize temperature and humidity data of a [sensor-am2302-history](https://github.com/fi3te/sensor-am2302-history) server.

## Usage

- Install the Python version specified in the file `Pipfile`.
- Install the virtualenv management tool [Pipenv](https://pipenv.pypa.io/).
- Open the terminal in the project folder.
- Run `pipenv install --ignore-pipfile`
- Run the application as explained:
  ```console
  $ pipenv run python -m app --help

  ============================================================
  |               sensor-am2302-history-client               |
  ============================================================
  usage: app.py [-h] [-i IP] [-p PORT] [-b BACKUP_FOLDER_PATH] {backup} ...

  positional arguments:
    {backup}
      backup

  optional arguments:
    -h, --help            show this help message and exit
    -i IP, --ip IP        192.168.0.50
    -p PORT, --port PORT  4000
    -b BACKUP_FOLDER_PATH, --backup-folder-path BACKUP_FOLDER_PATH
                          ./backup
  ```
- Examples:  
  `pipenv run python -m app`  
  `pipenv run python -m app -i localhost`  
  `pipenv run python -m app -b ./data`  
  Use the argument 'backup' to fetch the data non-interactively:  
  `pipenv run python -m app backup -i 192.168.0.10 -b ./data`
  