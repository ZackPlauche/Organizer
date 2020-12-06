import shutil
import settings
from pathlib import *

# Browse through every file and folder

class Organizer:

    def __init__(self, base_dir=settings.BASE_DIR, ignore_dirs=settings.IGNORE_DIRS):
        self.base_dir = Path(base_dir)
        self.ignore_dirs = ignore_dirs

    def browse_files(file_type='', is_dir=False):   

        def real_browse_files(method):
            """Browse through every file & folder before running method"""

            def wrapper(self, *args, **kwargs):
                for i in self.base_dir.glob(f'**/*{file_type}'):
                    if not any(directory in str(i.absolute()) for directory in self.ignore_dirs):
                        if is_dir == True:
                            if i.is_dir():
                                method(self, i, *args, **kwargs)
                        else: 
                            method(self, i, *args, **kwargs)
            return wrapper
        return real_browse_files

    @browse_files()
    def remove_files(self, file_object, file_type=False, file_contains=False):
        """Remove files of a specific type"""
        file_name = file_object.name
        if file_type and file_contains:
            if file_name.endswith(file_type) or file_contains in file_name:
                file_object.unlink()
        else:
            if file_type:
                if file_name.endswith(file_type):
                    file_object.unlink()
            elif file_contains:
                if file_contains in file_name:
                    file_object.unlink()

    @browse_files(is_dir=True)
    def clean_folders(self, folder):
        """Remove all empty folders in directory tree"""
        if not next(folder.iterdir(), None):
            folder.rmdir()

    @browse_files()
    def copy_files(self, file_object, folder_name: str, file_types: tuple):
        """Copy all files of desired file types into a desired folder"""

        destination_folder = self.base_dir / folder_name
        if not destination_folder.exists():
            # destination_folder.mkdir()
            print('Make deestination folder (hypothetically...)')

        # Check if file is in desired file types
        if file_object.name.lower().endswith(file_types):
            # TODO: Check if file with the same name already exists

            # Copy file into destination folder
            # shutil.copy(file_object, destination_folder)
            print(file_object.name)

    @browse_files()
    def list_files(self, file_object, file_type=None):
        if file_type:
            if file_object.name.endswith(file_type):
                print(f'{file_object.name}')
        else:
            ftype = 'DIRECTORY' if file_object.is_dir() else 'FILE'
            print(f'{ftype}: {file_object.name}')


def main():
    pass

if __name__ == '__main__':
    main()