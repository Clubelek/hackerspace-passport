

WKI=wkhtmltoimage
FFX=firefox -headless

SVGDIR=svg
PNGDIR=png

$(PNGDIR)/%.png : $(SVGDIR)/%.svg
	@test -d $$(dirname $@) || mkdir -p $$(dirname $@)
	$(FFX) -screenshot $@ file://$$(realpath $<)

$(PNGDIR)/full_cover.png : $(SVGDIR)/full_cover.svg $(SVGDIR)/front_cover.svg $(SVGDIR)/back_cover.svg $(SVGDIR)/binding_cover.svg