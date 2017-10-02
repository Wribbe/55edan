latexfile = pagerank

all: $(latexfile).pdf

$(latexfile).pdf : $(latexfile).tex
	while (pdflatex $(latexfile) ; \
	grep -q "Rerun to get cross" $(latexfile).log ) do true ; \
	done


clean:
	git clean -xfd
