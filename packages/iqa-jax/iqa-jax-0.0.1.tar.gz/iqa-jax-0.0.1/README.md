# IQA-jax
Image Quality Assessment library for Jax.  
Implementations are Jax.numpy ported versions of the original Numpy-based [BasicSR](https://github.com/XPixelGroup/BasicSR).  

## NOTE
<b>Current implementations have not been tested. There is no guarantee that the outputs will be the same as BasicSR (MATLAB).</b>  
Functions marked as tested below ensure that the results match the original BasicSR's implementation.  
Check the test codes under ./tests.  

## Metrics
 - [X] PSNR
 - [X] SSIM
 - [ ] NIQE
 - [X] FID

## Tests
 - [X] PSNR
 - [X] SSIM
 - [ ] NIQE
 - [ ] FID
 - [ ] InceptionV3
 - [X] Preprocessing(RGB2Y Conversion)
