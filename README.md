# abox.tools translations, frozen

Thirteen of the site's languages as they were on 11 September 2026, kept
exactly as they were deployed, and served from here rather than rebuilt:

Arabic (`ar`), German (`de`), Spanish (`es`), French (`fr`), Hindi (`hi`),
Indonesian (`id`), Italian (`it`), Japanese (`ja`), Korean (`ko`), Dutch (`nl`),
Portuguese (`pt`), Turkish (`tr`) and Traditional Chinese (`zh-TW`).

English and Simplified Chinese are still built from
[A-Box-of-Tools/website](https://github.com/A-Box-of-Tools/website) and are the
languages the site is maintained in.

## Why they stopped being built

Every change to a tool in English had to be made fourteen more times, once per
translated copy of its page, or the build refused it. Almost nobody was reading
the thirteen: over the 28 days to 6 September 2026, 99.05% of arrivals landed on
an English page, Simplified Chinese had 395, the best of the rest had 35 and
three had one apiece. They were already out of the sitemap, the hreflang sets
and the language switcher, with `noindex` on every page.

So the work is kept and the upkeep is not. Every page here still answers at the
address it always had, in the language it was translated into, and a reader with
a bookmark still gets it. What it does not get is anything that changes in
English after this date: a new tool has no page here, and a fixed bug stays
unfixed in these copies.

## What is here

- `site/<lang>/` - the deployed pages, from the `dist` build of website 1.4.2
  (website commit `332ef1cb2e1c681d0028dbc841482626e516f1a8`, dist build
  `676716c`). The website's deploy copies these folders into the site at a
  pinned commit of this repository, so nothing pushed here reaches
  abox.tools until the website says so.
- `source/locales/<lang>/` - the translation sources those pages were built
  from, at the same website commit, for anybody who wants to read or revive one.
- `freeze.py` and `verify_freeze.py` - how this was made, and the check that it
  was made right.

### The one change from what was deployed

Each page used to load seven small frame scripts from the site root -
`lang.js`, `lang-keep.js`, `handoff.js`, `feedback.js`, `page-md.js`,
`offline.js` and `hub-filter.js`. Those root copies belong to the English build
and will change with it, and a frozen page that loaded tomorrow's version of
them could break without a byte of this repository moving. So each language
folder carries its own copies, as they were deployed, and its pages load those:
`/lang.js?v=...` became `/de/lang.js?v=...` and so on. Nothing else was touched.

`verify_freeze.py` proves it against the deployed tree: of 17,965 files, 16,457
are byte-identical to what was live, 1,417 pages differ only in those script
paths, and the other 91 are the copies themselves.

They still share three things with the live site, all of them harmless if they
change: `/sitemap.xml` (named in a `<link>`), `/icon-180.png` and `/logo.svg`,
and the links to the English and Chinese pages they were translated from.

## Bringing a language back

Move `source/locales/<lang>/` back into the website's `locales/`, take the
language off `frozen_languages` in its `config/site.toml`, and translate what
English has gained since. Its folder here then stops being deployed the day the
website builds it again. Editing `site/` by hand is possible and is best kept
for an emergency: whatever is changed here is changed only here.
