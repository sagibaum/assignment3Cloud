import requests
import pytest

print("Running tests...")
dish_ids = []

# Test 1: Execute three POST /dishes requests using the dishes "orange", "spaghetti", and "apple pie"
def test_post_dishes():
    dish_names = ["orange", "spaghetti", "apple pie"]

    for name in dish_names:
        response = requests.post("http://localhost:8000/dishes", data={"name": name})
        assert response.status_code == 201
        dish_ids.append(response.json()["id"])
    assert len(set(dish_ids)) == len(dish_names)

# Test 2: Execute a GET dishes/<orange-ID> request
def test_get_dish():
    response = requests.get(f"http://localhost:8000/dishes/{dish_ids[0]}")
    assert response.status_code == 200
    dish = response.json()
    assert 0.9 <= dish["sodium"] <= 1.1

# Test 3: Execute a GET /dishes request
def test_get_all_dishes():
    response = requests.get("http://localhost:8000/dishes")
    assert response.status_code == 200
    dishes = response.json()
    assert len(dishes) == 3

# Test 4: Execute a POST /dishes request supplying the dish name "blah"
def test_post_dish_blah():
    response = requests.post("http://localhost:8000/dishes", data={"name": "blah"})
    assert response.status_code in [400, 404, 422]
    assert response.json()["code"] == -3

# Test 5: Perform a POST dishes request with the dish name "orange"
def test_post_existing_dish():
    response = requests.post("http://localhost:8000/dishes", data={"name": "orange"})
    assert response.status_code in [400, 404, 422]
    assert response.json()["code"] == -2

# Test 6: Perform a POST /meals request specifying the meal name as "delicious" and the dish IDs
def test_post_meal():
    meal_data = {
        "name": "delicious",
        "appetizer": dish_ids[0],
        "main": dish_ids[1],
        "dessert": dish_ids[2]
    }

    response = requests.post("http://localhost:8000/meals", data=meal_data)
    assert response.status_code == 201
    assert response.json()["id"] > 0

# Test 7: Perform a GET /meals request
def test_get_meals():
    response = requests.get("http://localhost:8000/meals")
    assert response.status_code == 200
    meals = response.json()
    assert len(meals) == 1
    assert 400 <= meals[0]["calories"] <= 500

# Test 8: Perform a POST /meals request with the same meal name
def test_post_existing_meal():
    meal_data = {
        "name": "delicious",
        "appetizer": dish_ids[0],
        "main": dish_ids[1],
        "dessert": dish_ids[2]
    }

    response = requests.post("http://localhost:8000/meals", data=meal_data)
    assert response.status_code in [400, 422]
    assert response.json()["code"] == -2

#call all tests
test_post_dishes()
test_get_dish()
test_get_all_dishes()
test_post_dish_blah()
test_post_existing_dish()
test_post_meal()
test_get_meals()
test_post_existing_meal()
