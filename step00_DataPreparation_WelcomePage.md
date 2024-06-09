# Official Welcome Page

[Welcome to CTLungSeg’s documentation! — CTLungSeg 2.0.0 documentation (covid-19-ggo-segmentation.readthedocs.io)](https://covid-19-ggo-segmentation.readthedocs.io/en/latest/index.html)

# Dataset Preparation

```shell
# 创建一个名为"Examples"的目录。
New-Item  -Path . -Name "Examples" -ItemType "directory"

# 使用BitsTransfer模块从给定的URL下载文件，并将其保存到".\Examples"目录下。
Start-BitsTransfer -Source https://zenodo.org/record/3757476/files/COVID-19-CT-Seg_20cases.zip -Destination .\Examples\

# 使用Expand-Archive命令解压缩名为"COVID-19-CT-Seg_20cases.zip"的文件，并将解压后的内容保存到".\Examples\COVID-19-CT"目录中。
Expand-Archive -LiteralPath .\Examples\COVID-19-CT-Seg_20cases.zip -DestinationPath .\Examples\COVID-19-CT -Force
```

or download `COVID-19-CT-Seg_20cases.zip` manually from [COVID-19 CT Lung and Infection Segmentation Dataset (zenodo.org)](https://zenodo.org/records/3757476) and unzip to file `./Examples/COVID-19-CT`

