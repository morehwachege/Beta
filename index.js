const express = require("express");
const app = express();
const port = 3000;
const host = `https://localhost:${port}`

app.use('/static', express.static("public"))
app.use(express.urlencoded({extended: true }));

app.set("view engine", "ejs");

app.get('/', (req,res) => {
    res.render('todo.ejs');
})
app.post('/', (req, res) => {
    console.log(req.body);
})

app.listen(port, console.log(`Server listening at ${host}`))