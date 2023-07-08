import express from "express";
import router from './router.js';

const PORT = 8000;

const app = express();

app.use(express.json())
app.use(router);

app.listen(PORT, '0.0.0.0',  () => {
    console.log('listening on port', PORT);
})