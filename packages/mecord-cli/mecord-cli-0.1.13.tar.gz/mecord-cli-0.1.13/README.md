Mecord Python Tool
===============================================
The Mecord Python Tool is a official tool for mecodr, you can use it to **Register** device to mecord server, other person can use **Mecord Application** assign tasks to you for implementation

Installation
------------

The Mecord requires [Python](http://www.python.org/download) 3.10.6 or later.

##### Installing
    pip install mecord-cli

##### Uninstalling
    pip uninstall mecord-cli

Use
------------
##### 1. RegisterDevice To Mecord Server
    $ mecord deviceid
use mecord mobile application scan qrcode to register your device to mecord server

##### 2. Running
    $ mecord service start
start a process to wait for the server to issue tasks. **Please do not close it**

Module Developer
------------
    $ mecord widget init
in empty folder, use above command craete a mecord module, structure is like 
    
    [widget folder]
        |-- h5
            |-- config.json     //*required* widget config file
            |-- icon.png
            |-- index.html      //*required* index web page
        |-- script
            |-- main.py         //*required* entry file of receiving task
            |-- run.py
you can modify script and h5 file yourself, then publish to mecord sever 
    
    $ mecord widget publish