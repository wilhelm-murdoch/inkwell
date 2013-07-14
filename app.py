# -*- coding: utf-8 -*-
import os
from inkwell import inkwell

app = inkwell.bootstrap(os.environ.get('INKWELL_CONFIG_MODULE', None))

if __name__ == '__main__':
    print "Inkwell running in {} on port {} ...".format(
          app.config['ENVIRONMENT'],
        , app.config['PORT']
    )

    app.run(
          host=app.config['HOST']
        , port=app.config['PORT']
        , debug=app.config['DEBUG']
    )