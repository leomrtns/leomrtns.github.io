# Leo Martins — website and blog

Source for **[leomrtns.github.io](https://leomrtns.github.io/)**: projects, publications, and articles on computational biology, evolutionary genomics, mathematics, and programming. Built with Quarto and published through GitHub Pages.

## Write a post

Create one folder per article under `posts/`, named `YYMMDD-title`, with one of these source files:

| File | How to write it |
| --- | --- |
| `posts/260909-my-article/index.md` | Markdown, mathematics, and displayed code in Obsidian or any text editor. |
| `posts/260909-my-article/index.ipynb` | A Jupyter notebook edited in VS Code or Jupyter; run changed computations and save the outputs. |
| `posts/260909-my-article/index.qmd` | A Quarto document; explicitly render executable code locally and commit its `_freeze/` results. |

The prefix records the post date when the directory is created; `260909` means 9 September 2026. The new-post helper adds today’s prefix automatically:

```bash
python3 scripts/new-post.py my-article --title "My article" --format md
```

Use `--date 2026-09-09` to choose a different date. Keep the directory name stable after publication; changing the date in the article metadata does not require renaming the directory.

Put figures and downloads beside the entry. Use only one `index` source format per article. For example, a Markdown post starts with:

```yaml
---
title: "My article"
date: 2026-09-09
description: "A short introduction."
categories: [phylogenetics]
draft: false
---
```

Write the article below that header. An optional `image` field selects the listing thumbnail; otherwise the blog mascot is used. `draft: true` keeps an entry off the website, but its source is still visible if committed to this public repository.

The [authoring guide](authoring/README.md) covers starter commands, notebook metadata, figures, and computational documents.

## Preview locally

Use Quarto **1.10.18**, Python 3.12, and the packages in `requirements-render.txt`, installed in your Python environment. The wrapper uses Quarto on PATH or the explicit `QUARTO_BIN` and `QUARTO_PYTHON` settings.

```bash
./scripts/quarto.sh preview --host 127.0.0.1 --port 4260 --no-browser
```

Open `http://127.0.0.1:4260/`. Stop preview before running a separate full build:

```bash
./scripts/quarto.sh render
python3 scripts/validate-site.py
```

## Publish an update

**`main` is the publishing branch.** A pull request is optional.

1. Start from the latest `main`: `git switch main`, then `git pull --ff-only origin main`.
2. Edit source files, save notebook outputs or updated `.qmd` computations as needed, and preview the result.
3. Set `draft: false` for posts ready to publish. Commit the source, figures, and any required `_freeze/` results, then push to `main`.
4. Check **Actions → Build and publish website** for successful validation and deployment.

For example, after editing a Markdown article:

```bash
git add posts/260909-my-article
git commit -m "Add my article"
git push origin main
```

Markdown can also be edited on GitHub and committed directly to `main`. If you choose a separate branch, open a pull request targeting `main` and merge it after the checks pass. The workflow does not open or merge pull requests for you.

Each push to `main` automatically refreshes ORCID data, builds the site, validates its pages and links, and deploys it. Pull requests run checks without publishing. A failed build does not replace the last successful deployment.

Quarto generates `_site/`; the workflow uploads that folder to GitHub Pages. **Do not edit or commit `_site/`.** Git pushes contain source commits; the Pages deployment contains the generated website. There is no need to edit the [workflow](.github/workflows/website.yml) for each post.

New posts automatically appear in Blog, categories, search, and RSS. Featured articles on the homepage are selected manually in `index.md`.

## Publications and peer reviewing

The Publications page reads public works and reviewing records from ORCID. Every workflow build refreshes them automatically. To refresh without a source change, choose **Actions → Build and publish website → Run workflow → main**. There is no scheduled refresh.

Local builds use the saved data under `publications/data/`. To update that snapshot:

```bash
python3 scripts/update-publications.py --refresh
./scripts/quarto.sh render
```

Commit changed data files if the refreshed snapshot should be saved in Git. Refreshes on GitHub update that deployment without committing data back to the repository. If a remote refresh fails, the saved list is retained and its refresh date remains visible.

## Project files

| Path | Purpose |
| --- | --- |
| `index.md`, `about/`, `projects/`, `blog/`, `publications/` | Website pages. |
| `posts/` | Blog sources, figures, and downloads. |
| `_quarto.yml`, `posts/_metadata.yml` | Site configuration and post defaults. |
| `_freeze/`, when present | Saved computational results to commit with executable posts. |
| `assets/` | Shared artwork, styles, and the Matplotlib style. |
| `scripts/`, `.github/workflows/website.yml` | Build helpers and automatic publishing. |
| `publications/data/` | Saved ORCID records and journal names. |

Further reading: [authoring guide](authoring/README.md), [transition notes](README_transition.md), [Quarto documentation](https://quarto.org/docs/guide/).
