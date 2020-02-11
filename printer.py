import math

_border_char = '='
_progress_char = '-'
_number_of_spaces = 20
_default_line_width = 60


def _line_width(text: str, fixed_line_width: bool) -> int:
    if fixed_line_width:
        return _default_line_width
    else:
        return len(text) + 2 + 2 * _number_of_spaces


def _spaces(text: str, fixed_line_width: bool) -> str:
    if fixed_line_width:
        return ' ' * ((_default_line_width - 2 - len(text))//2)
    else:
        return ' ' * _number_of_spaces


def print_heading(text: str, fixed_line_width: bool = True) -> None:
    line_width = _line_width(text, fixed_line_width)
    spaces = _spaces(text, fixed_line_width)
    spaces_left = spaces
    spaces_right = spaces if len(text) % 2 == 0 else spaces + ' '
    print()
    print(_border_char * line_width)
    print('|' + spaces_left + text + spaces_right + '|')
    print(_border_char * line_width)


def print_subheading(text: str) -> None:
    print()
    print(text)


def show_progress_bar(position: int, max_position: int) -> None:
    position = max(0, position)
    max_position = max(1, position, max_position)
    progress_bar_width = _default_line_width - 2
    progress = math.floor(progress_bar_width * position / max_position)
    bar_text = _progress_char * progress + ' ' * (progress_bar_width - progress)
    print('\r|%s|' % bar_text, end='')
    if position == max_position:
        print()
