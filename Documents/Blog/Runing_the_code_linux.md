Note: This blog is migrated from LEARN, the original text is written by Yuanhao on 11 Oct 22.

## 1.Miniconda/anaconda

Download miniconda installer for linux

```shell
curl -o ~/Download https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```

run the installer

```shell
sh ~/Downloads/Miniconda3-latest-Linux-x86_64.sh
```

Create a vitual environment named PSD(depends on you) with python 3.8

```shell
conda create -n PSD python=3.8
```

## 2.clone the repository

```shell
git clone https://git.ecdf.ed.ac.uk/psd2223/assessment_source.git ~/Desktop/assessment_source
```

## 3.Install requirements

```shell
cd ~/Desktop/assessment_source

conda activate PSD

pip install -r ./requirements.txt
```

## 4.Run the code

```shell
tar -xzf ./papers.tar.gz
mkdir Docs Ents JSON data
python prototype.py
```

