"""
mblog: a minimal markdown blog
"""
from __future__ import print_function

__VERSION__ = '1.6.0'

# pylint: disable=W
# pylint: disable=missing-docstring
try:

    import logging
    import multiprocessing as mp
    import sys
    import webbrowser

    import waitress

    from mblog.config import HOST, IP, PORT, THREADS, DEBUG, USER

    from mblog.config import app, database, DATABASE_NEEDS_FTS
    from mblog.models import Entry
    if DATABASE_NEEDS_FTS:
        from mblog.models import FTSEntry
    from mblog.routes import *

except ImportError as importError:
    print("All dependencies aren't installed. \n Error: {} \n Run: $ pip install -r requirements.txt".format(
        str(importError)), file=sys.stderr)
    exit(1)


def startBrowser():
    def __startBrowserIntl():
        try:
            hostUrl = "http://{}:{}/".format(HOST, PORT)
            webbrowser.open(hostUrl, new=2)
        except:
            pass

    browserProcess = mp.Process(target=__startBrowserIntl)
    browserProcess.daemon = True
    browserProcess.start()


def startBlog():
    database.create_tables([Entry], safe=True)
    if DATABASE_NEEDS_FTS:
        database.create_tables([FTSEntry], safe=True)

    logging.basicConfig(level=logging.INFO)

    try:
        if not DEBUG:
            waitress.serve(app, host=IP, port=PORT, threads=THREADS)
        else:
            app.run(host=IP, port=PORT, debug=DEBUG)
    except:
       app.run(host=IP, port=PORT, debug=DEBUG)
