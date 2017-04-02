from argparse import Namespace
from logging import DEBUG, INFO

import pytest

from eleanorrigbot import parse_args


DEFAULTS = dict(location=[-3.0087, 53.3261, -2.8180, 53.4751], log_level=INFO)


def build_namespace(**kwargs):
    namespace = DEFAULTS.copy()
    namespace.update(kwargs)
    return Namespace(**namespace)


@pytest.mark.parametrize('args, namespace', [
    ([], build_namespace()),
    (['-v'], build_namespace(log_level=DEBUG)),
    (['--verbose'], build_namespace(log_level=DEBUG)),
    (['-l', '1', '2', '3', '4'], build_namespace(location=[1, 2, 3, 4])),
    (
            ['--location', '1', '2', '3', '4'],
            build_namespace(location=[1, 2, 3, 4]),
    ),
    (
        ['--verbose', '-l', '1.23', '4.56', '7.89', '10.00'],
        build_namespace(location=[1.23, 4.56, 7.89, 10.0], log_level=DEBUG)
    )
])
def test_arg_parsing(args, namespace):
    assert(parse_args(args)) == namespace


def test_arg_version():
    with pytest.raises(SystemExit) as exc:
        parse_args(['--version'])
    assert exc.value.code == 0


@pytest.mark.parametrize('args', [
    ['-l', '1', '2', '3'],
    ['-l', 'foo', 'bar', 'baz', 'bang'],
])
def test_parse_failure(args):
    with pytest.raises(SystemExit) as exc:
        parse_args(args)
    assert exc.value.code == 2
