import pytest


@pytest.mark.xfail(reason='Тест падает из-за бага')
def test_with_bug():
    assert 1==2

@pytest.mark.xfail(reason='Баг исправлен, маркировка осталась')
def test_without_bug():
    pass

@pytest.mark.xfail(reason='Внешний сервис временном не доступен')
def test_external_service_is_unavailable():
    assert 1==2