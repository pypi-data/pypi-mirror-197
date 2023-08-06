wget https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-x86_64.sh
sh Mambaforge-Linux-x86_64.sh -b -p $HOME/mambaforge
rm -f Mambaforge-Linux-x86_64.sh
./mambaforge/bin/mamba init
exec /bin/bash

mamba install -y gxx gcc cmake

git clone https://github.com/DaehwanKimLab/hisat2.git hisat-3n
cd hisat-3n
git checkout -b hisat-3n origin/hisat-3n
make