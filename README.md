Create an environment

```bash
conda create -n wineq python=3.7 -y
```
Activate environment

```bash
conda activate wineq
```
Create requirements.txt file

Install necessary libraries

```bash
pip install -r requirements.txt
```

Download the data from

https://drive.google.com/drive/folders/18zqQiCJVgF7uzXgfbIJ-04zgz1ItNfF5?usp=sharing

git init

dvc init 
(Please note the dvc init command can give an error "cannot import name 'fsspec_loop' from 'fsspec.asyn' " probably because of using an older dvc version 2.10.2. To overcome this error downgrade fsspec version by running commands below:
pip uninstall fsspec
pip install fsspec==2022.7.1
and try running dvc init again, it should work now)

dvc add data_source/winequality.csv

git add .

git commit -m "first commit"
