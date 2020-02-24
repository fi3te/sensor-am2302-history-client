import backup_service
import plot_service
import print_service
import statistics_service

print_service.print_heading('sensor-am2302-history-client')

print_service.print_subheading('Please choose an option...')

print('1) Backup files')
print('2) Show backup statistics')
print('3) Create plot')
print()


def execute_option_of_user_input() -> None:
    user_input = input('> ')
    options = {
        '1': backup_service.start_backup,
        '2': statistics_service.show_statistics,
        '3': plot_service.create_plot
    }
    options.get(user_input, execute_option_of_user_input)()


execute_option_of_user_input()
