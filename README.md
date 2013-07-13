# Inkwell

These docs are currently under construction. While Inkwell is pretty much done, it needs a client to run it. That's where [Quill](https://github.com/wilhelm-murdoch/quill) comes in... which is something I'm still working on.

So far ...

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