# SplashGen

## Installation Instructions

> **NOTE**: You will need Python 3.7+

`pip install splashgen`

## Getting Started

1. Copy the file contents of [this example](https://github.com/true3dco/splashgen/blob/master/examples/zenweb.py) into a py file of your own
2. Change the values to reflect your brand
3. Add in a logo.svg into the same directory as your py file
4. Run `splashgen <<Your File>>.py` to build the static files
5. Run `python -m http.server --directory build` to start a HTTP server in the output directory
6. Head over to [http://localhost:8000/](http://localhost:8000/) to see your splashpage!

## **Project Status**

Splashgen is currently in an early alpha. If there are any missing features that you would like added please open an issue and we will add it in! This API is in flux and will receive significant improvements and changes over the next few weeks.
