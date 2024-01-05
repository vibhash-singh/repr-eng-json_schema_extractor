INPUT_DIR=/report/src
OUTPUT_DIR=/report/build

.PHONY: report
report:
	echo "Generating report ..."
	cd $(INPUT_DIR) && pdflatex -output-directory=$(OUTPUT_DIR) main.tex

.PHONY: clean
clean:
	echo "Removing build files ..."
	rm -rf $(OUTPUT_DIR)/*
