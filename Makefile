

WKI=wkhtmltoimage

SVGDIR=svg
PNGDIR=png

$(PNGDIR)/%.png : $(SVGDIR)/%.svg
	@test -d $(PNGDIR) || mkdir $(PNGDIR)
	$(WKI) -f png --transparent --enable-javascript --no-stop-slow-scripts $< $@