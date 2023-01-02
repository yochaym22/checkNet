const express = require('express');
const cors = require('cors')
const bodyParser = require('body-parser')
const fetch = require('node-fetch')

const app = express();
const PORT = 5000;
const BASE_SCRAPPER_URL = 'http://localhost:8000/scrapper/game/'
FRONT_HTML = __dirname + '/front.html'

app.use(cors({ allowedHeaders: 'Content-Type, Cache-Control' }));
app.options('*', cors());
app.use(bodyParser.urlencoded({extended: false}))
app.use(bodyParser.json())

app.get('/', (req, res) => {
    res.sendFile(FRONT_HTML)
});

app.post('/', async(req, res) => {
    const game_number = Number(req.body.number)
    const scrap_res = await fetch(BASE_SCRAPPER_URL + game_number)

    if (!scrap_res.ok){
        console.log('faild')
        throw new Error('error status: '+ scrap_res.status);
    }
    const result = await scrap_res.json()
    res.status(201).send(result);
});

app.listen(PORT, () => {
    console.log(`Now listening on port ${PORT}`);
});