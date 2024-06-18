environment : python3.10

pyenv local 3.10.13
python3 -m venv .venv310
. .venv310/bin/activate

# 0 Build AdelaiDet
pip install torch==1.13.1+cu116 --extra-index-url https://download.pytorch.org/whl/cu116
pip install wheel build
python setup.py sdist bdist_wheel

# 1 install AdelaiDet
pip install AdelaiDet-0.2.0-cp310-cp310-linux_x86_64.whl

# 2 install detectron2 dependencies
pip install torch==1.13.1+cpu --extra-index-url https://download.pytorch.org/whl/cpu

# 3 build and install detectron2
python -m pip install 'git+https://github.com/facebookresearch/detectron2.git'

# 4 install demo dependencies
pip install torchvision==0.14.1+cpu torchaudio==0.13.1 --extra-index-url https://download.pytorch.org/whl/cpu
pip install opencv-python scipy timm shapely albumentations Polygon3 pyclipper

# 5 Download weights
https://onedrive.live.com/?id=6A68D74A1E9078D1%21200&resid=6A68D74A1E9078D1%21200&authkey=%21AI85tl5C9igCOds&cid=6a68d74a1e9078d1

# 6 run demo
python demo.py --config-file configs/SRFormer/TotalText/R_50_poly.yaml --input ~/Pictures/cam_screen.jpeg --output ./test.jpeg --confidence-threshold 0 --opts MODEL.WEIGHTS totaltext-srformer-3seg.pth


# in simone container gpu (torch 1.13.0)

## build and install AdelaiDet
git clone https://github.com/retsuh-bqw/SRFormer-Text-Det.git
cd SRFormer-Text-Det
apply patches on the code of ms_deform_attn_forward (cpu)
pip install wheel build
python setup.py sdist bdist_wheel
pip install ./dist/AdelaiDet-0.2.0-cp38-cp38-linux_x86_64.whl

## build and install detectron2
python -m pip install 'git+https://github.com/facebookresearch/detectron2.git'

## Install last missing dependency
pip install timm

## run demo (don't forget to download weights)
docker cp text_detection simone-inference:/veesion/
docker exec -it simone-inference bash
cd text_detection/
python demo.py --config-file configs/SRFormer/TotalText/R_50_poly.yaml --input cam_screen/cam_screen.jpeg --output ./test.jpeg --confidence-threshold 0 --opts MODEL.WEIGHTS totaltext-srformer-3seg.pth


# in simone container nuc (torch 1.8.1)

## build and install AdelaiDet
git clone https://github.com/retsuh-bqw/SRFormer-Text-Det.git
cd SRFormer-Text-Det
apply patches on the code of ms_deform_attn_forward (cpu)
pip install wheel build
python3 setup.py sdist bdist_wheel
pip install ./dist/AdelaiDet-0.2.0-cp38-cp38-linux_x86_64.whl


## build and install detectron2
python3 -m pip install 'git+https://github.com/facebookresearch/detectron2.git'

## Install last missing dependency
pip install timm

## run demo (don't forget to download weights)
docker cp veesion-polygon simone-inference:/veesion/
docker exec -it simone-inference bash
cd veesion-polygon/
python3 demo.py --config-file configs/SRFormer/TotalText/R_50_poly.yaml --input cam_screen/cam_screen.jpeg --output ./test.jpeg --confidence-threshold 0 --opts MODEL.WEIGHTS totaltext-srformer-3seg.pth
