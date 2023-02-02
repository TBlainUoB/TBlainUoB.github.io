---
permalink: /
title: "Tom Blain Data Science & ML Resume"
excerpt: "About me"
author_profile: true
redirect_from:
  - /about/
  - /about.html
---

This is a website where I post my current research interests and areas of study,
I'm currently a masters student in mathematics at the University of Bristol, with a strong focus on Machine learning and Data Science.

---

#Current projects I am working on:

Predicting IMDb movie ratings: Using a web crawler to gather a dataset of movie titles - selected movies produced in the UK and US between 2000-2022 for the data. Using https://omdbapi.com/ to gather features from the titles in my dataset.
Features include: Title, Genres, Plot, Year, Actors.
Set up a basic model to OHE actors with more than 5 appearances in the database, preprocessed Word2Vec embeddings of title and plot. Boosting algorithm for regression prediction.
Areas of difficulty - How can we best encode the actors - dimensionality reduction. How can we get the key data from the plot to predict the rating - Different NLP techniques and preprocessing.

Variational Inference Research Paper:
Studying VI - aim is an 80 page research paper by June. Currently written an introduction with key concepts of bayesian statistics, and now covering the KL divergence and ELBO.
