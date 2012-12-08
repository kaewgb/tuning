pdf-local: report.pdf

report.pdf: *.tex
	$(PDFLATEX) report.tex
	$(PDFLATEX) report.tex
	$(PDFLATEX) report.tex

clean-local:
	rm -rf *pdf *aux *dvi *ps *log *bak
