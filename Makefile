REPORT_DIR=report

.PHONY: report
report:
	echo "Generating report ..."
	cd $(REPORT_DIR); pdflatex main.tex; bibtex main.aux; pdflatex main.tex; pdflatex main.tex;


.PHONY: clean
clean:
	echo "Removing build files ..."
	cd $(REPORT_DIR); rm -rf main.aux main.bbl main.blg main.log main.out main.pdf main.toc 
