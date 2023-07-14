import connectionController
from assertions import *

def test_insert_three_dishes():
    dish_names = ["orange", "spaghetti", "apple pie"]
    dish_ids = []

    for dish_name in dish_names:
        response = connectionController.http_post("dishes", data={'name': dish_name})
        assert response.status_code == 201
        dish_ids.append(response.json())

    assert len(set(dish_ids)) == len(dish_ids)

def test_get_orange_dish():
    response = connectionController.http_get("dishes/1")
    assert_status_code(response, 200)
    sodium_field = response.json().get("sodium")
    assert sodium_field is not None and 0.9 <= sodium_field <= 1.1


def test_get_all_dishes():
    response = connectionController.http_get("dishes")
    assert_status_code(response, 200)
    assert len(response.json()) == 3

def test_insert_dish_doesnt_exist():
    none_exist_dish = "blah"
    response = connectionController.http_post("dishes", data={'name': none_exist_dish})
    assert response.json() == -3
    assert response.status_code == 404 or response.status_code == 400 or response.status_code == 422

def test_insert_dish_already_exists():
    exist_dish = "orange"
    response1 = connectionController.http_post("dishes", data={'name': exist_dish})
    assert response1.json() == -2
    assert response1.status_code == 404 or response1.status_code == 400 or response1.status_code == 422

def test_post_meal():
    meal_data = {
        'name': "delicious",
        'appetizer': 1,
        'main': 2,
        'dessert': 3
    }
    response = connectionController.http_post("meals", data=meal_data)
    assert_status_code(response, 201)
    assert response.json() > 0

def test_get_meals():
    response = connectionController.http_get("meals")
    assert_status_code(response, 200)
    assert len(response.json()) == 1
    assert 400 <= response.json()["1"]['cal'] <= 500

def test_post_meal_already_exists():
    meal_data = {
        'name': "delicious",
        'appetizer': 1,
        'main': 2,
        'dessert': 3
    }
    response = connectionController.http_post("meals", data=meal_data)
    assert_status_code(response, 400 or 422)
    assert_ret_value(response, -2)
