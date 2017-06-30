import sys

from kort.api import app as application
from kort.conf import configure


def main(argv=sys.argv):
    filename = None
    if len(argv) > 2:
        filename = argv[1]
    conf = configure(filename)
    application.run(
        host=conf.get('api.host', '0.0.0.0'),
        port=conf.get('api.port', 5000),
        debug=conf.get('api.debug', True),
    )


if __name__ == '__main__':
    main()
