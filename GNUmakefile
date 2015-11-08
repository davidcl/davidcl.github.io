#
# This Makefile is part of Clément David's homepage.
#
# It will generate html files from text (xhtml or markdown) and templates.
#

# Tools path
MARKDOWN = /usr/bin/markdown
AWK = /usr/bin/gawk
SH = /bin/sh
RM = /bin/rm -f
CAT = /bin/cat
TOUCH = /bin/touch

# Setting default searching directories
directories = projects articles about

# including per-directory specific rules (if any).
# Use to add sub-directories to the $(directories) variables
-include $(addsuffix /GNUmakefile, $(directories))

# Adding others path to the directories variable after inclusion
directories += . styles

# Setting helpers variables
text-files = $(wildcard $(addsuffix /*.text, $(directories)))
html-files = $(wildcard $(addsuffix /*.htm, $(directories)))

img-files = $(wildcard $(addsuffix /*.png, $(directories))) \
		$(wildcard $(addsuffix /*.jpg, $(directories))) \
		$(wildcard $(addsuffix /*.svg, $(directories)))
other-files = $(wildcard $(addsuffix /*.ico, $(directories))) \
		$(wildcard $(addsuffix /*.css, $(directories)))

all-html = $(text-files:%.text=%.html) $(html-files:%.htm=%.html) 
all-atom = $(text-files:%.text=%.atom) $(html-files:%.htm=%.atom)

# Commands
default:
	@echo "No default rule, try:"
	@echo "  make all       # do almost everything"
	@echo "  make site      # generate html from written files"
	@echo "  make feed      # generate Atom feed from xhtml files"
	@echo "  make update    # will connect to the FTP server and updating change."
	@echo "  make clean     # remove generated files"

all: site update

site: $(all-html)

feed: $(all-atom)
	@echo "feed is not implemented by now" > /dev/stderr

update: $(all-html) $(img-files) $(other-files)
	git push
	git ls-files >update
	rsync -avz -e ssh --progress --delete --files-from=update . davidcl@fedorapeople.org:/home/fedora/davidcl/public_html

preview: site
	epiphany http://localhost:8000 &
	python3 -m http.server 8000

clean:
	$(RM) $(text-files:%.text=%.htm)
	$(RM) $(text-files:%.text=%.xhtml) $(html-files:%.htm=%.xhtml)
	$(RM) $(all-html)
	$(RM) $(all-atom)
	$(RM) update

.PHONY: clean preview

# Generic rules
%.htm: %.text
	$(MARKDOWN) $(MARKDOWNFLAGS) $< > $@

%.html: %.htm templates/default.template template.awk
	$(AWK) -f template.awk -v input="$<" -v output="$@" templates/default.template

%.atom: %.htm templates/atom-entry.template template.awk
	$(AWK) -f template.awk -v input="$<" -v output="$@" templates/atom-entry.template

