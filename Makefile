

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
IDDIR=identities

ifndef COLOR_PROFILE
COLOR_PROFILE=USWebCoatedSWOP
endif

all: $(PDFDIR)/full_cover.pdf $(patsubst $(IDDIR)/%.json,$(PDFDIR)/passport_%.pdf,$(wildcard $(IDDIR)/*.json))

include cover.mk
include pages.mk

$(PDFDIR)/passport_%.pdf : $(PDFDIR)/cover.pdf $(PDFDIR)/pages_%.pdf
	$(PPU) $^ $@

$(PDFDIR)/%.pdf : $(PNGDIR)/%.png
	@test -d $$(dirname $@) || mkdir -p $$(dirname $@)
	$(IMM) -density 254 -units pixelsperinch $< -profile resources/sRGB.icc -profile resources/$(COLOR_PROFILE).icc $@

$(PNGDIR)/%.png : $(HTMDIR)/%.html
	@test -d $$(dirname $@) || mkdir -p $$(dirname $@)
	$(FFX) -screenshot $@ file://$$(realpath $<)

$(PNGDIR)/%.png : $(SVGDIR)/%.svg
	@test -d $$(dirname $@) || mkdir -p $$(dirname $@)
	$(FFX) -screenshot $@ file://$$(realpath $<)

$(PNGDIR)/full_cover.png : $(SVGDIR)/full_cover.svg $(SVGDIR)/front_cover.svg $(SVGDIR)/back_cover.svg $(SVGDIR)/binding_cover.svg $(SVGDIR)/cropmarks_cover.svg

pages.mk cover.mk : $(SCRDIR)/organizer.py $(SVGDIR)/pages $(TMPDIR) $(IDDIR)
	$(PY) $^ $@

.SECONDEXPANSION:
$(SVGDIR)/pages/p_%.svg : $(SCRDIR)/mkid.py $(IDDIR)/$$(word 1,$$(subst -, ,$$*)).json $(TMPDIR)/p_{fname}-$$(word 2,$$(subst -, ,$$*)).svg
	$(PY) $^ $@

$(HTMDIR)/pages_%.html : $(SCRDIR)/pager.py $(TMPDIR)/pages_template.html $(SVGDIR)/pages/p_$$(word 1,$$(subst _, ,$$*)).svg $(SVGDIR)/pages/p_$$(word 2,$$(subst _, ,$$*)).svg $(SVGDIR)/page_background.svg $(SVGDIR)/cropmarks_pages.svg
	@test -d $$(dirname $@) || mkdir -p $$(dirname $@)
	$(PY) $^ $@

$(HTMDIR)/cover_%.html : $(SCRDIR)/pager.py $(TMPDIR)/cover_template.html $(SVGDIR)/pages/c_$$(word 1,$$(subst _, ,$$*)).svg $(SVGDIR)/pages/c_$$(word 2,$$(subst _, ,$$*)).svg $(SVGDIR)/inner_cover_background.svg $(SVGDIR)/cropmarks_cover.svg
	@test -d $$(dirname $@) || mkdir -p $$(dirname $@)
	$(PY) $^ $@

$(HTMDIR)/cover_%_0.html : $(SCRDIR)/pager.py $(TMPDIR)/cover_template.html $(SVGDIR)/pages/c_%.svg $(SVGDIR)/pages/c_0.svg $(SVGDIR)/blank_cover_background.svg $(SVGDIR)/cropmarks_cover.svg
	@test -d $$(dirname $@) || mkdir -p $$(dirname $@)
	$(PY) $^ $@

$(HTMDIR)/pages_n_n.html : $(SCRDIR)/pager.py $(TMPDIR)/pages_template.html $(SVGDIR)/pages/p_n.svg $(SVGDIR)/page_background.svg $(SVGDIR)/cropmarks_pages.svg
	@test -d $$(dirname $@) || mkdir -p $$(dirname $@)
	$(PY) $(SCRDIR)/pager.py $(TMPDIR)/pages_template.html $(SVGDIR)/pages/p_n.svg $(SVGDIR)/pages/p_n.svg $(SVGDIR)/page_background.svg $(SVGDIR)/cropmarks_pages.svg $(HTMDIR)/pages_n_n.html

$(HTMDIR)/cover_n_n.html : $(SCRDIR)/pager.py $(TMPDIR)/cover_template.html $(SVGDIR)/pages/c_n.svg $(SVGDIR)/inner_cover_background.svg $(SVGDIR)/cropmarks_cover.svg
	@test -d $$(dirname $@) || mkdir -p $$(dirname $@)
	$(PY) $(SCRDIR)/pager.py $(TMPDIR)/cover_template.html $(SVGDIR)/pages/c_n.svg $(SVGDIR)/pages/c_n.svg $(SVGDIR)/inner_cover_background.svg $(SVGDIR)/cropmarks_cover.svg $(HTMDIR)/cover_n_n.html

.INTERMEDIATE: $(PNGDIR)/full_cover.png $(HTMDIR)/pages_n_n.html $(HTMDIR)/cover_n_n.html
