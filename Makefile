

FFX=firefox -headless
PY=python3
IMM=convert
PPU=pdfunite

SVGDIR=svg
PNGDIR=png
HTMDIR=html
SCRDIR=scripts
TMPDIR=templates
PDFDIR=pdf

include cover.mk
include pages.mk

$(PNGDIR)/%.png : $(HTMDIR)/%.html
	@test -d $$(dirname $@) || mkdir -p $$(dirname $@)
	$(FFX) -screenshot $@ file://$$(realpath $<)

$(PNGDIR)/%.png : $(SVGDIR)/%.svg
	@test -d $$(dirname $@) || mkdir -p $$(dirname $@)
	$(FFX) -screenshot $@ file://$$(realpath $<)

$(PDFDIR)/%.pdf : $(PNGDIR)/%.png
	@test -d $$(dirname $@) || mkdir -p $$(dirname $@)
	$(IMM) -density 254 -units pixelsperinch $< $@

$(PNGDIR)/full_cover.png : $(SVGDIR)/full_cover.svg $(SVGDIR)/front_cover.svg $(SVGDIR)/back_cover.svg $(SVGDIR)/binding_cover.svg $(SVGDIR)/cropmarks_cover.svg

pages.mk cover.mk : $(SCRDIR)/organizer.py
	$(PY) $< svg/pages $@

.SECONDEXPANSION:
$(HTMDIR)/pages_%.html : $(SCRDIR)/pager.py $(TMPDIR)/pages_template.html $(SVGDIR)/pages/p_$$(word 1,$$(subst _, ,$$*)).svg $(SVGDIR)/pages/p_$$(word 2,$$(subst _, ,$$*)).svg $(SVGDIR)/page_background.svg $(SVGDIR)/cropmarks_pages.svg
	@test -d $$(dirname $@) || mkdir -p $$(dirname $@)
	$(PY) $^ $@

$(HTMDIR)/cover_%.html : $(SCRDIR)/pager.py $(TMPDIR)/cover_template.html $(SVGDIR)/pages/c_$$(word 1,$$(subst _, ,$$*)).svg $(SVGDIR)/pages/c_$$(word 2,$$(subst _, ,$$*)).svg $(SVGDIR)/inner_cover_background.svg $(SVGDIR)/cropmarks_cover.svg
	@test -d $$(dirname $@) || mkdir -p $$(dirname $@)
	$(PY) $^ $@
