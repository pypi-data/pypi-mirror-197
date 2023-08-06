from os.path import exists, join, splitext, basename
from os import listdir, stat
import json
import yaml


class LoaderType:
    """ Enum for the different loader types. """
    BASE: str = "base"
    YAML: str = "yaml"
    JSON: str = "json"


class PyI18nBaseLoader:
    """ PyI18n Base Loader class, supports yaml and json

    Attributes:
        load_path (str): path to translations
        _type (str): loader type

    Methods:
        load (tuple, object) -> dict: load translations for given
                                locales and returns as python dict
        type () -> str: return loader type
        get_path () -> str: return loader path
        __load_file (str, str, object, str) -> dict: return file content

    """

    _type: str = LoaderType.BASE

    def __init__(self, load_path: str = "locales/", namespaced: bool = False) -> None:
        """ Initialize loader class

        Args:
            load_path (str): path to translations

        Returns:
            None

        """
        self.load_path: str = load_path
        self.namespaced: bool = namespaced

    def load(self, locales: tuple, ser_mod: object) -> dict:
        """ Load translations for given locales,
            should be overridden in child classes.

        Args:
            locales (tuple): locales to load

        Returns:
            dict: loaded translations

        Notes:
            Custom load function should be implemented
            in child classes and return python dict

        """

        file_extension: str = ser_mod.__name__.replace('yaml', 'yml')

        loaded: dict = {}
        for locale in locales:

            file_path: str = f"{self.load_path}{locale}.{file_extension}"
            if not exists(file_path):
                continue

            try:
                loaded[locale] = self.__load_file(file_path,
                                                  file_extension,
                                                  ser_mod,
                                                  locale
                                                  )
            except (json.decoder.JSONDecodeError, yaml.YAMLError):
                continue

        return loaded

    def __load_file(self,
                    file_path: str,
                    ext: str,
                    ser_mod: object,
                    locale: str
                    ) -> dict:
        """ loads content, should not be called directly

        Returns:
            dict: loaded content

        """
        with open(file_path, 'r', encoding="utf-8") as _f:
            load_params: dict = {"Loader": yaml.FullLoader} \
                if ext == "yml" else {}

            return ser_mod.load(_f, **load_params)[locale]

    def __load_namespaced(self, locales: tuple, ser_mod: object) -> dict:
        """ Load translations from namespaces should be overridden in child classes. This will be looking for a locale (directories) and load all namespaces.

        Args:
            locales (tuple): locales to load
            ser_mod (object): module to serialize

        Returns:
            dict: loaded translations

        Notes:
            Custom load function should be implemented
            in child classes and return python dict

        """
        loaded: dict = {}
        for locale in locales:
            path: str = join(self.load_path, locale)

            if not exists(path):
                print(f"[WARNING] path {path} doesn't exist, probably you forgot to add to the available locales list.")
                continue

            for file in listdir(path):
                if file.endswith('.yml'):
                    filepath: str = join(path, file)
                    namespace: str = splitext(basename(filepath))[0]

                    # file is empty, should continue
                    if stat(filepath).st_size == 0:
                        continue

                    with open(filepath, 'r', encoding="utf-8") as _file:
                        locale_content: object = ser_mod.load(_file)

                        if locale not in loaded:
                            loaded[locale] = {}
                        loaded[locale][namespace] = locale_content

        return loaded

    def type(self) -> str:
        """ Return loader type

        Returns:
            str: loader type

        """
        return self._type

    def get_path(self) -> str:
        """ Return loader path

        Returns:
            str: loader path

        """
        return self.load_path


class PyI18nJsonLoader(PyI18nBaseLoader):
    """ PyI18n JSON Loader class

    Attributes:
        load_path (str): path to translations
        _type (str): loader type

    Methods:
        load (tuple, object) -> dict: load translations for given
                                locales and returns as python dict
        type () -> str: return loader type
        get_path () -> str: return loader path
    """

    _type: str = LoaderType.JSON

    def load(self, locales: tuple) -> dict:
        """ Load translations for given locales using json

        Inherits from PyI18nBaseLoader

        Args:
            locales (tuple): locales to load
            namespaced (bool): tells loader should look for namespaces

        Returns:
            dict: loaded translations

        """

        if self.namespaced:
            return self.__load_namespaced(locales, yaml)

        return super().load(locales, json)

    def __load_namespaced(self, locales: tuple, ser_mod: object) -> dict:
        return super().__load_namespaced(locales, ser_mod)


class PyI18nYamlLoader(PyI18nBaseLoader):
    """ PyI18n YAML Loader class

    Attributes:
        load_path (str): path to translations
        _type (str): loader type

    Methods:
        load (tuple, object) -> dict: load translations for given
                                locales and returns as python dict
        type () -> str: return loader type
        get_path () -> str: return loader path
    """

    _type: str = LoaderType.YAML

    def load(self, locales: tuple) -> dict:
        """ Load translations for given locales using yaml

        Inherits from PyI18nBaseLoader

        Args:
            locales (tuple): locales to load
            namespaced (bool): tells loader should look for namespaces

        Returns:
            dict: loaded translations

        """
        if self.namespaced:
            return self.__load_namespaced(locales, yaml)

        return super().load(locales, yaml)

    def __load_namespaced(self, locales: tuple, ser_mod: object) -> dict:
        return super().__load_namespaced(locales, ser_mod)
