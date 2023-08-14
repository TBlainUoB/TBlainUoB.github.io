---
title: "Study Of OOB Error in Random Forests (pdf)"
excerpt: "Second part to my DataScience portfolio on bootstrapping. This time investigating how bootstrapping is used in Random forests. Consequentially, we have out of bag samples which can be used as an alternative to cross validation methods. I wanted to investigate the error using OOB over CV for different values of 'max_features' in the random forest."
collection: portfolio
permalink: /portfolio/OOBErrorInRF
---
[Link to pdf paper](http://TBlainUoB.github.io/files/OOBErrorInRF.pdf)

Abstract:
In this paper we will introduce decision trees and random forests, with the goal of exploring how we can use out-of-bag (OOB) samples as a computationally efficient alternative to cross validation (CV) methods. We experiment by generating a standard classification dataset, and building a random forest classifier with varying values of max_features (mtry). We conclude that out-of-bag error may not be a good choice for tuning the mtry parameter since OOB error seems to become more biased than CV when the parameter is small, but more investigation will have do be done with different varying datasets.
