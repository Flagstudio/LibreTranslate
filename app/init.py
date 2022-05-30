from pathlib import Path

import polyglot
from argostranslate import package, translate

import app.language


def boot(load_only=None):
    try:
        check_and_install_models(load_only_lang_codes=load_only)
        check_and_install_transliteration()
    except Exception as e:
        print("Cannot update models (normal if you're offline): %s" % str(e))


def check_and_install_models(force=False, load_only_lang_codes=None):
        download_path = 'translate-ru_en-1_0.argosmodel'
        package.install_from_path(download_path)

        print('Starting to install language model')
        # reload installed languages
        app.language.languages = translate.load_installed_languages()
        print('End to install language model')


def check_and_install_transliteration(force=False):
    # 'en' is not a supported transliteration language
    transliteration_languages = [
        l.code for l in app.language.languages if l.code != "en"
    ]

    print('Transliteration start')
    # check installed
    install_needed = []
    if not force:
        t_packages_path = Path(polyglot.polyglot_path) / "transliteration2"
        for lang in transliteration_languages:
            if not (
                t_packages_path / lang / f"transliteration.{lang}.tar.bz2"
            ).exists():
                install_needed.append(lang)
    else:
        install_needed = transliteration_languages

    print('Transliteration mid')

    # install the needed transliteration packages
    if install_needed:
        print('ATTENTION! INSTALL IS NEEDING')

        print(
            f"Installing transliteration models for the following languages: {', '.join(install_needed)}"
        )

        from polyglot.downloader import Downloader

        downloader = Downloader()

        for lang in install_needed:
            downloader.download(f"transliteration2.{lang}")
            print('transliteration end maybe')
