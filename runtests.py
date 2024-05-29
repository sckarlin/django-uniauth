#!/usr/bin/env python
import os
import sys
from pathlib import Path
from typing import NoReturn, List, Optional

import django
from django.conf import settings
from django.test.utils import get_runner


def usage(message: str = '') -> NoReturn:
    exit_value = 0
    if message:
        print(message)
        exit_value = 1
    print("Usage: python runtests.py [test_labels]")
    sys.exit(exit_value)


def get_test_labels(argv: Optional[List[str]] = None) -> List[str]:
    if argv is None:
        argv = sys.argv
    if len(argv) > 1:
        if ('-h' in argv[1:]) or ('--help' in argv[1:]):
            usage()
        labels = []
        for label in argv[1:]:
            if not label.startswith('test_'):
                usage('test_labels must start with "test_"')
            file_path = Path('tests') / f'{label}.py'
            if not file_path.exists():
                usage(f'{file_path} for test_label "{label}" does not exist')
            labels.append(f'tests.{label}')
    else:
        labels = ['tests']
    return labels


def main() -> int:
    test_labels = get_test_labels()
    os.environ['DJANGO_SETTINGS_MODULE'] = "tests.settings"
    django.setup()
    test_runner_class = get_runner(settings)
    test_runner = test_runner_class()
    num_failures = test_runner.run_tests(test_labels=test_labels)
    return 0 if num_failures == 0 else 1


if __name__ == "__main__":
    retval = main()
    sys.exit(retval)
