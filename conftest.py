# pylint: disable=C0114, W0613, C0116, C0115
import pytest
import requests


@pytest.fixture
def requests_mock(monkeypatch):
    class MockResponse:
        def __init__(self, text):
            self.text = text
            self.content = text.encode('utf-8')

    def mock_get(*args, **kwargs):
        return MockResponse('Mocked response')

    monkeypatch.setattr(requests, 'get', mock_get)
