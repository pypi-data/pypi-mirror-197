# flake8: noqa
from tests.helpers import (test_path, bigger_files_path,
                           corrupted_path, namespaced_path)
from pyi18n import loaders


def test_loaders_yaml_loader():
    loader = loaders.PyI18nYamlLoader(test_path)
    locales: tuple = ("en", "pl")
    loaded_locales = loader.load(locales)
    assert loaded_locales != {}
    assert tuple(loaded_locales.keys()) == locales
    assert loader._type == "yaml"


def test_loaders_yaml_loader_with_invalid_path():
    loader = loaders.PyI18nYamlLoader("some_invalid_path/")
    locales: tuple = ("en", "pl")
    loaded_locales = loader.load(locales)
    assert loaded_locales == {}
    assert loader._type == "yaml"


def test_loaders_json_loader_corrupted_yaml() -> None:
    loader = loaders.PyI18nYamlLoader(test_path)
    locales: tuple = ("pl")
    loaded_locales = loader.load(locales)
    assert not loaded_locales
    assert loader._type == "yaml"


def test_loaders_yaml_loader_with_non_existing_locale():
    loader = loaders.PyI18nYamlLoader(test_path)
    locales: tuple = ("en", "pl", "ru")
    loaded_locales = loader.load(locales)
    assert loaded_locales.keys() != locales
    assert tuple(loaded_locales.keys()) == ("en", "pl")
    assert loader._type == "yaml"


def test_loaders_yaml_loader_without_any_locale():
    loader = loaders.PyI18nYamlLoader(test_path)
    loaded_locales = loader.load(())
    assert loaded_locales == {}
    assert loader._type == "yaml"


def test_loaders_json_loader():
    loader = loaders.PyI18nJsonLoader(test_path)
    locales: tuple = ("en", "pl")
    loaded_locales = loader.load(locales)
    assert loaded_locales != {}
    assert tuple(loaded_locales.keys()) == locales
    assert loader._type == "json"


def test_loaders_json_loader_corrupted_json() -> None:
    loader = loaders.PyI18nJsonLoader(test_path)
    locales: tuple = ("pl")
    loaded_locales = loader.load(locales)
    assert not loaded_locales
    assert loader._type == "json"


def test_loaders_json_loader_with_invalid_path():
    loader = loaders.PyI18nJsonLoader("some_invalid_path/")
    locales: tuple = ("en", "pl")
    loaded_locales = loader.load(locales)
    assert loaded_locales == {}
    assert loader._type == "json"


def test_loaders_json_loader_with_non_existing_locale():
    loader = loaders.PyI18nJsonLoader(test_path)
    locales: tuple = ("en", "pl", "ru")
    loaded_locales = loader.load(locales)
    assert loaded_locales.keys() != locales
    assert tuple(loaded_locales.keys()) == ("en", "pl")
    assert loader._type == "json"


def test_loaders_json_loader_without_any_locale():
    loader = loaders.PyI18nJsonLoader(test_path)
    loaded_locales = loader.load(())
    assert loaded_locales == {}
    assert loader._type == "json"


def test_loaders_json_bigger_files():
    loader = loaders.PyI18nJsonLoader(bigger_files_path)
    locales: tuple = ("en",)
    loaded_locales = loader.load(locales)
    assert loaded_locales != {}
    assert loader._type == "json"

def test_loader_yml_namespaced():
    loader = loaders.PyI18nYamlLoader(namespaced_path, namespaced=True)
    locales: tuple = ('en_US', 'de_DE')
    loaded_locales = loader.load(locales)
    assert loaded_locales != {}
    assert loader._type == "yml"
    assert loaded_locales.keys() == list(locales)
