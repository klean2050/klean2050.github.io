---
layout: page
title: Music Semantics
description: Sponsored by USC, NTUA
img: assets/img/firstimg.png
importance: 5
category: past
related_publications: kratimenos2021augmentation, avramidis2021deep, avramidis2023role
---

### Visual Context in Music Semantics

Human perception and experience of music is highly context-dependent. Contextual variability contributes to differences in how we interpret and interact with music, challenging the design of robust models for information retrieval. Incorporating multimodal context from diverse sources provides a promising approach toward modeling this variability. Music presented in media such as movies and music videos provide rich multimodal context that modulates underlying human experiences. However, such context modeling is underexplored, as it requires large amounts of multimodal data along with relevant annotations. Self-supervised learning can help address these challenges by automatically extracting rich, high-level correspondences between different modalities, hence alleviating the need for fine-grained annotations at scale. In this study, we propose VCMR – Video-Conditioned Music Representations, a contrastive learning framework that learns music representations from audio and the accompanying music videos. The contextual visual information enhances representations of music audio, as evaluated on the downstream task of music tagging.

<br>

### Musical Instrument Classification

Augmentation Methods for Audio Mixtures: Most research in Instrument Classification deals with monophonic music, while efforts on polyphonic material mainly focus on predominant instrument recognition. Here we propose an approach for polyphonic music from predominantly monophonic data that involves performing data augmentation by mixing different audio segments. A variety of data augmentation techniques focusing on different sonic aspects, such as overlaying audio segments of the same genre, as well as pitch and tempo-based synchronization, are explored and we further investigate the usage of a combination of classifiers implementing the above methods.

Modeling Audio Waveforms: Audio Classification tasks are traditionally addressed through time-frequency representations of audio signals such as spectrograms. However, the emergence of deep neural networks as efficient feature extractors has enabled the direct use of audio signals for classification purposes. In this paper, we attempt to recognize musical instruments by only utilizing their raw waveforms. Various recurrent and convolutional architectures incorporating residual connections are examined and parameterized in order to build end-to-end classi-fiers with low computational cost and only minimal preprocessing. We obtain competitive classification scores and useful instrument-wise insight through the IRMAS Dataset, while maintaining a significantly reduced number of trainable parameters.

<br>