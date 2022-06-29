import json
import os.path
from tempfile import TemporaryDirectory

import pytest

from cli import main
from tests.utils import PROJECT_DIR, TEST_DIR


@pytest.fixture
def cli():
    return os.path.join(PROJECT_DIR, "cli.py")


@pytest.fixture
def data():
    def create_path(filename):
        return os.path.join(TEST_DIR, "data", filename)

    return create_path


@pytest.fixture
def locale():
    return TemporaryDirectory()


def test_update_translation_file_from_file(cli, data, locale):
    main(f"{data('a.py')} --locale {locale.name} -d".split())

    with open(os.path.join(locale.name, "en.json")) as fh:
        en = json.load(fh)

    assert {
        "a-1": "",
        "a-2": "",
        "a-3": "",
        "a-4": "",
    } == en


def test_update_translation_file_from_file_with_lang(cli, data, locale):
    main(f"{data('a.py')} --locale {locale.name} --lang de -d".split())

    with open(os.path.join(locale.name, "de.json")) as fh:
        en = json.load(fh)

    assert {
        "a-1": "",
        "a-2": "",
        "a-3": "",
        "a-4": "",
    } == en


def test_update_translation_file_from_dir(cli, data, locale):
    main(f"{os.path.join(TEST_DIR, 'data')} --locale {locale.name} --lang en".split())

    with open(os.path.join(locale.name, "en.json")) as fh:
        en = json.load(fh)

    assert {
        "a-1": "",
        "a-2": "",
        "a-3": "",
        "a-4": "",
        "b-1": "",
        "b-2": "",
        "b-3": "",
        "b-4": "",
    } == en

    # do not overwrite existing keys
    with open(os.path.join(locale.name, "en.json"), "wt") as fh:
        en["a-1"] = "some-translation"
        json.dump(en, fh)

    main(f"{os.path.join(TEST_DIR, 'data')} --locale {locale.name} --lang en".split())

    with open(os.path.join(locale.name, "en.json")) as fh:
        en = json.load(fh)

    assert {
        "a-1": "some-translation",
        "a-2": "",
        "a-3": "",
        "a-4": "",
        "b-1": "",
        "b-2": "",
        "b-3": "",
        "b-4": "",
    } == en


def test_fail_if_locale_are_invalid():
    with pytest.raises(SystemExit):
        main(
            f"{os.path.join(TEST_DIR, 'data')} --locale ./invalid/path --lang en".split()
        )
