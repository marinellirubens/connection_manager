"""Method to handle requests to the server."""
from flask import Flask
from singleton_decorator import singleton


@singleton
class App(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
