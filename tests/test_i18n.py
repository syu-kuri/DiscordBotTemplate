from bot.core import i18n


def test_english_and_japanese_locales_have_identical_keys() -> None:
    assert set(i18n._TRANSLATIONS["en"]) == set(i18n._TRANSLATIONS["ja"])


def test_unknown_key_returns_key() -> None:
    unknown_key = "unknown.translation.key"

    assert i18n.t(unknown_key) == unknown_key


def test_unknown_locale_falls_back_to_english() -> None:
    assert (
        i18n.t("general.help.description", locale="unknown")
        == "Show available commands."
    )
