import connectionController
from assertions import *

def test_insert_three_dishes():
    dish_names = ["orange", "spaghetti", "apple pie"]
    dish_ids = []

    for dish_name in dish_names:
        response = connectionController.http_post("dishes", data={'name': dish_name})
        assert response.status_code == 201
        dish_ids.append(response.json())
        print(response.json())

    assert len(set(dish_ids)) == len(dish_ids)

def test_get_orange_dish():
    response = connectionController.http_get("/dishes/1")
    assert_status_code(response, 200)
    sodium_field = response.json().get("sodium")
    assert sodium_field is not None and 0.9 <= sodium_field <= 1.1


def test_get_all_dishes():
    response = connectionController.http_get("dishes")
    assert_status_code(response, 200)
    assert len(response.json()) == 3

def test_insert_dish_doesnt_exist():
    dish_name = "blah"
    response = connectionController.http_post("dishes", data={'name': dish_name})
    assert_ret_value(response, -3)
    assert_status_code(response, 404)
    assert_status_code(response, 400)
    assert_status_code(response, 422)

def test_insert_dish_already_exists():
    dish_name = "orange"
    response = connectionController.http_post("dishes", data={'name': dish_name})
    assert_ret_value(response, -2)
    assert_status_code(response, 404)
    assert_status_code(response, 400)
    assert_status_code(response, 422)

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
