#!/usr/bin/env python
import argparse
from datetime import datetime
import logging
import os
import re
import sys
from unicodedata import normalize

from couchdbkit import Database
from couchdbkit.designer.fs import FSDoc
from couchdbkit.schema import value_to_json
from couchdbkit import utils

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

LOG_FMT = r"%(asctime)s [%(process)d] [%(levelname)s] %(message)s"
LOG_DATE_FMT = r"%Y-%m-%d %H:%M:%S"
LOG_LEVELS = {
    "critical": logging.CRITICAL,
    "error": logging.ERROR,
    "warning": logging.WARNING,
    "info": logging.INFO,
    "debug": logging.DEBUG}

logger = logging.getLogger(__name__)

def slugify(text, delim=u'-'):
    """Generates an slightly worse ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))


class Post(FSDoc):

    def get_id(self):
        ftitle = os.path.join(self.docdir, 'title')
        fid = os.path.join(self.docdir, 'tile')
        if os.path.exists(ftitle):
            title = utils.read_file(ftitle).split("\n")[0].strip()
            if title:
                return slugify(title)
        elif os.path.exists(fid):
            docid = utils.read_file(idfile).split("\n")[0].strip()
            if docid:
                return docid
        return os.path.split(self.docdir)[1]


    def push(self, db):
        doc = self.doc(db, with_attachments=False, force=False)
        doc['created_at'] = datetime.utcnow()
        doc['type'] = "post"
        doc["body"] = doc["body"].replace("%%DOCID%%",
                self.docid).replace("%%DBNAME%%", db.dbname)
        doc = value_to_json(doc)
        db.save_doc(doc, force_update=True)
        attachments = doc.get('_attachments') or {}

        for name, filepath in self.attachments():
            if name not in attachments:
                logger.debug("attach %s " % name)
                db.put_attachment(doc, open(filepath, "r"), name=name)

        logger.debug("%s/%s had been pushed from %s" % (db.uri,
            self.docid, self.docdir))


def pushposts(db, path):
    for d in os.listdir(path):
        docdir = os.path.join(path, d)
        if not docdir.startswith('.') and os.path.isdir(docdir):
            doc = Post(docdir, is_ddoc=False)
            doc.push(db)


def main():
    parser = argparse.ArgumentParser(description='send some docs')
    parser.add_argument('path', help='folder containing docs to send')
    parser.add_argument('dburl', nargs='?', help='db url',
            default='http://127.0.0.1:5984/posts')

    parser.add_argument('--log-level', dest='loglevel', default='info',
            help="log level")
    parser.add_argument('--log-output', dest='logoutput', default='-',
            help="log output")

    args = parser.parse_args()

     # configure the logger
    loglevel = LOG_LEVELS.get(args.loglevel.lower(), logging.INFO)
    logger.setLevel(loglevel)
    if args.logoutput == "-":
        h = logging.StreamHandler()
    else:
        h = logging.FileHandler(args.logoutput)
    fmt = logging.Formatter(LOG_FMT, LOG_DATE_FMT)
    h.setFormatter(fmt)
    logger.addHandler(h)


    path = os.path.normpath(os.path.join(os.getcwd(), args.path))
    if not os.path.exists(path):
        sys.stderr.write("Error: %r doesn't exists" % args.path)
        sys.stderr.flush()
        sys.exit(1)

    try:
        # create db
        db = Database(args.dburl, create=True, wait_tries=1.)

        # send posts
        pushposts(db, path)
    except Exception, e:
        sys.stderr.write("Error: %r" % e)
        sys.stderr.flush()
        sys.exit(1)

    sys.exit(0)



if __name__ == '__main__':
    main()
