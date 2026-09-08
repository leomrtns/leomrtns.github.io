# Leo Martins — website and blog

A Quarto website combining the project directory, personal blog, and Binfie Notes. The intended address is **https://leomrtns.github.io/**. Source lives in the existing `leomrtns.github.io` repository; the local redesign branch is `website-redesign`.

Nothing has been published as part of the local migration. Pushes and any GitHub Pages configuration changes require Leo's approval.

## Write in the editor you already use

| File | Editor | What is required |
| --- | --- | --- |
| `.ipynb` | VS Code's notebook editor or JupyterLab | Existing notebook kernel to run your code; save cell outputs. |
| `.md` | Obsidian or any text editor | Nothing beyond the editor for prose, mathematics, and displayed code. |
| `.qmd` | VS Code or any text editor | Quarto for preview; the relevant Python/R/Julia environment if code should execute. |

Quarto is the renderer, not a new editor. Its optional VS Code extension adds preview and assistance. Jupyter is not needed just to write Markdown or mathematics. Plain `.md` posts are built directly: no renaming or conversion is required for Obsidian.

See [the authoring guide](authoring/README.md) for examples, figures, frozen computations, and new-post commands.

## Local preview

Use Quarto **1.10.18** and Python 3.12 with `requirements-render.txt`. There is no need for Ruby, Jekyll, Docker, a C compiler, or the old C kernel to render the archived notebooks.

In the current local project, Quarto and a Python environment have already been downloaded under the parent project's `.tools/` directory. Nothing was installed system-wide. The wrapper detects those tools and keeps its caches inside the repository:

```bash
./scripts/quarto.sh preview --host 127.0.0.1 --port 4260 --no-browser
```

Open `http://127.0.0.1:4260/`. Stop an active Quarto preview with Ctrl+C before running a separate full render; simultaneous render processes share temporary output files. To build and validate without starting a server:

```bash
./scripts/quarto.sh render
python3 scripts/validate-site.py
```

On another computer, install Quarto 1.10.18 from its official distribution and install `requirements-render.txt` in a project-local virtual environment. The wrapper also accepts `QUARTO_BIN` and `QUARTO_PYTHON`, or uses Quarto on PATH. The plain `quarto render` command works in CI.

## Automatic GitHub publishing — prepared, not activated

The workflow in `.github/workflows/website.yml`:

1. Builds and validates pushes to `website-redesign`, pushes to `master`, and pull requests targeting `master`.
2. Publishes **only from `master`**, using GitHub Pages Actions. A push to the redesign branch cannot deploy the website through this workflow.
3. Renders stored notebook results rather than executing old analysis environments.
4. Uploads only `_site/`, never the repository as a whole.

After reviewing and approving the redesign, the recommended deployment is to keep this repository, set Settings → Pages → Source to **GitHub Actions**, and merge the approved branch into `master`. The site remains at `https://leomrtns.github.io/`; a new project repository would normally add its name to the URL. Do not change the publishing source while the old site is still intended to serve from Jekyll.

If a different repository or branch is chosen, adjust `_quarto.yml` (`site-url`) and the workflow's branch triggers and deployment conditions before pushing. No GitHub settings have been changed. Workflow execution on GitHub has not yet been tested.

### The old `/jupyterblog/` site

Redirect pages and old RSS paths are included in the main site's output. GitHub Pages can serve a separately deployed project site at `/jupyterblog/` ahead of the user site's files at that path. Therefore, when the main migration is ready, choose one of:

- Disable the old `jupyterblog` Pages deployment so the main site's compatibility routes can serve that path; keep the source repository as an archive.
- Publish redirects from the old repository itself.

This is a separate, approval-required publishing step. Do not delete the notebook repository. The local migration does not depend on changing it.

## Content and design

- `index.md`: homepage and selected writing.
- `projects/index.md`: all existing software and companion-analysis links.
- `blog/index.md`: automatic category listing and RSS.
- `posts/<slug>/index.md` or `index.ipynb`: the nine published articles.
- `_drafts/`: the five original unpublished drafts, excluded from rendering and deployment.
- `authoring/templates/`: starter Markdown, notebook, and computational posts; excluded from the website.
- `assets/design/theme.scss`: site-wide typography, colours, code blocks, and figure layout.
- `assets/design/leo.mplstyle`: matching Matplotlib defaults for future figures.
- `doxygen-biomcmclib/` and `SpecImage/`: original documentation resources copied unchanged.
- `scripts/migration-map.json`: migrated routes and notebook code/output fingerprints.
- `scripts/post-render.py`: legacy indexes, feeds, aliases, and attachment paths.

The old Jekyll source folders and configuration remain in Git for reference but are outside Quarto's explicit render list. Posts preserve their original text, apart from correcting one broken `random.org` link. Notebook code and outputs are unchanged; the migration changes metadata and adds stable cell IDs. Run `python3 scripts/validate-site.py --check-migration` to verify the original C code/output fingerprints. This optional audit is not enforced by CI, so intentional future notebook edits remain possible. The home diagram is original schematic geometry, not inferred biological data. The reference site's source and graphics were not copied.

## References

- [Quarto in VS Code](https://quarto.org/docs/tools/vscode/index.html)
- [Quarto blogs](https://quarto.org/docs/websites/website-blog.html)
- [Fastpages migration](https://nbdev.fast.ai/tutorials/blogging.html)
- [GitHub Pages custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
