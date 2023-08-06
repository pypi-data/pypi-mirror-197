import os


class SaveFile:
    """a class to save file"""

    @staticmethod
    def mkdir(path):
        """Create directory"""
        try:
            if not os.path.exists(path):
                os.mkdir(path)
            else:
                print(f" * Directory %s already exists = {path}")
        except OSError as err:
            raise OSError(f"{err}")
