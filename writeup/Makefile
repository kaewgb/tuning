default: report.pdf

SOURCES=				\
	report.tex			\
	_intro.tex			\
	_background.tex		\
	_algo.tex		\
	_setup.tex		\
	_results.tex		\
	_conclusion.tex

report.pdf: $(SOURCES)
	pdflatex $<
	bibtex report
	pdflatex $<
	pdflatex $<


RESULTS_ONLY = \
	graphs.tex \

graphs.pdf: $(RESULTS_ONLY)
	pdflatex $<
	bibtex report
	pdflatex $<
	pdflatex $<


.PHONY:	clean

clean:
	rm -rf *.pdf *.aux *.dvi *.ps *.log *.bak
