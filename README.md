## Introduction

This is the implementation of Captioning-ImageNet project. The goal of this project is to caption images within ImageNet dataset in a semi-autonomous way.
Specifically, we use a pre-trained butd model and implement constrained beam search algorithm to actually generate the caption. The detail of the methodology
of this project can be refered to the project report and will be omitted here. Instead, we focus on the introduction of how this work is implemented. 
Particularly, we will mention following topics:
1. Code structure
2. Implementation detail
3. Usage

## Code Structure
The code is consist of following classes:
1. dataset.imagenet_dataset.ImageNetDataset: This class loads a synset from ImageNet and constructs transition tables for the state machine which
is associate with this synset.
2. modules.constrained_beam_search.ConstrainedBeamSearch: This class implement the constrained beam search algorithm based on the transition tables constructed by ImageNetDataset class.
3. modules.captioner.PythiaCaptioner: This is the decoder  part of BUTD model which built upon the Pythia framework.
4. modules.rcnn_encoder.VQAMaskRCNNBenchmark: This is the encoder part of BUTD model which also built upon Pythia.
5. model.butd.PythiaBUTD: This class connects the encoder and decoder and construct the complete BUTD model.
## Implementation Detail

## Usage