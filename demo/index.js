'use strict'

const express = require("express");
const bodyParser = require('body-parser');
const {PythonShell} = require('python-shell');
const res = require("express/lib/response");

const app = express();
app.use(express.static("public"));

// Code in this section sets up an express pipeline
app.use(function(req, res, next) {
  console.log(req.method,req.url);
  next();
});

app.get("/", (request, response) => {
  response.sendFile(__dirname + "/public/tweet_sen.html");
});

app.get("/getImage", function(req, res){
  res.sendFile(__dirname + "/graph.png");
})

app.get("/getSample", function(req, res){
  res.sendFile(__dirname + "/sample.png");
})

// Post Requests
app.use(bodyParser.json());

app.post("/analyzeTweet", async function(req, res){
  console.log("Recieved URL:", req.body.url);

  const python_script = 'tweet_analysis.py';
  let options = {
    mode: 'text',
    args: [req.body.url]
  };

  PythonShell.run(python_script, options, function(err, result){
    if(err){
      throw err;
    }
    
    res.json({});
  })

});

// Page not found
app.use(function(req, res){
  res.status(404); 
  res.type('txt'); 
  res.send('404 - File '+req.url+' not found'); 
});

// end of pipeline specification
const listener = app.listen(3000, function () {
  console.log("The static server is listening on port " + listener.address().port);
});

