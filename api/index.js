const express = require('express');
const path = require('path');

const app = express();

// Serve the static files from the React app
app.use(express.json());
app.use(express.static(path.join(__dirname, 'client/build')));

// An api endpoint that returns python script output
app.post('/api/predict', (req,res) => {
    var image = req.body.image;
    console.log(typeof image);
    console.log(image);

    //res.send(req.body);
    //res.sendStatus(200);
    let runPy = new Promise(function(success, nosuccess) {

        const { spawn } = require('child_process');
        const pyprog = spawn('python', [__dirname+'/network/test.py']);
        pyprog.stdin.write(JSON.stringify(["foo", "bar", "baz"]))
    
        pyprog.stdout.on('data', function(data) {
    
            success(data);
        });
    
        pyprog.stderr.on('data', (data) => {
    
            nosuccess(data);
        });
    });

    runPy.then(function(fromRunpy) {
        console.log(fromRunpy.toString());
        res.end(fromRunpy);
    }).catch((error) => {
        console.log(error.toString());
    });
});

// Handles any requests that don't match the ones above
app.get('*', (req,res) =>{
    res.sendFile(path.join(__dirname+'/client/build/index.html'));
});

const port = process.env.PORT || 5000;
app.listen(port);

console.log('App is listening on port ' + port);