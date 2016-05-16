#!/usr/bin/env python

# Set the path
import os
import sys
from flask.ext.script import Manager, Server

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from blogservice import app

manager = Manager(app)

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    # use_debugger = True,
    use_reloader=True,
    host='0.0.0.0',
    port='5434'
    )
)

if __name__ == "__main__":
    manager.run()
