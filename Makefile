# Copyright 2024, Vibhash Kumar Singh <singh13@ads.uni-passau.de>
# SPDX-License-Identifier: GPL-2.0-only

REPORT_DIR=report

.PHONY: report
report:
	echo "Generating report ..."
	cd $(REPORT_DIR); pdflatex main.tex; bibtex main.aux; pdflatex main.tex; pdflatex main.tex;


.PHONY: clean
clean:
	echo "Removing build files ..."
	cd $(REPORT_DIR); rm -rf main.aux main.bbl main.blg main.log main.out main.pdf main.toc 
