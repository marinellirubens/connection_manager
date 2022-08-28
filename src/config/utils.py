"""Module to contain all the utility functions for the application."""
import os


def create_directories(directories):
    # directories = ['logs', 'files', 'sqlite']

    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
