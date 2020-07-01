Futhark
=========

Markdown and DVCS can change the way we collaborate. Even for those pesky journals that require a submission in Word format, you can do the majority of your work in Markdown and then convert to Word via pandoc (and if need be LibreOffice to convert .odt/.docx to .doc). However, a common bibliography is still difficult to pull off. The Makefile and scripts here automagically extract the relevant pandoc references from the specified BibTeX library and create a minimal local BibTeX file that you can include in your repository.

This was inspired by and expands upon the ideas in [this blog post](http://timotheepoisot.fr/2013/11/10/shared-bibtex-file-markdown/).

Requirements:

- `make`
- [Git](http://git-scm.com/) ([Mercurial version available on SourceHut](https://hg.sr.ht/~palday/futhark))
- [`pandoc`](http://johnmacfarlane.net/pandoc/)
- [Python](https://www.python.org/)
    - note that BibTexParser will work with Python 2 or 3, but the md-diff script
      will not work unmodified on Python 2.
- [BibTexParser](http://bibtexparser.readthedocs.org/en/latest/install.html)

License:
My contributions are currently GPLv2, but I am building on the work of others, whose licensing conditions aren't yet clear. The LaTeX template is a modification of the standard pandoc template and is thus subject to [the same restrictions](https://github.com/jgm/pandoc-templates).
