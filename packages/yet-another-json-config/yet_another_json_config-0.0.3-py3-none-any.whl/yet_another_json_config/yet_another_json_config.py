"""
Reads and write json files as a configuration file, supports nested json values.
"""
import json
import os
from typing import Union

class Config():
    def __init__(self, config_file_path: str, file_must_exist: bool = False):
        """
        Create an instance of a configuration file.

        Args:
        config_file_path (str): The path to the configuration file.
        file_must_exist (bool, Optional): Raises a FileNotFoundError exception if file does not exist. Default value is 'False'.
        """

        # if file exists, attempt to load it
        # otherwise assume new config file
        if os.path.exists(config_file_path):
            if os.path.isfile(config_file_path):
                self._config_file_path = config_file_path

                self._load()
            else:
                raise FileNotFoundError(f'Config File {config_file_path} is not a file.')
        elif file_must_exist == False:
            # check that the file path is valid by attempting to open it real quick
            try:
                with open(config_file_path, 'x') as tempfile: # OSError if file exists or is invalid
                    pass
            except FileNotFoundError as e:
                pass

            self._settings = {}
            self._config_file_path = config_file_path
        else:
            raise FileNotFoundError(f'Config File {config_file_path} does not exist.')

    def _load(self):
        """
        Loads the configuration file.
        """

        if os.path.exists(self._config_file_path):
            # Open Config File, read the json information and close the file
            with open(self._config_file_path, 'r', encoding = 'utf-8') as f:

                settings = json.loads(f.read())

            self._settings = settings
        else:
            raise FileNotFoundError(f'Config File {self._config_file_path} does not exist.')

    def save(self, indent: int = 4):
        """
        Saves the configuration file.
        """
        with open(self._config_file_path, "w", encoding='utf-8') as out_file:
            json.dump(self._settings, out_file, indent = indent)

    def get(self, *keys: str):
        """
        Returns the specified setting.
        """

        return self._action(keys, action='get')

    def set(self, *keys: str, value):
        """
        Sets the specified setting.
        """

        self._action(keys, action='set', value=value)

    def delete(self, *keys: str):
        """
        Deletes the specified setting.
        """

        self._action(keys, action='delete')

    def exists(self, *keys: str) -> bool:
        """
        Returns a boolean if a setting exists.
        """

        return self._action(keys, action='exists')

    def settings(self):
        """
        Returns the current settings.
        """

        return self._settings

    def _action(self, keys, action: str, value = None):
        """
        Perform an action on a setting.

        Args:
        keys (Tuple[Union[str, Tuple[str, ...]]]): A list of keys that specify the path to the
            value to be accessed or modified in the dictionary. Each key in the list is either
            a string or a tuple of strings. If a tuple is used, it represents a sub-path within
            the dictionary.
        action (str): A string that specifies the action to be performed on the dictionary.
            Valid actions are 'get', 'set', 'delete', and 'exists'.
        value (Any, optional): The value to be used in conjunction with the 'set' action.
            This argument is ignored for all other actions. If the 'set' action is specified and
            `value` is not provided, a TypeError is raised.
        """

        if action not in ['get', 'set', 'exists', 'delete']:
            raise ValueError(f"{action} was not a valid action. Only 'get', 'set', 'exists', and 'delete' can be used.")

        action_text = action

        # Pull off plural, only for exists action for now
        if action[-1] == 's':
            action_text = action[:-1]

        if keys == ():
            raise KeyError(f'No key specified to {action_text}.')

        # Convert based on being a tuple or not
        if type(keys[0]) == tuple:
            print(keys)
            keys_list = list(*keys)
        else:
            keys_list = list(keys)

        if len(keys_list) == 0:
            raise KeyError(f'No key specified to {action_text}.')

        data = self._settings

        last_key = keys_list[-1]

        if last_key == []:
            raise KeyError(f'No key specified to {action_text}.')

        # When assigning drill down to *second* last key
        for k in keys_list[:-1]:
            if k in data:
                data = data[k]
            else:
                if action != 'exists':
                    raise KeyError(f'Setting {k} does not exist.')
                else:
                    return False

        # based on action, respond differently to the setting
        if action == 'get':
            return data[last_key]
        elif action == 'set':
            data[last_key] = value
        elif action == 'exists':
            if last_key in data:
                return True
            else:
                return False
        elif action == 'delete':
            if last_key in data:
                del data[last_key]
            else:
                raise KeyError(f'Setting {last_key} does not exist and cannot be deleted.')

    def __str__(self):
        return str(self._settings)

    def __repr__(self):
        return str(self._settings)

    def __getitem__(self, item: Union[str, tuple, list]):
        return self.get(item)

    def __setitem__(self, item: Union[str, tuple, list], value):
        self.set(item, value=value)

    def __delitem__(self, item: Union[str, tuple, list]):
        self.delete(item)

    def __contains__(self, item: Union[str, tuple, list]):
        return self.exists(item)

    def __len__(self):
        return len(self._settings)
