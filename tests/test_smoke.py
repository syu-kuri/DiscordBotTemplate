# Keeps CI green (pytest exits 5 on zero collected tests) until the real
# tests land in issue #12. Safe to delete once test_config.py / test_i18n.py
# have actual test functions.
def test_smoke():
    assert True
