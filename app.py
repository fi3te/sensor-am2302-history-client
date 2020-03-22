import re
import types
from abc import ABC
from datetime import datetime
from typing import List, Optional, Pattern

import backup_service
import plot_service
import print_service
import statistics_service

DATE_PATTERN = r'^(3[01]|[12][0-9]|0[1-9])\.(1[012]|0[1-9])\.(20[0-9]{2})$'


class ArgumentDefinition(ABC):
    def __init__(self, description: str, pattern_hint: str, pattern: Pattern, cast: types.FunctionType,
                 default_value=None):
        self.description = description
        self.pattern_hint = pattern_hint
        self.pattern = pattern
        self.cast = cast
        self.default_value = default_value


class DateArgumentDefinition(ArgumentDefinition):
    def __init__(self, description: str):
        super().__init__(description, 'dd.mm.yyyy', re.compile(DATE_PATTERN),
                         lambda x: datetime.strptime(x, '%d.%m.%Y').date())


INTERVAL_ARGUMENT_DEFINITION = [DateArgumentDefinition('From'), DateArgumentDefinition('To')]


class Option(ABC):
    def __init__(self, key: str, description: str):
        self.key = key
        self.description = description


class ChoiceOption(Option):
    def __init__(self, key: str, description: str, suboptions: List[Option]):
        super().__init__(key, description)
        self.suboptions = suboptions


class ActionOption(Option):
    def __init__(self, key: str, description: str, action,
                 arguments: Optional[List[ArgumentDefinition]] = None):
        super().__init__(key, description)
        self.action = action
        self.arguments = arguments


all_options = [
    ActionOption('1', 'Backup files', backup_service.start_backup),
    ActionOption('2', 'Show backup statistics', statistics_service.show_statistics, INTERVAL_ARGUMENT_DEFINITION),
    ChoiceOption('3', 'Create plot', [
        ActionOption('1', 'Daily mean plot', plot_service.show_daily_mean_plot),
        ActionOption('2', 'Weekly mean plot', plot_service.show_weekly_mean_plot),
        ActionOption('3', 'Monthly mean plot', plot_service.show_monthly_mean_plot)
    ])
]


def request_argument(argument: ArgumentDefinition):
    print_service.print_subheading(
        f'{argument.description} ({argument.pattern_hint}, default value: {argument.default_value})')
    while True:
        user_input = input('> ')
        if user_input == '':
            return argument.default_value
        elif re.fullmatch(argument.pattern, user_input):
            return argument.cast(user_input)


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
        if chosen_option.arguments:
            arguments = []
            for argument in chosen_option.arguments:
                arguments.append(request_argument(argument))
            chosen_option.action(*arguments)
        else:
            chosen_option.action()
    else:
        process_options(options)


def main() -> None:
    print_service.print_heading('sensor-am2302-history-client')
    print_service.print_subheading('Please choose an option...')
    process_options(all_options)


if __name__ == '__main__':
    main()
