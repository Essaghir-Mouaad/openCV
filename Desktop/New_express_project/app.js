

const express = require("express");
const bodyParser = require("body-parser");
const ejs = require("ejs");
const _ = require("lodash");

const homeStartingContent = "Lacus vel facilisis volutpat est velit egestas dui id ornare. Semper auctor neque vitae tempus quam. Sit ametluctus venenatis lectus. Ultrices vitae auctor eu augue ut lectus arcu bibendum at. Odio euismod lacinia at quis risus sed vulputate odio u";
const aboutContent = "Hac habitasse platea dictumst vestibulum rhoncus est pellentesque. Dictumst vestibulum rhoncus est pellentesque elitvitae. Mauris ultrices eros in cursus turpis massa tincidunt dui.";
const contactContent = "Scelerisque eleifend donec pretium vulputate sapien. Rhoncus urna neque viverra justo nec ultrices. Arcu dui vivamneque. Ultrices gravida dictum fusce ut placerat orci nulla. Mauris in aliquam sem fringilla ut morbi tincidunt. Tortor posuere ac ut cons";

const app = express() ;

app.set ('view engine', 'ejs');


app.use(bodyParser.urlencoded({extended:true}) );
app.use(express.static("public"));


var publish = [];


app.get("/", (req, res)=>{
    res.render("home", {startContent:homeStartingContent, post:publish})
})

app.get("/about", (req, res)=>{
    res.render("about", {aboutContent:aboutContent})
})

app.get("/contact", (req, res)=>{
    res.render("contact", {contactContent:contactContent})
})

app.get("/compose", (req, res)=>{
    res.render("compose")
})

app.get("/posts/:publish", (req, res)=>{
    var path = _.lowerCase(req.params.publish);

    publish.forEach(element => {
        if (path === _.lowerCase(element.title)) {
            res.render("post", {title:element.title, article:element.article})
        }else{
            console.log("are not mutched");
        }
    });
})


app.post("/compose", (req, res)=>{

    const posts = {
        title : req.body.compose1,
        article : req.body.text1
    }

    publish.push(posts)
    res.redirect("/")
})


app.listen(3006, function() {
console.log("Server started on port 3006");
})