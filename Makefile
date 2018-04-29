

WKI=wkhtmltoimage

SVGDIR=svg
PNGDIR=png

$(PNGDIR)/%.png : $(SVGDIR)/%.svg
	@test -d $(PNGDIR) || mkdir $(PNGDIR)
	$(WKI) -f png --transparent --enable-javascript --no-stop-slow-scripts $< $@

$(PNGDIR)/full_cover.png : $(SVGDIR)/full_cover.svg $(SVGDIR)/front_cover.svg $(SVGDIR)/back_cover.svg $(SVGDIR)/binding_cover.svg