"""
Main module file, used for managing and starting application server.
"""


from flask_script import Manager

from app import APP


# application command manager
manager = Manager(APP)

# main server loop
if __name__ == "__main__":
    manager.run()