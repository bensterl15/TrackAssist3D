conda create -n C_Elegan_boot python==3.9.7
source activate C_Elegan_boot
python -m pip install 3DUnet/funlib.learn.torch
python -m pip install torch==1.10.0+cu113 -f https://download.pytorch.org/whl/torch_stable.html
python -m pip install torchvision==0.11.1+cu113 -f https://download.pytorch.org/whl/torchvision/
