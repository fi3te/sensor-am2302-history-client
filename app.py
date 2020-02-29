import types
from typing import NamedTuple, Optional, List

import backup_service
import plot_service
import print_service
import statistics_service


class Option(NamedTuple):
    key: str
    description: str
    executable: bool
    action: Optional[types.FunctionType]
    suboptions: Optional[List['Option']]


all_options = [
    Option('1', 'Backup files', True, backup_service.start_backup, None),
    Option('2', 'Show backup statistics', True, statistics_service.show_statistics, None),
    Option('3', 'Create plot', False, None, [
        Option('1', 'Daily mean plot', True, plot_service.show_daily_mean_plot, None),
        Option('2', 'Monthly mean plot', True, plot_service.show_monthly_mean_plot, None)
    ])
]


def process_options(options: List[Option], show_options: bool) -> None:
    if show_options:
        print()
        for option in options:
            print('%s) %s' % (option.key, option.description))

    user_input = input('> ')
    dictionary = {option.key: (option.action if option.executable else option.suboptions) for option in options}
    function_or_suboptions = dictionary.get(user_input)
    if isinstance(function_or_suboptions, types.FunctionType):
        function_or_suboptions()
    elif isinstance(function_or_suboptions, List):
        process_options(function_or_suboptions, True)
    else:
        process_options(options, False)


print_service.print_heading('sensor-am2302-history-client')
print_service.print_subheading('Please choose an option...')
process_options(all_options, True)
