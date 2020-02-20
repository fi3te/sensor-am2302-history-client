import backup_service
import printer

printer.print_heading('sensor-am2302-history-client')

printer.print_subheading('Please choose an option...')

print('1) Backup files')
print()


def execute_option_of_user_input():
    user_input = input('> ')
    options = {
        '1': backup_service.start_backup,
    }
    options.get(user_input, execute_option_of_user_input)()


execute_option_of_user_input()