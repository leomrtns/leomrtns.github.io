---
layout: splash
permalink: /
header:
  overlay_color: "#5e616c"
  overlay_image: /assets/images/mm-home-page-feature.jpg
excerpt: "Computational Biologist"
intro: 
  - excerpt: "Below you will find links to other pages, with code, documentation, and technical notes for bioinformatics and computational evolutionary biology software."
feature_row:
  - image_path: /assets/images/logo_araiguma.png
    alt: "notebooks"
    title: "Notebooks"
    excerpt: "Project with technical notes on bioinformatics algorithms and implementations"
    url: "https://leomrtns.github.io/notebooks"
    btn_class: "btn--primary btn--small"
    btn_label: "Notebooks webpage"
  - image_path: /assets/images/mm-customizable-feature.png
    alt: "guenomu"
    title: "Guenomu"
    excerpt: "Species tree estimation from multi-gene family data"
    url: "https://bitbucket.org/leomrtns/guenomu/"
    btn_class: "btn--primary btn--small"
    btn_label: "source code on bitbucket"
  - image_path: /assets/images/mm-customizable-feature.png
    alt: "genefam_dist"
    title: "Genefam-dist"
    excerpt: "C library for distance calculation between gene families and species trees, \
              with a python module for creating a signature of a gene family tree."
    url: "https://github.com/leomrtns/genefam-dist"
    btn_class: "btn--primary btn--small"
    btn_label: "source code"
  - image_path: /assets/images/mm-customizable-feature.png
    alt: "specimage"
    title: "SpecImage"
    excerpt: "Python module to work with hyperspectral imaging data."
    url: "https://github.com/leomrtns/specimage"
    btn_class: "btn--primary btn--small"
    btn_label: "source code"
  - image_path: /assets/images/logo_biomcmc.png
    alt: "biomcmclib"
    title: "biomcmc-lib Software"
    excerpt: "C library with low level functions for phylogenetic analyses"
    url: "https://github.com/quadram-institute-bioscience/biomcmc-lib"
    btn_class: "btn--primary btn--small"
    btn_label: "source code on github"
  - image_path: /assets/images/logo_biomcmc.png
    alt: "biomcmc-libdocs"
    title: "biomcmc-lib documentation"
    excerpt: "Doxygen documentation for biomcmc-lib source code"
    url: "https://leomrtns.github.io/doxygen-biomcmclib"
    btn_class: "btn--primary btn--small"
    btn_label: "See documentation"
---
{% include feature_row id="intro" type="center" %}
<!--{% include feature_row id="feature_row" type="left" %} -->
{% include feature_row id="feature_row" %}
