---
layout: splash
permalink: /
header:
  overlay_color: "#5e616c"
  overlay_image: /assets/images/mm-home-page-feature.jpg
excerpt: "Computational Biologist"
intro: 
  - excerpt: "Below you will find links to other pages with code, documentation, and technical notes for bioinformatics and computational evolutionary biology software."
featr_code:
  - image_path: /assets/images/logo_guenomu.png
    alt: "guenomu"
    title: "Guenomu"
    excerpt: "Hierarchical Bayesian species tree estimation from multi-gene family data"
    url: "https://bitbucket.org/leomrtns/guenomu/"
    btn_class: "btn--primary btn--small"
    btn_label: "source code on bitbucket"
  - image_path: /assets/images/logo_genefam.png
    alt: "genefam_dist"
    title: "Genefam-dist"
    excerpt: "Signature inference of gene family trees from anchoring species trees."
    url: "https://github.com/leomrtns/genefam-dist"
    btn_class: "btn--primary btn--small"
    btn_label: "source code on github"
  - image_path: /assets/images/logo_specimage.png
    alt: "specimage"
    title: "SpecImage"
    excerpt: "Python module to work with hyperspectral imaging data."
    url: "https://github.com/leomrtns/specimage"
    btn_class: "btn--primary btn--small"
    btn_label: "source code on github"
  - image_path: /assets/images/logo_biomcmc.png
    alt: "biomcmclib"
    title: "biomcmc-lib library"
    excerpt: "C library with low level functions for phylogenetic analyses"
    url: "https://github.com/quadram-institute-bioscience/biomcmc-lib"
    btn_class: "btn--primary btn--small"
    btn_label: "source code on github"
  - image_path: /assets/images/logo_superdistance.png
    alt: "super_distance"
    title: "Super Distance"
    excerpt: "Supertree estimation from gene family trees, using matrix representation with distances"
    url: "https://github.com/quadram-institute-bioscience/super_distance"
    btn_class: "btn--primary btn--small"
    btn_label: "source code on github"
  - image_path: /assets/images/logo_biomc2.png
    alt: "recomb-biomc2"
    title: "recomb-biomc2"
    excerpt: "Hiearchical Bayesian Model for Viral Phylogenetic Recombination"
    url: "https://github.com/leomrtns/recomb-biomc2"
    btn_class: "btn--primary btn--small"
    btn_label: "source code on github"
featr_texts:
  - image_path: /assets/images/logo_araiguma.png
    alt: "notebooks"
    title: "Notebooks"
    excerpt: "Project with technical notes on bioinformatics algorithms and implementations"
    url: "https://leomrtns.github.io/notebooks"
    btn_class: "btn--info btn--small"
    btn_label: "Notebooks webpage"
  - image_path: /assets/images/logo_biomcmc.png
    alt: "biomcmc-libdocs"
    title: "biomcmc-lib API"
    excerpt: "Doxygen documentation for employing biomcmc-lib source code"
    url: "https://leomrtns.github.io/doxygen-biomcmclib"
    btn_class: "btn--info btn--small"
    btn_label: "API documentation page"
  - image_path: /assets/images/logo_biomcmc_blog.png
    alt: "biomcmc-blog"
    title: "bioMCMC blog"
    excerpt: "Old blog for phylogenetics discussions"
    url: "http://biomcmc.blogspot.com"
    btn_class: "btn--info btn--small"
    btn_label: "read blog posts"
---
<!--{% include feature_row id="feature_row" type="left" %} -->
{% include feature_row id="intro" type="center" %}
{% include feature_row id="featr_code" %}
{% include feature_row id="featr_texts" %} 
