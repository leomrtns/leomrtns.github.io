---
layout: splash
permalink: /
header:
  overlay_color: "#5e616c"
  overlay_image: /assets/images/mm-home-page-feature.jpg
excerpt: "Computational Biologist"
intro: 
  - excerpt: |
  This page contains links to other pages, with code, documentation, and technical notes for bioinformatics and computational evolutionary biology software. 
  <br> 
  I also write here eventual posts that don't fit into the links belows
feature_row:
  - image_path: /assets/images/logo_araiguma.png
    alt: "notebooks"
    title: "Notebooks"
    excerpt: "Technical notes on bioinformatics algorithms and implementations"
    url: "https://leomrtns.github.io/notebooks"
    btn_class: "btn--primary"
    btn_label: "Notebooks webpage"
  - image_path: /assets/images/mm-customizable-feature.png
    alt: "guenomu"
    title: "Guenomu"
    excerpt: "Species tree estimation from multi-gene family data"
    url: "https://bitbucket.org/leomrtns/guenomu/"
    btn_class: "btn--primary"
    btn_label: "source code on bitbucket"
  - image_path: /assets/images/logo_biomcmc.png
    alt: "biomcmclib"
    title: "biomcmc-lib Software"
    excerpt: "C library with low level functions for phylogenetic analyses"
    url: "https://github.com/quadram-institute-bioscience/biomcmc-lib"
    btn_class: "btn--primary"
    btn_label: "source code on github"
  - image_path: /assets/images/logo_biomcmc.png
    alt: "biomcmc-libdocs"
    title: "biomcmc-lib documentation"
    excerpt: "Doxygen documentation for biomcmc-lib source code"
    url: "https://leomrtns.github.io/doxygen-biomcmclib"
    btn_class: "btn--primary"
    btn_label: "See documentation"
---
{% include feature_row id="intro" type="center" %}
{% include feature_row id="feature_row" type="left" %}
