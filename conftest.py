import os
import sys
import pytest
import django

# get the absolute path of the project root
# this is important or pytest gets lost 🧭
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# add the project root to the python path
# without this, imports break and everything dies 💀
sys.path.insert(0, PROJECT_ROOT)

# configure django settings
# super important to use test settings here!
# no queremos romper la db de prod por accidente 😱
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.test_settings')
django.setup()

@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    # this runs once before all tests
    # prepara todo para que los tests no fallen 🙏
    with django_db_blocker.unblock():
        # run migrations fresh every time
        # yes, it's slow, but it's safer this way 🐌
        from django.core.management import call_command
        call_command('migrate')






