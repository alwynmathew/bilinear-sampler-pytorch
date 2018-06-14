# Bilinear sampler pytorch
Pytorch implementation of STN bilinear sampler 

Ported from [tensorflow implementation](https://github.com/mrharicot/monodepth/blob/master/bilinear_sampler.py)<sup id="a1">[1](#f1)</sup> of [STN](https://github.com/daviddao/spatial-transformer-tensorflow/blob/master/spatial_transformer.py)<sup id="a2">[2](#f2)</sup> can be found at [bilinear_pytorch.py](https://github.com/alwynmathew/bilinear-sampler-pytorch/blob/master/bilinear_pytorch.py).

1. <small id="f1"> [Unsupervised Monocular Depth Estimation with Left-Right Consistency](https://arxiv.org/pdf/1609.03677.pdf)   </small>

2. <small id="f2"> [Spatial Transformer Networks](https://arxiv.org/pdf/1506.02025.pdf)  </small>

##### Known issues

1. ```_wrap_mode == 'border'``` doesnt work.

### Alternative Pytorch build-in bilinear sammpler

Usage can be found at [bilinear.py](https://github.com/alwynmathew/bilinear-sampler-pytorch/blob/master/bilinear.py). Thanks to [@scholltan](https://github.com/scholltan) for the code.



