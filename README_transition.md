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
| `posts/` (no underscore) | Current blog source: one `posts/<slug>/index.md`, `index.qmd`, or `index.ipynb` per entry, with its figures/downloads. | Keep. Write new entries here. Moving published entries can break their URLs. |
| `_data/`, `_pages/`, `_posts/` | Old Jekyll data, pages, and posts. Not read by the Quarto build. | Can be removed or archived without breaking the new build. Preserve any original content you still want; the pre-migration version is also saved in the legacy tag. |
| `_drafts/` | Original unpublished Jekyll drafts, not current blog entries. | Not needed by the build, but contains writing that was **not migrated into published posts**. Archive it or migrate drafts you want before deleting it. |
| `_config.yml`, `Gemfile` | Old Jekyll configuration and Ruby dependencies. | Can be archived or removed; the Quarto workflow does not use them. |
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

No folders were deleted as part of this documentation update. To revive an old draft, copy its text into `posts/<slug>/index.md`, update its front matter and image paths, and use `draft: true` until it is ready. Simply moving an old Jekyll file into `posts/` does not necessarily convert its metadata or template syntax.


### The old `/jupyterblog/` site

The original notebook site remains online as an archive. Its articles are also available under `posts/` in the new site. Its separate GitHub Pages deployment currently serves `/jupyterblog/`, taking precedence over the compatibility redirects included in the new site's output. It is not part of the routine for adding new posts: write those in this repository's `posts/` folder.


## Previous website

The annotated tag [`legacy-website-2026-09-08`](https://github.com/leomrtns/leomrtns.github.io/tree/legacy-website-2026-09-08) preserves commit `8be9bc946190d9e581d6c2adfdefca19a90d615a`, verified against the last successful deployment before migration. Browse that tag to read the old Markdown posts or download its source archive from GitHub. It contains the original Jekyll site and configuration, not a rendered HTML snapshot. Compare the tag with `main` to review the redesign.

## Content and design

- `index.md`: homepage and selected writing.
- `projects/index.md`: all existing software and companion-analysis links.
- `blog/index.md`: automatic category listing and RSS.
- `publications/index.md`: research outputs from the saved ORCID feed.
- `posts/<slug>/index.md` or `index.ipynb`: the nine published articles.
- `_drafts/`: the five original unpublished drafts, excluded from rendering and deployment.
- `authoring/templates/`: starter Markdown, notebook, and computational posts; excluded from the website.
- `assets/design/theme.scss`: site-wide typography, colours, code blocks, and figure layout.
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
