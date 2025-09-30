---
layout: page
title: Deep Biosignal Representations
description: USC PhD Thesis Part I
img: assets/img/fm-figure.png
importance: 1
category: present
related_publications: avramidis2023scaling, kommineni2024knowledge, 
---

Foundation models are reshaping the landscape of artificial intelligence, but their potential for biosignals—continuous streams of physiological and behavioral data—remains largely untapped. Unlike text or images, biosignals carry both universal and highly personal information: sensor-specific quirks, individual traits, and subtle patterns that shift across contexts. The challenge is to extract generalizable representations without collapsing into overfitting to a particular person or device. This raises fundamental questions: How do we disentangle what belongs to the sensor, the subject, or the underlying phenomenon of interest? Which pre-training strategies amplify user-specific biases rather than capture shared structure?

Answering these questions requires rethinking both algorithms and evaluation. Self-supervised approaches like contrastive or masked modeling may inadvertently lock onto personalized artifacts, while the inherent noise and sparsity of biosignal recordings demand architectures designed with inductive biases—such as state-space models or quantization-based frameworks. Beyond model design, information-theoretic perspectives can help estimate the true capacity of a sensor stream, grounding representation learning in principled measures. By addressing these challenges, foundation models for biosignals could unlock a new paradigm of generalizable, cross-domain representations that bridge individual variability with population-level insight.

<br>