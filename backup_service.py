import file_service
import http_client
import print_service


def start_backup() -> None:
    print_service.print_heading('Preparations')

    print_service.print_subheading('Creating directory for backup files...')
    msg = file_service.create_directory_for_backup_files()
    print(msg)

    print_service.print_subheading('Determining already downloaded files...')
    downloaded_elements = file_service.get_backup_file_names_without_file_extension()
    print('Count: ' + str(len(downloaded_elements)))
    last_downloaded_element = downloaded_elements[-1]
    print('Last downloaded: ' + last_downloaded_element)

    print_service.print_subheading('Determining available files...')
    all_elements = http_client.fetch_dates_with_sensor_data()
    print('Count: ' + str(len(all_elements)))
    files_to_download = [element for element in all_elements if element not in downloaded_elements]
    if last_downloaded_element in all_elements:
        files_to_download.append(last_downloaded_element)
    number_of_files_to_download = len(files_to_download)
    print('Files to download: ' + str(number_of_files_to_download))

    print_service.print_heading('Backup')

    print_service.print_subheading('Downloading files...')
    number_of_downloaded_files = 0

    print_service.show_progress_bar(number_of_downloaded_files, number_of_files_to_download)
    for file_to_download in files_to_download:
        file_content = http_client.download_file(file_to_download)
        file_service.write_content_to_backup_file(file_to_download, file_content)
        number_of_downloaded_files += 1
        print_service.show_progress_bar(number_of_downloaded_files, number_of_files_to_download)

    print('Downloaded files: ' + str(number_of_downloaded_files))
