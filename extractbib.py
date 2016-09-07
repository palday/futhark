#! /usr/bin/env python
# s. https://gist.github.com/palday/1ff12dd110255541df0f
# adapted from
# GitHub Gist https://gist.github.com/tpoisot/7406955
# don't forget to install bibtexparser: http://bibtexparser.readthedocs.org/en/latest/install.html
# or with pip:
# pip install bibtexparser

import sys
import codecs
from bibtexparser.bparser import BibTexParser, logger
from logging import NullHandler
logger.addHandler(NullHandler())

non_local_fields = ['address',
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

def dict2bib(ke,di):
   # it seems the type field changed between different bibtexparser versions
   try:
      b = "@"+di['type'].upper()+"{"+ke+",\n"
   except KeyError:
      b = "@"+di['ENTRYTYPE'].upper()+"{"+ke+",\n"

   for (k, v) in sorted(di.iteritems()):
      if k.lower().strip() in non_local_fields:
         if k == 'link':
            k = 'url'
         b += '\t' + k + ' = {'+v+'},\n'
   b += '}\n'
   return b

if __name__ == "__main__":
   ## Check the number of arguments
   if len(sys.argv) != 4:
      raise ValueError("Wrong number of arguments")
   else :
      key_list = sys.argv[1]
      bib_file = sys.argv[2]
      out_file = sys.argv[3]
   ## The three arguments should be strings
   if not isinstance(key_list, str):
      raise TypeError("The path to the list of keys should be a string")
   if not isinstance(bib_file, str):
      raise TypeError("The path to the bibtex library should be a string")
   if not isinstance(out_file, str):
      raise TypeError("The path to the output bibtex file should be a string")
   ## Step 1 - read the key list
   keys = [kl.rstrip(":\n") for kl in open(key_list, 'r')]
   ## Step 2 - read the library file
   refs = BibTexParser(open(bib_file, 'r').read()).get_entry_dict()
   ## Step 3 - extract the used entries
   used_refs = {key: refs[key] for key in keys if key in refs}
   ## Step 4 - convert the dicts back into bibtex
   refs_as_bib = [dict2bib(k, v) for (k, v) in used_refs.iteritems()]
   ## Step 5 - write the output file
   with codecs.open(out_file, 'w', 'utf-8-sig') as of:
      of.writelines(refs_as_bib)
