import pytest
from django.conf import settings
from django.db import connections


@pytest.mark.django_db
def test_db_password_and_connection():
    engine = settings.DATABASES['default']['ENGINE']
    if engine.endswith('sqlite3'):
        pytest.skip('sqlite backend used')
    assert settings.DATABASES['default']['PASSWORD'], 'Database password should not be empty'
    with connections['default'].cursor() as cursor:
        cursor.execute('SELECT 1')
        assert cursor.fetchone()[0] == 1
