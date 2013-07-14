# Inkwell

Inkwell is a Flask blueprint, or stand-alone server, which supports a Git-based blogging platform.

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
