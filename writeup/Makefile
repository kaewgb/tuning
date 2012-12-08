default: report.pdf

SOURCES=				\
	report.tex			\
	_intro.tex			\
	_background.tex 	\
	_hypterm.tex		\
	_conclusion.tex

report.pdf: $(SOURCES)
	latex $<
	bibtex report
	latex $<
	pdflatex $<

.PHONY:	clean

clean:
	rm -rf *.pdf *.aux *.dvi *.ps *.log *.bak
