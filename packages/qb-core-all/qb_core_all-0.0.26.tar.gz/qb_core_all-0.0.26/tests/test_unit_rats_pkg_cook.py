"""
this tests cases and conditions that business scenarios cannot cover easily
ideal for odd error cases, edge cases
"""
import pytest

from qb_core.common.plugin.plugin_manager import PluginManager
from qb_core.rats_pkg.cook.cook_model import Cook, CookAdded, CookRemoved
from qb_core.rats_pkg.cook.cook_persistence_plug_point import CookPersistenceInterface

_cook_persistence = None


@pytest.fixture()
def setup_cook_persistence():
    # making sure the test always starts with empty list
    global _cook_persistence
    _cook_persistence = PluginManager.get_plugin("cook_persistence_plug_point")
    _cook_persistence.clear_all()

    yield
    # making sure the test cleans up to an empty list
    _cook_persistence.clear_all()


def test_cook_model():
    """this test is for testing str and repr methods"""
    cook = Cook()

    cook.init(name="nala paaka", email="np@unreal.com")
    assert str(cook) == "self.name='nala paaka', self.email='np@unreal.com'"
    assert repr(cook) == '{"name": "nala paaka", "email": "np@unreal.com"}'

    cook_removed = CookRemoved(cook)
    assert str(cook_removed) == 'self.cook={"name": "nala paaka", "email": "np@unreal.com"}'
    assert repr(cook_removed) == '{"cook": "self.name=\'nala paaka\', self.email=\'np@unreal.com\'"}'


def test_cook_persistence(setup_cook_persistence):
    """this test is for testing methods not commonly used"""
    assert _cook_persistence.read_cook_count() == 0

    expected_cook = Cook()
    expected_cook.init(name="nala paaka", email="np@unreal.com")

    actual_cook = _cook_persistence.read_cook("nala paaka")
    assert actual_cook is None

    _cook_persistence.save_cook(expected_cook)
    actual_cook = _cook_persistence.read_cook("nala paaka")
    assert actual_cook == expected_cook

    _cook_persistence.print_all()


def test_cook_persistence_plug_point():
    """since this is like an abstract class, business scenarios will not reach this code"""
    obj = CookPersistenceInterface()
    assert obj.read_cook_count() is None
    assert obj.read_cook("dont_care") is None
    assert obj.save_cook("dont_care") is None
    assert obj.remove_cook("dont_care") is None
    assert obj.print_all() is None
