# Copyright (c) 2013, Phillip Alday
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

python = python
library ?= /path/to/library
paper ?= article
mdflags ?= -f markdown-hard_line_breaks+yaml_metadata_block
refs ?= $(paper).bib

draft: $(paper).pdf
	cp $(paper).pdf $(paper)_`git show -s --format=%ci HEAD | awk '{print $$1}'`_`git rev-parse --short HEAD`.pdf

%.pdf: %.md $(refs)
	pandoc --standalone --template=template.latex --bibliography=$(refs) $*.md -o $*.pdf

%.md: %.Rmd
	echo 'knitr::knit("$*.Rmd")' | R --vanilla

clean:
	rm -rf $(paper).{pdf,html,odt,docx}

$(refs): bib.keys
	$(python) extractbib.py bib.keys $(library) $(refs)

bib.keys: $(paper).md
	grep @[-:_a-zA-Z0-9]* $(paper).md -oh --color=never | sort  | uniq -u | sed 's/@//g' > bib.keys
