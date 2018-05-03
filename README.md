# Clubelek's Hackerspace Passports

These are the source (SVG) files for [Hackerspace Passports](https://www.noisebridge.net/wiki/Passport)
tailored for the [Clubelek of INSA Lyon](https://wiki.hackerspaces.org/Clubelek).
There's nothing more to it, really. But I had to honor the tradition of the README file,
so there you are. I guess I could explain how to use the generation scripts,
as well as some design choices.

## Making

The passport has been designed to be relatively easy to make. It does require some work,
but not high skill or expensive tools.

You will need:

 - A computer running Linux. This has been tested on WSL, so any distribution
   should work fine.
 - A printer. Just a regular, 2D printer that prints on paper.
 - Some glue that can stick to the materials you're printing on.
 - Something to bind the passport: staples, string, wire...

### Step 1: Creating the PDF files

As easy as a `make`.

All you need is a Linux computer with `make`, `python3`, `poppler-utils`,
`firefox` and `imagemagick` installed. You will also need the fonts `DejaVu Sans`
and `DejaVu Serif` which are installed by default on most computers,
and [`Monotype Corsiva`](/resources/MTCORSVA.TTF) and [`OCRB`](/resources/OCRB.otf)
which are in the [`resources`](/resources) folder.

Then open a terminal, `git clone` this repo and run `make` in the cloned directory.

Your Git might be pissed off if you don't have [Git LFS](https://git-lfs.github.com/)
installed, but you don't need it to get the files used by the build scripts.

### Step 2: Printing

There are 2 files to print: `full_cover.pdf` and `passport.pdf`.

`full_cover.pdf` is the outer cover, to be printed on a tough material
(something plastic-like is recommended). If you don't have any you can print
on paper instead.

`passport.pdf` is the inside, to be printed on paper. Thick paper is recommended,
but you can print on regular paper as well. Print on both sides,
and make sure the crop marks are aligned.

Once all is printed, cut the cover along the crop marks. Don't cut the inner pages yet.

> Alternately, you can replace the first page of `passport.pdf` by the one from
> `full_cover.pdf`. Print it on the front side of the paper,
> then continue by printing the second page of `passport.pdf` on the rear side.
> This way, you won't have to glue the outer cover to the passport.

### Step 3: Binding

Stack the inner pages in order. Fold them, make sure the pages with `GLUE FRONT COVER`
and `GLUE BACK COVER` are on the *outside* of the bundle.

Bind the pages using the material of your choice.

Fold the cover and put the pages inside. Align them carefully. Glue the front cover.

Optionally, add an NFC sticker in the circle at the end of the passport. Glue the back cover.

Trim the pages that overflow from the cover. You're done!

## Design

So many things to tell... Well, first off, I wanted this thing as close as possible
to a real passport. My first source of inspiration was
[the Wikipedia page for Passports](https://en.wikipedia.org/wiki/Passport) and
[French Passports](https://en.wikipedia.org/wiki/French_passport).
I also took some information (especially regarding the positions of elements
on the ID page) from ICAO Doc 9303, the one that gives the full specification
for international passports.

First off, the size is the standard TD3 size (height of 125mm and width of 88mm).
It is the same size as regular passports.

The page background is inspired from the security background of passport pages,
with its repeating patterns... except that here it's the Clubelek's logo.
With randomized colors. I went through all the trouble to create randomized
images just for you, you better like them.

The quote on the first page is fitting for the theme of hackers and makers:
"Everyone's got ideas. Often the same ones. What's important, is to know how to use them."
That's precisely our what we do: we use good ideas, and turn them into things,
using our knowledge, skills, and intuition.
The makers are those who know how to use an idea.

After the quote, we have a request for hospitality. That's something often found on passports,
either that or a promise of protection. We can't do much in term of protection,
and it's not very much in the spirit of hackerspaces anyway, so a request for hospitality will do.

> *Placeholder for inner pages*

The last page has legal disclaimers, both so we don't have too much trouble with the law
(imitating an official document and all that), and to mimic the actual disclaimers
at the end of a real passport. In a French passport, they say that the document
is the property of the State of France, and that tempering is prohibited.
But it wouldn't be a *hacker's* passport if one couldn't temper with it, right?
