
const express = require('express');
const create = require('express-handlebars').create;

const fs = require('fs');


const app = express();

const hbs = create({
    extname: "hbs",
    helpers: {
        ifeq: function(a, b, options){
            if (a === b) {
                return options.fn(this);
            }
            return options.inverse(this);
        },
    }
});

app.engine('.hbs', hbs.engine);
app.set('view engine', '.hbs');
app.set('views', './views');

app.get('/form/:name', (req, res) => {
    console.log('req')
    const form = JSON.parse(fs.readFileSync("./forms/" + req.params["name"] + ".json"));
    res.render('template', form);
});

app.listen(3000);
