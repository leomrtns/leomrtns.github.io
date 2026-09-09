# Website transition notes

Maintainer reference for the September 2026 transition to Quarto. Current usage and publishing instructions are in [README.md](README.md).

## Background

The redesign combined the main Jekyll website and its notebook entries into one Quarto website. Publication was approved on 8 September 2026. The main website is now built using GitHub Actions; the source, figures, notebook outputs, and archive references remain in this repository.

`website-redesign` was the development branch for this migration. It is not needed for ordinary updates. Its existing push trigger still runs checks without deploying. Current updates and pull requests target `main`.

## Branch rename

On 9 September 2026, the publishing/default branch changes from `master` to `main`, locally and on GitHub. The workflow push and pull-request filters, deployment conditions, and current authoring instructions use `main`.

For another existing clone that still has a local `master` branch and no local `main` branch, run:

```bash
git branch -m master main
git fetch origin --prune
git branch --set-upstream-to=origin/main main
git remote set-head origin -a
```

The first command renames the local branch. The remaining commands refresh the remote references and upstream after the GitHub rename. These commands do not push. If a local `main` already exists, inspect both branches before renaming; do not force-overwrite it. New clones start on `main` automatically.

## Where to write, and what to keep

An underscore does **not** mean a file or folder is obsolete. Quarto uses some underscore names too.

| Path | Purpose | Can it be moved or deleted? |
| --- | --- | --- |
| `posts/` (no underscore) | Current blog source: one `posts/<YYMMDD-slug>/index.md`, `index.qmd`, or `index.ipynb` per entry, with its figures/downloads. | Keep. Write new entries here. Moving published entries can break their URLs. |
| `old/_data/`, `old/_pages/`, `old/_posts/` | Archived Jekyll data, pages, and posts. Not read by the Quarto build. | Can be removed without breaking the new build. Preserve any original content you still want; the pre-migration version is also saved in the legacy tag. |
| `old/_drafts/` | Original unpublished Jekyll drafts, not current blog entries. | Not needed by the build, but contains writing that was **not migrated into published posts**. Migrate drafts you want before deleting them. |
| `old/_config.yml`, `old/Gemfile`, `old/assets/css/main.scss` | Archived Jekyll configuration, Ruby dependencies, and Minimal Mistakes stylesheet. | The Quarto workflow does not use or publish them. |
| `_quarto.yml` | Active site configuration: pages, theme, navigation, resources, and build hooks. | Keep. |
| `posts/_metadata.yml` and individual posts' `_metadata.yml` files | Active Quarto defaults and notebook download links. | Keep. |
| `_site/` | Generated HTML website and copied assets, created by a render. Git ignores it; it is not blog source. | Safe to delete locally; the next full render recreates it. Do not edit or commit it. Its configured location is used by the workflow and build scripts. |
| `_freeze/` (if present) | Saved computational results for executable `.qmd` posts. Different from `_site/`. | Keep and commit results needed to build those posts without rerunning their analysis environments. Do not treat this as a disposable cache. |
| `publications/_entries.qmd`, `publications/_reviews.qmd` | Generated includes built from saved ORCID data before rendering. Git ignores them. | Safe to delete locally; the build recreates them. Do not edit them manually. |
| `publications/data/` | Saved ORCID works, reviews, and journal names used for offline rendering and fallback. | Keep and commit. |
| `.quarto/`, `.local-state/`, `.ipynb_checkpoints/`, `__pycache__/` | Local build state, temporary files, or editor/runtime caches. | Safe to clear when no render or editing session is using them; they are not published. Preserve any personal files you put there yourself. |
| `.github/workflows/website.yml` | Active GitHub build and deployment workflow. | Keep. |
| `assets/`, `scripts/`, `requirements-render.txt`, `authoring/` | Shared images/styles, build helpers, rendering dependencies, and writing templates/instructions. | Keep. Older-looking assets can still be used by the new pages. |
| `index.md`, `about/`, `projects/`, `blog/`, `publications/`, `doxygen/` | Current website pages. | Keep. |
| `doxygen-biomcmclib/`, `SpecImage/` | Existing documentation and showcase pages, copied into the published website. | Keep if those pages and links should continue working. |

The legacy files are now archived under `old/`. To revive an old draft, copy its text into `posts/<YYMMDD-slug>/index.md`, update its front matter and image paths, and use `draft: true` until it is ready. Simply moving an old Jekyll file into `posts/` does not necessarily convert its metadata or template syntax.


### The old `/jupyterblog/` site

The original notebook site remains online as an archive. Its articles are also available under `posts/` in the new site. Its separate GitHub Pages deployment currently serves `/jupyterblog/`, taking precedence over the compatibility redirects included in the new site's output. It is not part of the routine for adding new posts: write those in this repository's `posts/` folder.


## Previous website

The annotated tag [`legacy-website-2026-09-08`](https://github.com/leomrtns/leomrtns.github.io/tree/legacy-website-2026-09-08) preserves commit `8be9bc946190d9e581d6c2adfdefca19a90d615a`, verified against the last successful deployment before migration. Browse that tag to read the old Markdown posts or download its source archive from GitHub. It contains the original Jekyll site and configuration, not a rendered HTML snapshot. Compare the tag with `main` to review the redesign.

## Content and design

- `index.md`: homepage and selected writing.
- `projects/index.md`: all existing software and companion-analysis links.
- `blog/index.md`: automatic category listing and RSS.
- `publications/index.md`: research outputs from the saved ORCID feed.
- `posts/<YYMMDD-slug>/index.md` or `index.ipynb`: the nine published articles.
- `old/_drafts/`: the five original unpublished drafts, excluded from rendering and deployment.
- `authoring/templates/`: starter Markdown, notebook, and computational posts; excluded from the website.
- `assets/css/theme.scss`: the single active custom stylesheet for site-wide typography, colours, code blocks, and figure layout, layered on Quarto's Cosmo theme.
- `assets/design/leo.mplstyle`: matching Matplotlib defaults for future figures.
- `assets/design/posts/`: schematic thumbnails for the technical articles.
- `doxygen-biomcmclib/` and `SpecImage/`: original documentation resources copied unchanged.
- `scripts/migration-map.json`: migrated routes and notebook code/output fingerprints.
- `scripts/post-render.py`: legacy indexes, feeds, aliases, and attachment paths.

The old Jekyll source folders and configuration remain in Git for reference but are outside Quarto's explicit render list. Posts preserve their original text, apart from correcting one broken `random.org` link. Notebook code and outputs are unchanged; the migration changes metadata and adds stable cell IDs. Run `python3 scripts/validate-site.py --check-migration` to verify the original C code/output fingerprints. This optional audit is not enforced by CI, so intentional future notebook edits remain possible. The home diagram is original schematic geometry, not inferred biological data. The reference site's source and graphics were not copied.


## Verification and local setup

The cleanup guidance was checked on 9 September 2026 by temporarily removing `_data/`, `_drafts/`, `_pages/`, `_posts/`, `_config.yml`, and `Gemfile`, then rendering and validating all 16 pages. The notebook code/output fingerprints and resource checks passed. All six paths were restored; no archived writing was deleted.

During development, portable Quarto and Python tools were installed under the parent project's `.tools/` directory, rather than system-wide. The wrapper detects those when available, but a fresh clone does not contain them.

The [original validation record](authoring/VALIDATION.md) records the migration checks. The saved legacy release is source code and assets, not a rendered HTML snapshot.

## References

- [Fastpages migration](https://nbdev.fast.ai/tutorials/blogging.html)
- [GitHub branch renaming](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-branches-in-your-repository/renaming-a-branch)

## Dated post directories

Post folders now use `YYMMDD-title`. The nine existing entries use their recorded post dates; filesystem creation times from a clone are not meaningful authoring dates. `scripts/migration-map.json` maps the previous undated URLs to the dated articles. The build writes redirects and preserves notebook, image, and attachment downloads at their previous paths. Notebook source, code, and saved outputs are unchanged by the directory renames.

## Styling and image roles

Edit `assets/css/theme.scss` for website appearance. `_quarto.yml` loads it after Quarto's Cosmo theme. The former `assets/design/theme.scss` was moved here; the unused Jekyll `assets/css/main.scss` was archived as `old/assets/css/main.scss`. The independent styles inside `SpecImage/` belong to that preserved showcase and are not the Quarto website theme.

`assets/design/leo.mplstyle` styles newly generated Matplotlib plots, not website HTML. Existing generated illustrations remain under `assets/design/`; shared new images can go in `assets/images/`. Put an article's own figures and downloads beside its `index.md`, `index.qmd`, or `index.ipynb`. Image styling no longer tests for `logo_` in filenames or `design/posts/` in paths. Moving an image only requires updating its references, not its styling rules.

| Role / selector in the theme | Image treatment | Background location |
| --- | --- | --- |
| Homepage illustration: `.hero-diagram` | Full image, automatic height, original saturation. | Its `.hero-science` container. |
| Project cards: `.project-art img` | `saturate(.45)`; fills a 170px-high frame with `object-fit: cover`, positioned at `67% center`. Cropping is intentional in the current layout. | Its `.project-art` container. |
| Blog introduction mascot: `.blog-mascot img` | `saturate(.45)`; fills a 210×145px frame with the same cropping and position as project artwork. | Its `.blog-mascot` container. |
| Blog listing thumbnails: `.quarto-listing-default .quarto-post .thumbnail img` | All use `saturate(.45)` and centred `object-fit: contain` in a 160px-high frame, showing the whole image. | The enclosing thumbnail link. |
| Scientific figures inside articles | Original saturation; normal responsive sizing. | No shared decorative background is added by these rules. |

No image uses `mix-blend-mode` in the website theme. Reduced saturation still changes image colours; it does not remove an opaque background. Transparent pixels reveal the container underneath, while opaque white stays white. The decorative background is outside the filtered image, so the filter does not desaturate the container itself. A plot selected as a blog thumbnail receives the thumbnail treatment there; its version inside the article remains unaffected.

Change `--figure-background` and `--figure-wash` near the top of the theme to adjust the pale background/gradient. **The review summary panel also uses `--figure-wash`**, so it changes too. Some other colours are separate SCSS variables or literal values; changing one variable does not recolour the entire website. Project-card top borders alternate by `nth-child`, so rearranging cards changes their accent colours. The HTML image width/height attributes describe the existing artwork; review these and the fixed frames when replacing images of different proportions.

## Maintenance caveats retained intentionally

These are current behaviours to account for when editing. They were documented during the stylesheet cleanup, without changing the associated scripts, templates, or workflow.

### Publishing validation is tied to current content

`scripts/validate-site.py` runs in GitHub Actions and can block publication even when Quarto renders successfully. It currently requires exactly **14 project cards on Projects and three on the homepage**, the Liverpool profile URL and all seven footer icons, the configured ORCID link, and the exact HTML text `<summary>Reviewing by journal</summary>`. It also rejects a Binfie category shortcut on Projects and requires a thumbnail for each listed article.

When deliberately adding/removing project cards, changing footer links, or renaming the reviewing disclosure, update the corresponding checks as part of that edit. Their current locations can be found by searching the validator for `project-art`, `footer`, `ORCID`, or `Reviewing by journal`. Run a full render and validation before pushing. A failed workflow leaves the previous successful deployment online.

### Post structure, templates, and computations

- Keep one `posts/YYMMDD-title/index.*` source per article, directly one level below `posts/`. Quarto's render/listing patterns are recursive, but the post-render download/draft handling and validator use `posts/*/index.*`; adding year subfolders would require adjusting those scripts too.
- Blog order comes from the front-matter `date`, not the directory name. Changing that date does not rename the folder. The helper chooses the prefix when creating the post and refuses to overwrite an existing destination.
- Notebook metadata belongs in the first Raw cell, as in the provided template. Post-render handling reads that cell. Notebook downloads are copied automatically for published entries; add the per-post `_metadata.yml` described in the authoring guide to expose a download button.
- The notebook and executable `.qmd` templates still supply the **Binfie Notes** category. Replace it in each new post if unwanted. All templates start with `draft: true`; change it when ready. Draft source committed to this public repository remains publicly readable even when excluded from the rendered website.
- Notebooks are not executed during the normal website build. Run changed computations and save their outputs yourself. Executable `.qmd` posts need an explicit local render and committed `_freeze/` results. Whole-site builds with `freeze: true` can reuse results even after source edits; rerender the individual document to refresh them.
- `requirements-render.txt` installs rendering dependencies only. The executable template additionally needs a Python/Jupyter environment with NumPy and Matplotlib. Missing frozen results may make a GitHub build attempt computations without the needed analysis environment.
- `posts/_metadata.yml` supplies the default author and raccoon thumbnail. Override `image` and `image-alt` in a post to select its own thumbnail. Ordinary Markdown image links can be relative to that post's folder.

### Pages, paths, and archived URLs

- New posts enter Blog, categories, search, and RSS automatically. Homepage featured articles and project cards are authored manually in `index.md` and `projects/index.md`.
- Add a new top-level page to `project.render` in `_quarto.yml`; add its navigation entry separately. The validator also has an explicit list of main pages if you want the new page checked.
- `_site/` is configured in `_quarto.yml`, but also named in the workflow and validator. Changing the output directory requires updating all of those; the post-render script reads Quarto's output-directory environment variable with `_site` as fallback.
- The site URL and footer identity are configured in `_quarto.yml`; the ORCID ID is also embedded in `scripts/update-publications.py` and the validator. Moving the website to a repository subpath would require reviewing root-relative links and these settings.
- `scripts/migration-map.json` and `scripts/post-render.py` retain redirects and old download URLs for existing articles. New posts need no migration-map entry or redirects. Renaming, deleting, or hiding a mapped article requires reviewing its mapping, manual links, and validation expectations. The validator requires all mapped articles/aliases and at least as many RSS entries as mapped articles. Notebook fingerprint comparison is only enabled by `--check-migration`.
- Do not remove the whole post-render script just to remove redirects: it also creates `.nojekyll`, handles draft output, and copies downloadable notebooks. The historical attachment path is explicitly named there.
- `doxygen-biomcmclib/` and `SpecImage/` are copied unchanged, and the validator compares their resources. All of `assets/` is a published resource; keep private files and maintainer notes elsewhere. `old/` is excluded from the rendered website, but its committed contents remain available on GitHub.

### ORCID refreshes and local tooling

The Publications page refreshes during workflow builds, including a manual run on `main`; there is no schedule or browser-side live fetch. Only public ORCID records are available. Failed refreshes retain saved data, so the site can remain available with an older visible refresh date. GitHub refreshes do not commit updated snapshots back into the repository. Keep `publications/data/` for offline rendering/fallback, and commit locally refreshed snapshots when desired. Journal-name lookups are cached separately in `review-venues.json`; inspect that file when a label needs correction. Do not edit generated `_entries.qmd` or `_reviews.qmd`: the pre-render hook replaces them.

Only `main` builds deploy. The old `website-redesign` push trigger still runs checks without publishing; pull requests targeting `main` also run checks without merging or deploying. Publishing requires a push/merge to `main` or a manual workflow run on `main`.

`scripts/quarto.sh` can detect the development installations in the parent project's `.tools/website-authoring-env/` and `.tools/quarto-1.10.18/`; those paths are not included in a clone. On another machine, install Quarto and your Python environment and use `QUARTO_BIN` / `QUARTO_PYTHON` as necessary. Version references also appear in the workflow and README. The wrapper directs its configured temporary/cache directories into `.local-state/`; it sets `TMPDIR` but does not set every possible tool's cache or `TMP`/`TEMP` variable. For additional tools, configure their temporary files and environments under the active project too.
