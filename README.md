# Leo Martins — website and blog

This Quarto website is live at **https://leomrtns.github.io/**. It combines projects, publications, the personal blog, and the former notebook blog. **`master` is the publishing branch.** You can commit and push ordinary updates directly to `master`; no pull request is required. `website-redesign` was used to develop the migration and is not required for future posts.

The redesign and GitHub Pages migration were approved on 8 September 2026. The previous website is preserved by the `legacy-website-2026-09-08` tag.

## Write in the editor you already use

| File | Editor | What is required |
| --- | --- | --- |
| `.ipynb` | VS Code's notebook editor or JupyterLab | Existing notebook kernel to run your code; save cell outputs. |
| `.md` | Obsidian or any text editor | Nothing beyond the editor for prose, mathematics, and displayed code. |
| `.qmd` | VS Code or any text editor | Quarto for preview; the relevant Python/R/Julia environment if code should execute. |

Quarto is the renderer, not a new editor. Its optional VS Code extension adds preview and assistance. Jupyter is not needed just to write Markdown or mathematics. Plain `.md` posts are built directly: no renaming or conversion is required for Obsidian.

See [the authoring guide](authoring/README.md) for examples, figures, frozen computations, and new-post commands.

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

## Each new post or update

The simplest routine is to work directly on `master`:

1. Start from the latest source (`git switch master`, then `git pull --ff-only origin master`). Finish or commit any current work before switching branches.
2. Edit the appropriate source file. For a new article, create `posts/<slug>/index.md`, `index.qmd`, or `index.ipynb`; the [authoring guide](authoring/README.md) includes starter commands and examples. Put figures beside the entry. Do not create more than one `index` source format in the same article folder.
3. For a notebook, run changed computations in your own environment and save its outputs. For an executable `.qmd`, explicitly render that post locally and include its updated `_freeze/` results. Ordinary Markdown needs no code execution.
4. Set the post's title, date, description, categories, and `draft: false` when ready. Preview locally if possible; GitHub also validates every publishing build. `draft: true` excludes a post from the website, but **committed drafts are still visible in this public GitHub repository**.
5. Commit the source files and push to `master`. GitHub builds and publishes automatically; you do not upload HTML yourself.
6. Check **Actions → Build and publish website** for a successful build and deployment. If a build or validation fails, fix the reported problem and push again; that failed build does not replace the last successfully deployed site.

For example, after editing a Markdown post:

```bash
git add posts/my-new-article
git commit -m "Add my new article"
git push origin master
```

Stage any other changed source, figures, or `_freeze/` results too. Inspect `git status` before committing so that you include the intended files.

You can also create/edit Markdown directly on GitHub and choose **Commit directly to the master branch**. That commit triggers the same workflow. No local Quarto installation is needed for that route. For notebooks, use VS Code/Jupyter locally so you can run and save computations before uploading the notebook.

New published posts are automatically included in the Blog listing, categories, search, and RSS. The selected articles on the **homepage are curated manually in `index.md`**; adding a blog post does not automatically replace those selections.

### Optional branch and pull-request route

A branch is useful when you want to review changes before publishing, but it is optional. Push your branch, open a pull request targeting `master`, let the checks pass, and **merge it yourself**. The merge updates `master` and triggers publication. This workflow never opens pull requests, merges branches, or pushes generated files back into Git.

## What GitHub does automatically

The actual workflow is [`.github/workflows/website.yml`](.github/workflows/website.yml):

| Action | Builds and checks? | Publishes the live website? |
| --- | --- | --- |
| Push/commit to `master`, including merging a pull request | Yes | Yes, after the build and validation pass |
| Push to `website-redesign` | Yes | No |
| Open or update a pull request targeting `master` | Yes | No; you still need to merge it |
| Push to another branch without a pull request | No, under the current push filters | No |
| Actions → Run workflow, selecting `master` | Yes | Yes |
| Actions → Run workflow, selecting another branch that contains this workflow | Yes | No |

For each triggered build, GitHub checks out the source, installs Quarto/Python rendering dependencies, runs the ORCID parser tests, refreshes publications and peer-review data, renders the site, and validates its pages and links. It generally uses saved notebook outputs and committed frozen `.qmd` results; it does not provision all your analysis environments or rerun old notebooks by default.

**“Uploads only `_site/`” refers to the deployment artifact sent to GitHub Pages.** Quarto creates `_site/` on the GitHub runner from the committed source. The workflow uploads that generated folder and deploys it; it does not commit `_site/` to the repository. A normal `git push` still uploads your source commits to GitHub, including any tracked drafts or archived folders. Repository visibility and website publication are separate things.

GitHub Pages is configured to use **GitHub Actions**, with source on `master`. There is no scheduled ORCID refresh: it happens on these workflow builds or when you use **Run workflow**. You do not need to edit the workflow for each post.

## Local preview

Use Quarto **1.10.18** and Python 3.12 with `requirements-render.txt`. There is no need for Ruby, Jekyll, Docker, a C compiler, or the old C kernel to render the archived notebooks.

The wrapper can use installed Quarto, explicit `QUARTO_BIN`/`QUARTO_PYTHON` settings, or the portable tools under the parent project's `.tools/` directory when those are available. A fresh clone does not itself install these tools.

```bash
./scripts/quarto.sh preview --host 127.0.0.1 --port 4260 --no-browser
```

Open `http://127.0.0.1:4260/`. Stop an active Quarto preview with Ctrl+C before running a separate full render; simultaneous render processes share temporary output files. To build and validate without starting a server:

```bash
./scripts/quarto.sh render
python3 scripts/validate-site.py
```

On another computer, install Quarto 1.10.18 from its official distribution and install `requirements-render.txt` in a project-local virtual environment. The plain `quarto render` command works in CI.

### The old `/jupyterblog/` site

The original notebook site remains online as an archive. Its articles are also available under `posts/` in the new site. Its separate GitHub Pages deployment currently serves `/jupyterblog/`, taking precedence over the compatibility redirects included in the new site's output. It is not part of the routine for adding new posts: write those in this repository's `posts/` folder.

## Publications from ORCID

The Publications page uses the public works and peer-review feeds for [ORCID 0000-0001-5247-1320](https://orcid.org/0000-0001-5247-1320). It lists the preferred record from each ORCID work group, removes duplicate DOIs, and groups results by publication year. Article, preprint, and other output types remain labelled as supplied by ORCID. It does not scrape Google Scholar or require manual website entries.

To refresh locally:

```bash
python3 scripts/update-publications.py --refresh
./scripts/quarto.sh render
```

Ordinary local renders use the saved feeds under `publications/data/` without a network request. The generated `publications/_entries.qmd` and `_reviews.qmd` are rebuilt automatically and should not be edited. Peer-review totals count each ORCID review group once, excluding editor roles. The expandable table ranks journals by their recorded review counts, while funding and other reviewing are shown separately. Only public ORCID review records are included; these are review activities, not necessarily distinct manuscripts or a complete career total. Journal names are resolved from Crossref ISSNs and cached; the ISSN registry supplies the name for one journal absent from Crossref. Unresolved new identifiers remain visible until their name can be fetched. The page shows the date of the last successful download. If ORCID is unavailable or returns invalid/empty data, refreshing retains the saved list and prints a warning; it fails if there is no saved list to use.

Every workflow build refreshes both ORCID feeds first. To update publications and reviewing, open **Actions → Build and publish website → Run workflow**, choosing `master`. No source edit or new commit is required. Running it on `website-redesign` only builds and validates. ORCID changes are picked up at the next build, not on every visitor's page load. Refreshes on GitHub affect that deployment but are not committed back into `publications/data/`; to update the saved offline snapshot in Git, run the local refresh command and commit its changed data files. The website can only list works made public on that ORCID record.

## Previous website

The annotated tag [`legacy-website-2026-09-08`](https://github.com/leomrtns/leomrtns.github.io/tree/legacy-website-2026-09-08) preserves commit `8be9bc946190d9e581d6c2adfdefca19a90d615a`, verified against the last successful deployment before migration. Browse that tag to read the old Markdown posts or download its source archive from GitHub. It contains the original Jekyll site and configuration, not a rendered HTML snapshot. Compare the tag with `master` to review the redesign.

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

## References

- [Quarto in VS Code](https://quarto.org/docs/tools/vscode/index.html)
- [Quarto blogs](https://quarto.org/docs/websites/website-blog.html)
- [Fastpages migration](https://nbdev.fast.ai/tutorials/blogging.html)
- [GitHub Pages custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
