import re
import types
from abc import ABC
from argparse import ArgumentParser
from datetime import datetime
from typing import List, Optional, Pattern

import argh

import backup_service
import constants
import print_service
import statistics_service
from plot.plotly_service import PlotlyService

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


plot_service = PlotlyService()

all_options = [
    ActionOption('1', 'Backup files', backup_service.start_backup),
    ActionOption('2', 'Show backup statistics', statistics_service.show_statistics, INTERVAL_ARGUMENT_DEFINITION),
    ChoiceOption('3', 'Create plot', [
        ActionOption('1', 'Raw plot', plot_service.show_raw_plot, INTERVAL_ARGUMENT_DEFINITION),
        ActionOption('2', 'Hourly mean plot', plot_service.show_hourly_mean_plot, INTERVAL_ARGUMENT_DEFINITION),
        ActionOption('3', 'Daily mean plot', plot_service.show_daily_mean_plot, INTERVAL_ARGUMENT_DEFINITION),
        ActionOption('4', 'Weekly mean plot', plot_service.show_weekly_mean_plot, INTERVAL_ARGUMENT_DEFINITION),
        ActionOption('5', 'Monthly mean plot', plot_service.show_monthly_mean_plot, INTERVAL_ARGUMENT_DEFINITION)
    ])
]


def _request_argument(argument: ArgumentDefinition):
    print_service.print_subheading(
        f'{argument.description} ({argument.pattern_hint}, default value: {argument.default_value})')
    while True:
        user_input = input('> ')
        if user_input == '':
            return argument.default_value
        elif re.fullmatch(argument.pattern, user_input):
            return argument.cast(user_input)


def _process_options(options: List[Option]) -> None:
    print()
    for option in options:
        print(f'{option.key}) {option.description}')

    user_input = input('> ')
    dictionary = {option.key: option for option in options}
    chosen_option = dictionary.get(user_input)
    if isinstance(chosen_option, ChoiceOption):
        _process_options(chosen_option.suboptions)
    elif isinstance(chosen_option, ActionOption):
        if chosen_option.arguments:
            arguments = []
            for argument in chosen_option.arguments:
                arguments.append(_request_argument(argument))
            chosen_option.action(*arguments)
        else:
            chosen_option.action()
    else:
        _process_options(options)


@constants.add_parameters
def default() -> None:
    print_service.print_subheading('Please choose an option...')
    _process_options(all_options)


@argh.named('backup')
@constants.add_parameters
def backup() -> None:
    backup_service.start_backup()


def main() -> None:
    print_service.print_heading('sensor-am2302-history-client')
    parser = ArgumentParser()
    argh.add_commands(parser, [backup])
    argh.set_default_command(parser, default)
    argh.dispatch(parser)


if __name__ == '__main__':
    main()
