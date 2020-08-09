/*
 * Write your Express server in this file as described in README.md.
 * Name: Nicholas Milford
 */

var express = require('express');
var path = require('path');
var exhbs = require('express-handlebars');
var fs = require('fs');
var sendKeys = require('sendkeys-win');
var spawn = require('child_process').spawn, child;

// console.log(robot);

'use strict';

// print computer IP address
var os = require('os');
var ifaces = os.networkInterfaces();

Object.keys(ifaces).forEach(function (ifname) {
  var alias = 0;

  ifaces[ifname].forEach(function (iface) {
    if ('IPv4' !== iface.family || iface.internal !== false) {
      // skip over internal (i.e. 127.0.0.1) and non-ipv4 addresses
      return;
    }

    if (alias >= 1) {
      // this single interface has multiple ipv4 addresses
      console.log(ifname + ':' + alias, iface.address);
    } else {
      // this interface has only one ipv4 adress
      console.log(ifname, iface.address);
    }
    ++alias;
  });
});

// set up mouse control
mouseChild = spawn('C:/Users/Nick/AppData/Local/Programs/Python/Python36/python.exe', [path.join(__dirname, 'clickOn.py')]);
mouseChild.stdout.pipe(process.stdout)

var port = process.env.PORT || 3000;
var app = express();

app.post('/keys/:k', function(req, res){
        console.log("Pressing " + req.params.k);undefined
        res.status(200)
        sendKeys(req.params.k).then(() => {
                console.log('Sent');
        }).catch((err) => {
                console.error(err);4
        });
        res.end();
});

function refresh(){
        child = spawn('powershell.exe', [path.join(__dirname, 'screenshot.ps1')]);
        child.stdout.on("close", function(){
                console.log("Screen Refreshed");
        })
        child.stdout.pipe(process.stdout);
        child.stdin.end();
}

refreshImageInterval = setInterval(refresh, 2*1000);

app.post('/mouse/:x/:y', function(req, res){
        // console.log("Got a touch for " + req.params.x + ", " + req.params.y);
        x = parseInt(req.params.x);
        y = parseInt(req.params.y);
        if(typeof req.query.key != 'undefined'){
                console.log("clicking with key " + req.query.key + ", right click: " + req.query.r);
                sendKeys(req.query.key).then(() => {
                        mouseChild.stdin.write((x) + "\n");
                        mouseChild.stdin.write((y) + "\n");
                        mouseChild.stdin.wri5te(req.query.r + "\n");
                        // console.log("Click with key sent");
                }).catch((err) => {
                        console.error(err);
                });
        }undefined5undefined
        else{
                mouseChild.stdin.write(x + "\n");
                mouseChild.stdin.write(y + "\n");
        }
        res.status(200);
        res.end();
});

app.use(express.static(path.join(__dirname, 'public')));

app.listen(port, function(){
        console.log("Server started on port", port);
});
