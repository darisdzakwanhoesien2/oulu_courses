# Introduction to Social Network Analysis

## Overview
This folder contains exercises, notebooks, datasets, and projects related to social network analysis. The materials cover network construction, centrality measures, community detection, link prediction, and graph embeddings.

## Contents

- **data_code.ipynb**: 
  - Search and collect research papers from arXiv on specific topics.
  - Construct topic networks and author affiliation networks.
  - Compute graph statistics and detect communities using Girvan-Newman algorithm.
  - Generate Node2Vec embeddings and perform link prediction using machine learning classifiers.

- **exercise_1_daris_dzakwan_hoesien/**:
  - Random graph generation and visualization.
  - Centrality measures computation and visualization.
  - Analysis of the Karate Club dataset including graph construction, centrality, components, and diameter.

- **exercise_2/**:
  - Graph analysis on real-world datasets including Facebook combined network.
  - Calculation and visualization of various centrality measures.
  - Identification of key nodes and subgraphs.
  - Clustering coefficient analysis and power-law distribution fitting.

- **exercise_3/**:
  - Community detection on the Karate Club graph using multiple algorithms:
    - Girvan-Newman
    - Ratio Cut (Kernighan-Lin Bisection)
    - Louvain
    - Label Propagation
  - Evaluation of community quality and modularity.
  - Execution time measurement.
  - Graph expansion with additional nodes and repeated community detection.
  - Analysis of overlapping community membership and closeness centrality.

- **final_project/** and **past_project/**:
  - Project folders containing larger scale social network analysis projects (details not included here).

- Various data files including CSVs, Excel files, and BibTeX references for research papers.

## Topics Covered
- Network construction and visualization.
- Centrality measures: degree, closeness, betweenness, eigenvector, PageRank.
- Community detection algorithms and evaluation.
- Graph statistics: diameter, clustering coefficients, connected components.
- Graph embeddings with Node2Vec.
- Link prediction using machine learning.
- Real-world social network datasets analysis.

## Usage
- Requires Python 3.x with packages: networkx, matplotlib, numpy, pandas, sklearn, node2vec, powerlaw, seaborn.
- Run Jupyter notebooks to explore exercises and visualize results.
- Use provided datasets and scripts for hands-on social network analysis.


This README provides a guide to the social network analysis exercises, projects, and resources contained in this folder.

## data_code.ipynb

This notebook performs comprehensive social network analysis using research papers data collected from arXiv. The main steps include:

- **ArXiv Search:** Searching arXiv for research papers on specified topics and collecting metadata such as title, date, article ID, URL, main and all topics, and authors.
- **Topic Network Construction:** Building a topic similarity network based on shared topics between articles, computing adjacency matrices, and saving results.
- **Graph Statistics:** Computing graph characteristics like number of nodes, edges, diameter, average path length, clustering coefficient, and connected components.
- **Community Detection:** Applying the Girvan-Newman algorithm to detect communities in the topic network.
- **Author Affiliation Network:** Extracting author affiliations and building an organization collaboration graph with adjacency matrices.
- **Node2Vec Embeddings:** Generating node embeddings for the topic network using Node2Vec.
- **Link Prediction:** Predicting potential links in the network using machine learning classifiers such as Gradient Boosting Classifier.
- **Evaluation:** Assessing model performance with accuracy, Matthews correlation coefficient, confusion matrix, and classification reports.

This notebook demonstrates advanced techniques in social network analysis, graph embeddings, and link prediction using Python libraries such as NetworkX, Node2Vec, and scikit-learn.
