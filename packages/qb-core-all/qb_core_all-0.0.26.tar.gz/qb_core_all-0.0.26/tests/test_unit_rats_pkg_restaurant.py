import pytest

from qb_core.rats_pkg.cook import cook_persistence_core
from qb_core.rats_pkg.cook.cook_model import Cook, CookAdded, CookRemoved
from qb_core.rats_pkg.restaurant import _restaurant_persistence
from qb_core.rats_pkg.restaurant.restaurant_model import Restaurant


def test_restaurant_model():
    restaurant = Restaurant()

    restaurant.init(name="n", address="a",
                    cuisine_type="ct", rating="r",
                    status="s", manager_name="mn",
                    manager_email="me")
    assert str(restaurant) == "self.name='n', self.manager_name='mn', me"
    assert repr(restaurant) == '{"name": "n", "address": "a", ' \
                               '"cuisine_type": "ct", "rating": "r", ' \
                               '"status": "s", "manager_name": "mn", ' \
                               '"manager_email": "me", "verification_code": null, ' \
                               '"verification_valid_till": null, "cook_dict": {}}'


# is this needed?
# just trigger something to get 100% coverage.
# i am not sure if this is needed
# it will be nice if i can roll it with main functioal test
def test_save_self_verification_code():
    restaurant = Restaurant()
    restaurant.save_verification_code("1234")
    assert restaurant.verification_code == "1234"
    assert restaurant.status == "pending_verification"


@pytest.fixture()
def setup_restaurant_persistence():
    # making sure the test always starts with empty list
    _restaurant_persistence.RESTAURANT_DICT = {}
    yield
    # making sure the test cleans up to an empty list
    _restaurant_persistence.RESTAURANT_DICT = {}


def test_restaurant_persistence(setup_restaurant_persistence):
    assert _restaurant_persistence.read_restaurant_count() == 0

    expected_restaurant = Restaurant()
    expected_restaurant.init(name="r1", manager_email="r1me@unreal.com")

    _restaurant_persistence.save_restaurant(expected_restaurant)
    actual_restaurant = _restaurant_persistence.read_restaurant_by_manager_email("r1me@unreal.com")
    assert actual_restaurant == expected_restaurant

    actual_restaurant = _restaurant_persistence.read_restaurant_by_manager_email("some_junk")
    assert actual_restaurant is None

    _restaurant_persistence.print_all()
