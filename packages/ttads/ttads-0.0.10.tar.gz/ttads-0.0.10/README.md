# Tasmota Application Development Server

This tool aims to simplify Tasmota Berry script development by doing two things:

* Starts a web app that automatically zips your project(s), and serves it as a `.tapp` file.
* Opens a tunnel to the web app, letting you deploy your Tasmota Application to any device with an internet connection.

# How to Install

`pip install ttads`

# Usage

`ttads /my_projects`

## Sample Output

```bash
Waiting for tunnel to initialise...
 * Serving Flask app 'TappServer'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:80
Press CTRL+C to quit
Serving project "hct": `tasmota.urlfetch("http://c141-x-y-z-w.ngrok.io/hct.tapp")`
```

# :warning: Security Warning

Running `ttads` involves opening up your project files to the public internet, using a development server. Proceed with
caution. 