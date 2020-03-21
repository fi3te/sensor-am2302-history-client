import types
from abc import ABC
from typing import List

import backup_service
import plot_service
import print_service
import statistics_service


class Option(ABC):
    def __init__(self, key: str, description: str):
        self.key = key
        self.description = description


class ChoiceOption(Option):
    def __init__(self, key: str, description: str, suboptions: List[Option]):
        super().__init__(key, description)
        self.suboptions = suboptions


class ActionOption(Option):
    def __init__(self, key: str, description: str, action: types.FunctionType):
        super().__init__(key, description)
        self.action = action


all_options = [
    ActionOption('1', 'Backup files', backup_service.start_backup),
    ActionOption('2', 'Show backup statistics', statistics_service.show_statistics),
    ChoiceOption('3', 'Create plot', [
        ActionOption('1', 'Daily mean plot', plot_service.show_daily_mean_plot),
        ActionOption('2', 'Weekly mean plot', plot_service.show_weekly_mean_plot),
        ActionOption('3', 'Monthly mean plot', plot_service.show_monthly_mean_plot)
    ])
]


def process_options(options: List[Option]) -> None:
    print()
    for option in options:
        print(f'{option.key}) {option.description}')

    user_input = input('> ')
    dictionary = {option.key: option for option in options}
    chosen_option = dictionary.get(user_input)
    if isinstance(chosen_option, ChoiceOption):
        process_options(chosen_option.suboptions)
    elif isinstance(chosen_option, ActionOption):
        chosen_option.action()
    else:
        process_options(options)


def main() -> None:
    print_service.print_heading('sensor-am2302-history-client')
    print_service.print_subheading('Please choose an option...')
    process_options(all_options)


if __name__ == '__main__':
    main()
