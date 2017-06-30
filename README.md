# Kort API

Kort is a URL-Shortener API written in python using Flask and SQLAlchemy

## Why create yet another URL-Shortener ?

There is already a lot of url shortener libs existing and written in python, but they are usually not really shortening but rather encoding the url using a hash which is on average longer than the url which we wanted to shorten.

In Kort we use a bijective function which will use the database entry ID as key, so the link will always be really short (starting from 1 letter) and fast to encode/decode.

## Why make an API and not a web form/page ?

So it can be used programmatically, called by script or bots. But feel free to make a web form which will call this API internally.

## Who could need this ?

If you use any kind of complex dashboards at your company, it uses have a lot of parameters and the url is really long, and you usually end copy/pasting it manually in a mail or pastebin, as it can even break url parsing/triggering on some medias like IRC client (irssi).


## Table of contents

  * [Requirements](#requirements)
  * [Installation](#installation)
  * [Getting started](#getting-started)
  * [Use cases](#use-cases)
    * [Creating a shortened link](#creating-a-shortened-link)
    * [Using a shortened link](#using-a-shortened-link)
  * [Advanced Usage](#advanced-usage)
    * [Configuration](#configuration)
    * [WSGI](#wsgi)
  * [License](#license)

## Requirements

* A compatible operating system (Linux, BSD, Mac OS X/Darwin, Windows)
* Python 2.6/2.7/3.2/3.3/3.4/3.5/3.6

## Installation

### Install with pip

    $ pip install kort

### Build from source

    $ cd /path/to/the/repository
    $ python setup.py install --user

## Getting started

Using the provided CLI command 'kort', you can use --help for each command to see available options.

First initialize the database. Default is using a sqlite DB located in relative directory 'sqlite:///kort.db'.

    $ kort initdb

Launch the API. Default is running on localhost and port 5000.

    $ kort run

## Use cases

  * [Creating a shortened link](#creating-a-shortened-link)
  * [Using a shortened link](#using-a-shortened-link)

### Creating a shortened link

using curl

    $ curl -X POST "http://0.0.0.0:5000/" --data "url=http://example.com/"

will return a 201 response, shortened url is in response `Location` header

    `Location: http://0.0.0.0:5000/M`

If you submit the same request it will not create a new entry but return the previous entry with the same response to avoid duplicate entries in database.

### Using a shortened link

using curl

    $ curl -X GET "http://0.0.0.0:5000/M"

will return a 302 response with the real url located in a `Location` header.

## Advanced Usage

### Configuration

Kort comes with defaults value for configuration. But you can override everything using a YAML configuration file. One configuration example is provided in the conf directory: [conf.yaml.tmpl](https://github.com/sayoun/kort/blob/master/kort/conf/conf.yaml.tmpl).

Kort will search for a configuration file located in `/etc/kort.yaml`, if not found it will use default values.

### WSGI

You can launch Kort API as a WSGI process, using file provided in the bin directory [wsgi.py](https://github.com/sayoun/kort/blob/master/kort/bin/wsgi.py).

One gunicorn example is provided in the conf directory: [kort.gunicorn.tmpl](https://github.com/sayoun/kort/blob/master/kort/conf/kort.gunicorn.tmpl).

## License / Copying

MIT License

Copyright (c) [2017] [Dejan Filipovic (sayoun)]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
