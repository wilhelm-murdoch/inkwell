# -*- coding: utf-8 -*-
import os
from inkwell import inkwell

app = inkwell.bootstrap(os.environ.get('INKWELL_CONFIG_MODULE', 'inkwell.config.LocalConfig'))

if __name__ == '__main__':
    print "Starting Inkwell server in {0} environment".format(\
        app.config['ENVIRONMENT'])
    app.run(host=app.config['HOST'], port=app.config['PORT'], \
        debug=app.config['DEBUG'])