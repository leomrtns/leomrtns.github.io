# Writing posts

The blog accepts `.md`, `.qmd`, and `.ipynb` files. Use one `posts/<slug>/index.<extension>` per article. Images and downloads go in the same folder. Do not keep both `index.md` and `index.qmd` for one article: both would generate `index.html`.

## Obsidian

Open this repository, or just `posts/`, as an Obsidian vault. `.obsidian/` settings are ignored by Git. Write `.md` files; they render directly in Quarto. Obsidian does not support `.qmd` as a native note format without an extra plugin, and none is needed for this workflow.

Create a draft from the repository root:

```bash
python3 scripts/new-post.py sequence-notes --title "Notes on sequences" --format md
```

Open `posts/sequence-notes/index.md` in Obsidian. Replace the sample text, description and categories. The top of the note is ordinary YAML metadata:

```yaml
---
title: "Notes on sequences"
date: 2026-09-08
description: "What these notes explain."
categories: [phylogenetics]
draft: true
---
```

Set `draft: false` when ready. Drafts are excluded from the public site, search and RSS. The original `_drafts/` folder is completely excluded; to publish one of those drafts, copy it into a new post folder and explicitly set its publication date and status.

Use portable Markdown, including `$inline math$` and `$$display math$$`. Use `[label](../other-post/index.md)` and `![caption](figure.svg)`, not Obsidian-only `[[wikilinks]]`, `![[embeds]]`, Dataview, or plugin-specific syntax. Obsidian's New link format can be set to Relative path, and Use Wikilinks turned off. Settings are not changed automatically. Quarto-specific citations and cross-references are checked in the website preview; Obsidian's preview may differ.

## VS Code notebooks

```bash
python3 scripts/new-post.py notebook-notes --title "Notebook notes" --format ipynb
```

Select your existing kernel, edit text/code cells, run the computations, and **save the notebook with outputs**. Edit title, date and categories in the first Raw cell. Set `draft: false` when ready.

The website does not execute notebooks by default. This permits C notebooks, old dependencies, long computations and offline results to coexist. Changing code without rerunning it would leave stale output, so run the relevant cells and save before publishing a changed computation. Rendering old notebooks is not a claim that their calculations were reproduced.

For a downloadable notebook link, add a `_metadata.yml` alongside it:

```yaml
format:
  html:
    code-links:
      - text: Download notebook
        icon: download
        href: index.ipynb
```

## Plain-text computational documents (`.qmd`)

A `.qmd` file is an ordinary text file. You can create one in any editor by saving with that extension; Jupyter's notebook UI is optional. VS Code's Quarto extension provides syntax assistance and preview. Jupyter/Python or R is needed only when the document executes code using that engine.

```bash
python3 scripts/new-post.py density-example --title "A density example" --format qmd
```

This template includes an executable Python example, a LaTeX equation and a labelled figure. Install its NumPy/Matplotlib dependencies in your analysis environment. Set `QUARTO_PYTHON` to that environment's Python if needed, then render the individual post:

```bash
./scripts/quarto.sh render posts/density-example/index.qmd
```

The template explicitly enables execution and freezes its results. Commit the resulting `_freeze/` files with the source. A whole-site build can then reuse those computations without installing every historical analysis dependency. If the file has never been rendered locally, there are no frozen results to reuse. Explicitly rendering the individual post updates the computation; a whole-site render with `freeze: true` reuses existing results even if the source has changed.

For a prose-only `.qmd`, remove the `jupyter` and executable-code settings, or use `.md` instead. Code blocks marked with a language (` ```c `) display code; Quarto computational blocks (` ```{python} `) can execute it when enabled.

## Figures

Every blog listing entry has a thumbnail. Set these fields in a post's YAML header (the first Raw cell for a notebook):

```yaml
image: thumbnail.svg
image-alt: A short description of the figure
```

Put that image beside the post, or use a shared `/assets/...` path. Posts without an explicit image inherit the raccoon from `posts/_metadata.yml`. Listing diagrams illustrate the article's topic; they are not additional experimental results.

Project artwork keeps its original files under `assets/images/`. CSS gives it a consistent frame, softens saturation, and blends white into the shared blue/teal background. Scientific plots inside articles keep their original colours.

To replace the homepage figure, change the `<img>` source and alt text in `index.md`, and update its width/height to the new image's proportions. Transparent SVG or PNG artwork will reveal the default background beneath it. The background belongs to `.hero-science`, independently of the image; change `--figure-background` and `--figure-wash` in `assets/design/theme.scss` to adjust it everywhere those figure surfaces are used.

Existing notebook outputs and the colour-printing screenshot are preserved. Their surrounding layout, caption typography, and code blocks share the site's design. Do not recolour an image where colour is part of the example or a scientific encoding.

For new Matplotlib figures:

```python
plt.style.use("/path/to/this/repository/assets/design/leo.mplstyle")
```

The `.qmd` template locates this style relative to the project. Prefer SVG for line plots and diagrams; use PNG for dense raster images. Include descriptive captions, axis labels and units; keep categorical colours consistent across figures. The palette is teal `#126c70`, blue `#275ca0`, ochre `#8c6126`, and violet `#765194`.

For ordinary images in Markdown:

```markdown
![A caption that explains the plotted comparison.](figure.svg){#fig-comparison}

The result is shown in @fig-comparison.
```

## Publishing routine

1. Write in Obsidian or VS Code.
2. Run and save changed notebook computations, or explicitly render a computational `.qmd` to update `_freeze/`.
3. Preview locally and set `draft: false` for articles ready to publish.
4. Build and validate with `./scripts/quarto.sh render` and `python3 scripts/validate-site.py`.
5. Commit and push source changes directly to `master`. GitHub Actions builds, checks, and deploys the HTML automatically. No pull request is required for this route.

A local render does not publish anything. Pushing source changes to `master` starts the GitHub build and publication workflow. If you choose a separate branch, open a pull request targeting `master` and merge it yourself after its checks pass; the workflow does not merge it for you. New posts appear automatically in the Blog listing, search, and RSS. Homepage article selections are edited separately in `index.md`.

See the [repository README](../README.md) for the folder cleanup guide and exact workflow triggers. `_site/` is generated output, `_quarto.yml` and `_metadata.yml` are active configuration, and `_freeze/` contains saved computations—underscore names are not generally obsolete.
