import connectionController
from assertions import *

def test_insert_three_dishes():
    word1 = "orange"
    word2 = "spaghetti"
    word3 = "apple pie"
    response1 = connectionController.http_post("dishes", data={'name': word1})
    response2 = connectionController.http_post("dishes", data={'name': word2})
    response3 = connectionController.http_post("dishes", data={'name': word3})

    assert response1.status_code == 201
    assert response2.status_code == 201
    assert response3.status_code == 201

    assert response1.json() != response2.json() != response3.json()


def test_get_orange_dish():
    response = connectionController.http_get("/dishes/1")
    assert response.status_code == 200
    sodium_field = response.json()['sodium']
    assert sodium_field >= 0.9 and sodium_field <= 1.1

def test_get_all_dishes():
    response = connectionController.http_get("dishes")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_insert_dish_doesnt_exist():
    word1 = "blah"
    response1 = connectionController.http_post("dishes", data={'name': word1})

    assert response1.json() == -3
    assert response1.status_code == 404 or response1.status_code == 400 or response1.status_code == 422


def test_insert_dish_already_exists():
    word1 = "orange"
    response1 = connectionController.http_post("dishes", data={'name': word1})

    assert response1.json() == -2
    assert response1.status_code == 404 or response1.status_code == 400 or response1.status_code == 422


def test_post_meal():
    response1 = connectionController.http_post("meals", data={'name': "delicious", 'appetizer': 1, 'main': 2, 'dessert': 3})

    assert response1.status_code == 201
    assert response1.json() > 0


def test_get_meals():
    response = connectionController.http_get("meals")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()["1"]['cal'] >= 400 and response.json()["1"]['cal'] <= 500


def test_post_meal_already_exists():
    response1 = connectionController.http_post("meals", data={'name': "delicious", 'appetizer': 1, 'main': 2, 'dessert': 3})

    assert response1.status_code == 400 or response1.status_code == 422
    assert response1.json() == -2
