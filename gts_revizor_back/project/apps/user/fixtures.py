import pytest
from mixer.backend.django import mixer


@pytest.fixture
def user():
    return mixer.blend('user.User')
