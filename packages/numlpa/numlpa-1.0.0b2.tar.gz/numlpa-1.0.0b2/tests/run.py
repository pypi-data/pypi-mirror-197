#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Test script.

This script executes the unit tests for the package.

"""

from contextlib import contextmanager, redirect_stdout
from json import load, dumps
from os import devnull
from pathlib import Path
from shutil import copytree, rmtree
from subprocess import CalledProcessError, DEVNULL, run
from tempfile import TemporaryDirectory, TemporaryFile
from unittest import main, TestCase

from numlpa import kits


dir_tests = Path(__file__).parent
dir_target = dir_tests/'target'

with open(dir_tests/'references.json', 'r', encoding='utf-8') as file:
    ref = load(file)


def runcheck(command):
    """Run a command and check the exit code.

    Parameters
    ----------
    command : str
        Command to be runned.

    Raises
    ------
    CalledProcessError
        If the command exited with an error code.

    """
    with TemporaryFile() as file:
        try:
            run(command, shell=True, check=True, stdout=file, stderr=file)
        except CalledProcessError as error:
           file.seek(0)
           raise RuntimeError(file.read().decode()) from error


@contextmanager
def temporary_target():
    """Return a temporary clone of the target test directory.

    Returns
    -------
    str
        Path to the cloned target directory.

    """
    temp_dir = TemporaryDirectory()
    path = Path(temp_dir.name)
    copytree(dir_target, path, dirs_exist_ok=True)
    try:
        yield path
    finally:
        temp_dir.cleanup()


class TestKits(TestCase):
    """Class for testing kits."""

    def test_distributions(self):
        """Test dislocation distributions."""
        self.maxDiff = None
        tested = kits.names('distributions')
        for name in tested:
            with self.subTest(name=name):
                distribution = kits.get('distributions', name)
                parameters = ref['distributions'][name]['parameters']
                dat = distribution.draw(**parameters)
                self.assertEqual(
                    ref['distributions'][name]['returns']['positions'],
                    dat['dislocations']['positions'],
                )
                self.assertEqual(
                    ref['distributions'][name]['returns']['senses'],
                    dat['dislocations']['senses'],
                )
                self.assertEqual(
                    ref['distributions'][name]['returns']['density'],
                    dat['distribution']['density'],
                )

    def test_diffractometers(self):
        """Test diffractometers."""
        self.maxDiff = None
        tested = kits.names('diffractometers')
        for name in tested:
            for kind in ('edge', 'edge',):
                with self.subTest(name=name, kind=kind):
                    params_key = f'parameters-{kind}'
                    return_key = f'returns-{kind}'
                    diffractometer = kits.get('diffractometers', name)
                    parameters = ref['diffractometers'][name][params_key]
                    dat = diffractometer.diffract(**parameters)
                    self.assertEqual(
                        ref['diffractometers'][name][return_key],
                        dat['coefficients'],
                    )

    def test_models(self):
        """Test LPA models."""
        tested = kits.names('models')
        for name in tested:
            transform = ref['models'][name]['parameters']['transform']
            harmonic = ref['models'][name]['parameters']['harmonic']
            parameters = ref['models'][name]['parameters']['parameters']
            model = kits.get('models', name)
            dat = model.model(transform, harmonic)(*parameters)
            self.assertEqual(
                ref['models'][name]['returns'],
                list(dat),
            )

class TestCommandLineInterface(TestCase):
    """Class for testing the command-line interface."""

    def test_draw(self):
        """Test draw command."""
        for distribution in kits.names('distributions'):
            with self.subTest(distribution=distribution):
                with temporary_target() as target:
                    runcheck(f"cd {target}; numlpa draw {distribution}")

    def test_diffract(self):
        """Test diffract command."""
        for diffractometer in kits.names('diffractometers'):
            with self.subTest(diffractometer=diffractometer):
                with temporary_target() as target:
                    runcheck(f"cd {target}; numlpa draw samples -n 1")
                    runcheck(f"cd {target}; numlpa diffract samples {diffractometer}")


if __name__ == '__main__':
    main()
