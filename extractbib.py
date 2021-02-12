#! /usr/bin/env python
# Copyright (c) 2014-2021, Phillip Alday
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import argparse
import sys
import bibtexparser

import logging
from logging import NullHandler
logging.basicConfig(format='\033[1m\033[33m%(levelname)s:\033[0m %(message)s')

from bibtexparser.bparser import BibTexParser, logger
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.customization import convert_to_unicode, homogenize_latex_encoding
logger.setLevel(logging.ERROR)

# fix missing standard types
bibtexparser.bibdatabase.STANDARD_TYPES.add("collection")
bibtexparser.bibdatabase.STANDARD_TYPES.add("periodical")

NON_LOCAL_FIELDS = ['address',
                    'annote',
                    'author',
                    'booktitle',
                    'chapter',
                    'crossref',
                    'doi',
                    'edition',
                    'editor',
                    'howpublished',
                    'institution',
                    'journal',
                    'key',
                    'month',
                    'note',
                    'number',
                    'organization',
                    'pages',
                    'publisher',
                    'school',
                    'series',
                    'title',
                    'url',
                    'link',
                    'volume',
                    'year',
                  ]

def prune(entry):
   """
      prune(entry)

   Remove local fields from a BibTeX entry.

   Local fields include things like "date-added" and references to document
   storage.

   This function uses `NON_LOCAL_FIELDS` as a whitelist, instead of
   blacklisting local fields.
   """
   keepers = NON_LOCAL_FIELDS + ['ID', 'ENTRYTYPE'] # bibtexparser fields
   return {field:value for field, value in entry.items() if field in keepers}

argparser = argparse.ArgumentParser(
   description="Extract minimal BibTeX entries from a large bibliography")
argparser.add_argument('keylist', type=open,
   help="Filename of a newline delimited list of BibTeX keys")
argparser.add_argument('bibfile', type=open,
   help="BibTeX file to extract entries from")
argparser.add_argument('outfile', type=argparse.FileType('w', encoding='UTF-8'),
   help="Destination file for extracted keys (will be overwritten")
# TODO expose addition bibtexparser options, e.g.
# parser = BibTexParser(common_strings=False)
# parser.ignore_nonstandard_types = False
# parser.homogenise_fields = False
# allow for more verbose logging

def main(argv=None):
    args = argparser.parse_args(argv)

    keys = [_.rstrip() for _ in args.keylist.readlines()]

    bibparser = BibTexParser(common_strings=True)
    bibparser.customization = convert_to_unicode

    allrefs = bibtexparser.load(args.bibfile, parser=bibparser).get_entry_dict()
    usedrefs = BibDatabase()
    usedrefs.entries = [prune(allrefs[key]) for key in keys if key in allrefs]

    missing = [key for key in keys if key not in allrefs]

    if missing:
        logging.warning("Following keys not found: {}".format(', '.join(missing)))

    writer = BibTexWriter()
    #writer.indent = ' ' * 4
    args.outfile.write(writer.write(usedrefs))

if __name__ == "__main__":
   sys.exit(main())
