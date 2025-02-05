# -*- coding: utf-8 -*-
from src.helpers.remove_folder import remove_folder
from src.open_file import open_file
import os
import subprocess


class CloneFlutter:
    def __rename_dir(self, path_flutter: str, label: str, version_label: str):
        flutter_current_version_name = open_file(path_flutter + f'{label}/{version_label}', is_print=False)
        os.chdir(path_flutter)
        try:
            os.rename(label, flutter_current_version_name)
        except Exception as e:
            print(f'Error {e}')

    def __set_file_version(self, path_flutter: str, label, version: str):
        new_path = os.path.join(path_flutter, label, "version")
        with open(new_path, 'w') as f:
            f.write(version.replace(" ", ""))

    def clone(self, path_flutter, version: str, label: str, version_label: str):
        try:
            self.__rename_dir(path_flutter=path_flutter, label=label, version_label=version_label)
        except FileNotFoundError:
            pass
        print('Please await, for the requested version ...\n')
        result = subprocess.run(
            f"git clone -b stable https://github.com/flutter/flutter.git {os.path.join(path_flutter, label)} --depth 1 --branch {version}",
            capture_output=True, text=True, shell=True)

        print('Running flutter doctor -v\n')
        subprocess.run("flutter doctor -v", capture_output=True, text=True, shell=True)

        if result.returncode == 0:
            print("Naming version\n")
            self.__set_file_version(path_flutter=path_flutter, label=label, version=version)
            print("Freeing up space ...\n")
            remove_folder(os.path.join(path_flutter, label, 'examples'))
            print('Completed Successfully!\n')
            print(f'The current version is {version}')

        else:
            print(result.stderr)
