import os

import http_client
import printer

BACKUP_FOLDER_NAME = 'backup'
BACKUP_FOLDER_PATH = './' + BACKUP_FOLDER_NAME


def start_backup() -> None:
    printer.print_heading('Preparations')

    printer.print_subheading('Creating directory for backup files...')
    if not os.path.exists(BACKUP_FOLDER_NAME):
        os.mkdir(BACKUP_FOLDER_NAME)
        print('Directory "%s" created.' % BACKUP_FOLDER_NAME)
    else:
        print('Directory "%s" already exists.' % BACKUP_FOLDER_NAME)

    printer.print_subheading('Determining already downloaded files...')
    downloaded_elements = []
    for subdir, dirs, files in os.walk(BACKUP_FOLDER_PATH):
        for file in files:
            if subdir == BACKUP_FOLDER_PATH:
                downloaded_elements.append(file[:-4])
    print('Count: ' + str(len(downloaded_elements)))
    downloaded_elements.sort()
    last_downloaded_element = downloaded_elements[-1]
    print('Last downloaded: ' + last_downloaded_element)

    printer.print_subheading('Determining available files...')
    all_elements = http_client.fetch_dates_with_sensor_data()
    print('Count: ' + str(len(all_elements)))
    files_to_download = [element for element in all_elements if element not in downloaded_elements]
    if last_downloaded_element in all_elements:
        files_to_download.append(last_downloaded_element)
    number_of_files_to_download = len(files_to_download)
    print('Files to download: ' + str(number_of_files_to_download))

    printer.print_heading('Backup')

    printer.print_subheading('Downloading files...')
    number_of_downloaded_files = 0

    printer.show_progress_bar(number_of_downloaded_files, number_of_files_to_download)
    for file_to_download in files_to_download:
        file_content = http_client.download_file(file_to_download)
        file = open(BACKUP_FOLDER_PATH + '/' + file_to_download + '.txt', 'w', encoding='utf-8')
        file.write(file_content)
        number_of_downloaded_files += 1
        printer.show_progress_bar(number_of_downloaded_files, number_of_files_to_download)

    print('Downloaded files: ' + str(number_of_downloaded_files))
