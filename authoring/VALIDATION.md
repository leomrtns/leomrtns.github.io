# Local validation — 8 September 2026

Built with Quarto 1.10.18 and Python 3.12. This is a local source/build validation; the GitHub workflow has not run and no site has been uploaded.

- Full render succeeds for the homepage, project directory, blog, about, documentation index, 404 page, and nine articles (15 pages).
- All internal links and image/script/style resources from those pages resolve. Existing external links were preserved; their remote availability was not exhaustively tested.
- All five C notebooks retain byte-equivalent code cell sources, outputs, and execution counts, compared through canonical JSON fingerprints to the old repository.
- All notebooks have local downloadable `.ipynb` files.
- All nine migrated posts appear in RSS; the old feed paths mirror the new feed.
- Old article URL aliases exist. Serving the `/jupyterblog/` aliases on GitHub still requires resolving the separate old project-site deployment.
- All files in the existing Doxygen and SpecImage directories are copied unchanged.
- A synthetic draft notebook is absent from public HTML, raw notebook downloads, search, and RSS. The synthetic source was removed after the check.
- Markdown, `.qmd`, and notebook starter creation was exercised in a temporary directory inside the project.
- The `.qmd` example executed successfully with a LaTeX equation, cross-referenced figure, and matching Matplotlib style.
- Its whole-project render then succeeded with an unavailable Python executable, using the frozen computation rather than rerunning the analysis.
- The GitHub workflow's YAML, master-only deployment condition, shell wrapper syntax, SVG syntax, and Git whitespace checks pass.

The original five drafts remain excluded from rendering. The third-party reference repository and old `jupyterblog` checkout are unchanged. Archived article text has not been scientifically re-reviewed; one malformed `random.org` link was repaired.
