# Futhark

Markdown and DVCS can change the way we collaborate. Even for those pesky journals that require a submission in Word format, you can do the majority of your work in Markdown and then convert to Word via pandoc (and if need be LibreOffice to convert .odt/.docx to .doc). However, a common bibliography is still difficult to pull off. The Makefile and scripts here automagically extract the relevant pandoc references from the specified BibTeX library and create a minimal local BibTeX file that you can include in your repository.

This was inspired by and expands upon the ideas in [this blog post](http://timotheepoisot.fr/2013/11/10/shared-bibtex-file-markdown/).

Requirements:

- `make`
- [Git](http://git-scm.com/) ([Mercurial version available on SourceHut](https://hg.sr.ht/~palday/futhark))
- [`pandoc`](http://johnmacfarlane.net/pandoc/)
- [Python (3)](https://www.python.org/)
- [BibTexParser](http://bibtexparser.readthedocs.org/en/latest/install.html)

You can install `pandoc` and all the Python tooling via [conda](https://www.anaconda.com/products/individual):
```bash
user@host:~/projectdir$ conda env create -f environment.yml
user@host:~/projectdir$ conda activate futhark
(futhark) user@host:~/projectdir$ conda activate futhark
```

If you prefer to use your system Python, virtual environments, PyEnv, etc., then the Python packages are available via pip:
```bash
user@host:~/projectdir$ python -m pip install -r requirements.txt
```

The `mdwc` is useful for word counts of markdown documents with a YAML header block and is developed [here](https://github.com/palday/mdwc).

## License
My contributions are GPLv2. Previous versions used code with an unclear license, but that has been removed in current versions.

The LaTeX template is a modification of the standard pandoc template and is thus subject to [the same restrictions](https://github.com/jgm/pandoc-templates).
