import axios from 'axios';
import express from "express";
const router = express.Router();
const API_KEY = 'Vsrai71RbGrBh7ZROuzVVg==oHMTSk8Nrfkd4REf'

let dishes = {};
let meals = {};

let dishesCounter = 0;
let mealsCounter = 0;

router.get('/dishes', (req, res) => {
    res.json(dishes);
})

router.post('/dishes', async (req, res) => {
    const headers = { 'X-Api-Key': API_KEY };
    let retVal;
    let statusCode = 201;
    try {
        if (!req.is('application/json')) {
            retVal = 0;
            statusCode = 415;
        }
        else{
            const dishName = req.body.name;
            if (!dishName) {
                retVal = -1;
                statusCode = 400;
            }
            else if (isExist(dishName, dishes)) {
                retVal = -2;
                statusCode = 400;
            }
            else {
                const res = await axios.get(`https://api.api-ninjas.com/v1/nutrition?query=${dishName}`, { headers })

                if (res.data.length === 0) {
                    retVal = -3;
                    statusCode = 400;
                }
                else {
                    dishesCounter++;
                    const newDish = convertToDish(res.data[0]);
                    dishes[dishesCounter] = newDish;
                    retVal = dishesCounter;
                }
            }
        }
        res.status(statusCode).json(retVal)
    }
    catch (err) {
        retVal = -4;
        statusCode = 400;
        res.status(statusCode).json(retVal)

    }
})

router.get('/dishes/:searchKey', (req, res) => {
    const searchKey = req.params.searchKey;
    let retVal;
    let statusCode = 200;

    if (searchKey == '') {
        retVal = -1;
        statusCode = 400;
    }
    else {
        let res;
        if (Number(searchKey)) {
            res = getDishById(searchKey);
        }
        else {
            res = getDishByName(searchKey)
        }

        if (res != null) {
            retVal = res;
        }
        else {
            retVal = -5;
            statusCode = 404;
        }
    }
    res.status(statusCode).json(retVal);
})

router.delete('/dishes/:searchKey', (req, res) => {
    const searchKey = req.params.searchKey;
    let retVal;
    let statusCode = 200;

    if (searchKey == '') {
        retVal = -1;
        statusCode = 400;
    }
    else {
        let res;
        if (Number(searchKey)) {
            res = getDishById(searchKey);
        }
        else {
            res = getDishByName(searchKey);
        }

        if (res == null) {
            retVal = -5;
            statusCode = 404;
        }
        else {
            retVal = res.ID;
            delete dishes[res.ID];
        }
    }

    res.status(statusCode).json(retVal);
})

router.get('/meals', (req, res) => {
    res.json(meals);
})

router.post('/meals', (req, res) => {
    let retVal;
    let statusCode = 201;
    const { name, appetizer, main, dessert } = req.body;

    if (!req.is('application/json')) {
        retVal = 0;
        statusCode = 415;
    }
    else if (!name || !appetizer || !main || !dessert) {
        retVal = -1;
        statusCode = 400;
    }
    else if (isExist(name, meals)) {
        retVal = -2;
        statusCode = 400;
    }
    else{        
        const appetizerDish = getDishById(appetizer);
        const mainDish = getDishById(main);
        const dessertDish = getDishById(dessert);
        
        if (appetizerDish == null || mainDish == null || dessertDish == null) {
            retVal = -5;
            statusCode = 400;
        }
        else {
            mealsCounter++;
            const newMeal = convertToMeal(name, appetizerDish, mainDish, dessertDish);
            meals[mealsCounter] = newMeal;
            retVal = mealsCounter;
        }
    }
    res.status(statusCode).json(retVal);
})

router.get('/meals/:searchKey', (req, res) => {
    const searchKey = req.params.searchKey;
    let retVal;
    let statusCode = 200;

    if (searchKey == '') {
        retVal = -1;
        statusCode = 400;
    }
    else {
        let res;

        if (Number(searchKey)) {
            res = getMealById(searchKey);
        }
        else {
            res = getMealByName(searchKey)
        }

        if (res != null) {
            retVal = res;
        }
        else {
            retVal = -5;
            statusCode = 404;
        }
    }
    res.status(statusCode).json(retVal);
})

router.delete('/meals/:searchKey', (req, res) => {
    const searchKey = req.params.searchKey;
    let retVal;
    let statusCode = 200;

    if (searchKey == '') {
        retVal = -1;
        statusCode = 400;
    }
    else {
        let res;
        if (Number(searchKey)) {
            res = getMealById(searchKey);
        }
        else {
            res = getMealByName(searchKey);
        }

        if (res == null) {
            retVal = -5;
            statusCode = 404;
        }
        else {
            retVal = res.ID;
            delete meals[res.ID];
        }
    }
    res.status(statusCode).json(retVal);
})

router.put('/meals/:id', (req, res) => {
    let retVal;
    let statusCode = 200;
    const mealId = req.params.id
    const { name, appetizer, main, dessert } = req.body;

    if (!req.is('application/json')) {
        retVal = 0;
        statusCode = 415;
    }
    else if (!name || !appetizer || !main || !dessert || mealId == '') {
        retVal = -1;
        statusCode = 400;
    }
    else if (isExist(name, meals)) {
        retVal = -2;
        statusCode = 400;
    }
    else{        
        const appetizerDish = getDishById(appetizer);
        const mainDish = getDishById(main);
        const dessertDish = getDishById(dessert);
        const meal = getMealById(mealId);
        
        if (appetizerDish == null || mainDish == null || dessertDish == null || meal == null) {
            retVal = -5;
            statusCode = 400;
        }
        else {
            const newMeal = convertToMeal(name, appetizerDish, mainDish, dessertDish);
            meals[mealId] = newMeal;
            retVal = mealId;
        }
    }
    res.status(statusCode).json(retVal);
})


const isExist = (name, obj) => {
    let retVal = false;
    for (const elem of Object.values(obj)) {
        if (elem.name === name) {
            retVal = true;
        }
    }
    return retVal;
}

const getDishByName = (name) => {
    let retVal = null;
    for (const dish of Object.values(dishes)) {
        if (dish.name === name) {
            retVal = dish;
        }
    }
    return retVal;
}

const getDishById = (id) => {
    return dishes[id] ? dishes[id] : null;
}

const getMealByName = (name) => {
    let retVal = null;
    for (const meal of Object.values(meals)) {
        if (meal.name === name) {
            retVal = meal;
        }
    }
    return retVal;
}

const getMealById = (id) => {
    return meals[id] ? meals[id] : null;
}

const convertToDish = (data) => {
    return {
        name: data.name,
        ID: dishesCounter,
        cal: data.calories,
        size: data.serving_size_g,
        sodium: data.sodium_mg,
        sugar: data.sugar_g
    };
};

const convertToMeal = (name, appetizerDish, mainDish, dessertDish) => {

    const totalCal = appetizerDish.cal + mainDish.cal + dessertDish.cal;
    const totalSodium = appetizerDish.sodium + mainDish.sodium + dessertDish.sodium;
    const totalSugar = appetizerDish.sugar + mainDish.sugar + dessertDish.sugar;

    return {
        name: name,
        ID: mealsCounter,
        appetizer: appetizerDish.ID,
        main: mainDish.ID,
        dessert: dessertDish.ID,
        cal: totalCal,
        sodium: totalSodium,
        sugar: totalSugar
    };
};


export default router;