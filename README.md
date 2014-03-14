[![Build Status](https://drone.io/github.com/wilhelm-murdoch/inkwell/status.png)](https://drone.io/github.com/wilhelm-murdoch/inkwell/latest) [![Code Health](https://landscape.io/github/wilhelm-murdoch/inkwell/master/landscape.png)](https://landscape.io/github/wilhelm-murdoch/inkwell/master)
# Inkwell

WORK IN PROGRESS

A teeny-tiny git-powered blogging platform written in Python and inspired by its Ruby counterpart [Toto](https://github.com/cloudhead/toto) created by [Alexis Sellier](https://github.com/cloudhead).

## Philosophy

## How Does It Work?

* content is entirely managed through git; you get full fledged version control for free.
* articles are stored as .txt files, with embeded metadata (in yaml format).
* articles are processed through a markdown converter by default.
* templating is completely powered by [AngularJS](http://angularjs.org).
* inkwell is built on top of [Flask](http://flask.pocoo.org/).
* inkwell exposes a very simple RESTful JSON API to interact with article content.
* inkwell can be used as a standalone server, a [Flask blueprint](http://flask.pocoo.org/docs/blueprints/), or directly accessed as a Python module.
* inkwell was built to take advantage of HTTP caching.
* inkwell was built with [Heroku](https://www.heroku.com/) in mind.
* comments are handled by [disqus](http://disqus.com/) by default.
* a very simple URL structure for browsing articles.
* the archives can be accessed by year, month or day.
* arbitrary metadata can be included in articles files, and accessed from the templates.
* optionally, inkwell can use a themed frontend, named [Quill](https://github.com/wilhelm-murdoch/quill), to provide a browser interface.

## Installation

### From Source

If you plan on forking and doing some local development, it's recommended you use a dedicated [virtualenv](http://www.virtualenv.org/en/latest/) environment.

    $: git clone git@github.com:wilhelm-murdoch/inkwell.git
    $: cd inkwell
    $: python setup.py install

Alternatively, you can use the following make targets for local development:

1. `make install` installs Inkwell locally in development mode.
2. `make uninstall` removes Inkwell locally
3. `make test` runs the unit test suite
4. `make clean` removes any garbage files that usage and installation generates

### Using Pip

    $: pip install git+git://github.com/wilhelm-murdoch/inkwell.git

Or, add the following line to a `requirements.txt` file if you wish to use Inkwell as a module in another project:

    -e git+ssh://git@github.com/wilhelm-murdoch/inkwell.git#egg=inkwell

## Quill

Inkwell can be run on its own if you want a basic RESTful API to deliver your article content, but what's an API without a client? This is where [Quill](https://github.com/wilhelm-murdoch/quill) comes in. It's the default theme for Inkwell written using AngularJS, making it a perfect option to power a RESTful client.

The way Quill works is it implements Inkwell as a Flask blueprint and then runs itself as a server. You interact with Quill through your browser and it calls its local Inkwell API to interact with your content.

You implement Quill by first forking, or cloning, the project and running the following commands:

```
$: git clone git://github.com/wilhelm-murdoch/quill.git weblog
$: cd weblog
$: make install
```

In most cases, this is all you need to do to get a build of Quill installed.

To run Quill, execute the following command:

```
$: make run
env INKWELL_CONFIG_MODULE=quill.config.LocalConfig python app.py
Quill running in local on port 8080 ...
 * Running on http://127.0.0.1:8080/
```

Now go to `http://127.0.0.1:8080/` in your browser window and you should see the default article. You are now ready to start writing your own articles!

## Writing Articles

Here is an example of an article:

```
title: I'm Henry, the VIII, I am
time: 10:30
tags:
- music
- Herman's Hermits

I'm Henry, the VIII, I am
Henry, the VIII, I am, I am
I got married to the widow next door
She's been married seven times before
```

The top portion is the header block.

## Configuration

## Inkwell API

This is a very basic API that provides a handful of simple endpoints which allow a client to easily browse published articles.

### Requirements

All requests to the API require the `Accept: application/json` header.

Date elements within the URL will be the in following format:

1. `year` 4 digit number
2. `month` zero-padded 2 digit number
3. `day` zero-padded 2 digit number

### Response

These are the response headers you should expect for every request:

```
HTTP/1.0 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: 895
Server: Werkzeug/0.9.1 Python/2.7.2
Date: Sun, 14 Jul 2013 11:06:22 GMT
```

This is the structure of all responses. It will be presented in either a single object or as an array of objects.

```
{
    "body": "<p>Hello World!</p>",
    "meta": {
        "date": "2013-07-12T00:00:00Z",
        "day": "12",
        "month": "07",
        "path": "2013/07/12/welcome-to-inkwell",
        "slug": "welcome-to-inkwell",
        "title": "Welcome to Inkwell!",
        "year": "2013"
    }
}
```

* `body` the article's body transformed from Markdown to HTML
* `meta` contains all metadata associated with the article, including arbitrary metadata added to the article's YAML header block.
* `meta.data` ISO timestamp derived from the article's filename.
* `meta.day` day of the article.
* `meta.month` month of the article.
* `meta.year` year of the article.
* `meta.path` current URL path to the article.
* `meta.title` title of the article derived from the YAML header block, or, if not found, from the article's filename.
* `meta.slug` the URL-friendly version of `meta.title`.

### Errors

All errors raised by Inkwell will provide appropriate HTTP responses in the following JSON format:

```
HTTP/1.0 404 NOT FOUND
Content-Type: application/json
Content-Length: 174
Server: Werkzeug/0.9.1 Python/2.7.2
Date: Sun, 14 Jul 2013 11:16:30 GMT

{
    "code": 404,
    "description": "The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.",
    "name": "Not Found"
}
```

### Endpoints

* [GET /inkwell](#get-inkwell)
* [GET /inkwell/{year}](#get-inkwellyear)
* [GET /inkwell/{year}/{month}](#get-inkwellyearmonth)
* [GET /inkwell/{year}/{month}/{day}](#get-inkwellyearmontday)
* [GET /inkwell/{year}/{month}/{day}/{title}](#get-inkwellyearmonthdaytitle)

#### GET /inkwell

Will return all currently published articles as an array of response objects.

```
$: curl -i -H "Accept: application/json" http://example.com/inkwell/
```

#### GET /inkwell/{year}

Will return any articles published under the given `year`.

```
$: curl -i -H "Accept: application/json" http://example.com/inkwell/2013
```

#### GET /inkwell/{year}/{month}

Will return any articles published under the given `year` and `month`.

```
$: curl -i -H "Accept: application/json" http://example.com/inkwell/1981/07
```

#### GET /inkwell/{year}/{month}/{day}

Will return any articles published under the given `year`, `month` and `day`.

```
$: curl -i -H "Accept: application/json" http://example.com/inkwell/1981/07/28
```

#### GET /inkwell/{year}/{month}/{day}/{title}

Will return the specified article if it exists, or a 404 response if it doesn't.

```
$: curl -i -H "Accept: application/json" http://example.com/inkwell/1981/07/28/wilhelms-birthday
```

## Thank You

1. I want to thank [Alexis Sellier](https://github.com/cloudhead) for giving me the idea to write something like [Toto](https://github.com/cloudhead/toto), but for Python.
2. A big, big, BIG pat on the back to Sam Hocevar, for providing everyone with a such a simple [software license](http://www.wtfpl.net/).
