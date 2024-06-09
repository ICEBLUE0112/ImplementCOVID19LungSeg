# Official Page

[Script — CTLungSeg 2.0.0 documentation (covid-19-ggo-segmentation.readthedocs.io)](https://covid-19-ggo-segmentation.readthedocs.io/en/latest/script.html#)

# Lung Extraction

## Purpose

通过预训练的U-Net模型对肺部进行提取。

The model and the code used to apply it belong to [this](https://github.com/JoHof/lungmask) repository. For more details, please refers [here](https://eurradiolexp.springeropen.com/articles/10.1186/s41747-020-00173-2).

## Attention

1. 在输入脚本两个参数时,地址最后以`/`结尾,防止无法正确寻找到输入输出路径
2. `./Examples/LUNG/`地址下,`.nii.gz.nrrd`后缀文件为`lung_extraction.sh`脚本执行结果,`.nrrd`后缀文件为`lung_extraction.ps1`脚本执行结果

## lung_extraction.ps1

### 解读

这段代码是一个PowerShell脚本，用于批量处理肺部提取任务。让我逐行解释每一行的含义：

1. `#!/usr/bin/env pwsh`：这是一个shebang，指定了脚本使用的PowerShell解释器。

2. `[CmdletBinding()]`：这是一个CmdletBinding属性，表示脚本是一个Cmdlet，可以接受参数和支持其他高级特性。

3. `Param`：定义脚本的参数块。

4. `[parameter(mandatory=$true, position=0)][string]$input_dir`：定义一个名为`$input_dir`的必需字符串参数，表示输入目录的路径。

5. `[parameter(mandatory=$true, position=1)][string]$output_dir`：定义一个名为`$output_dir`的必需字符串参数，表示输出目录的路径。

6. `If ( $null -eq $input_dir )`：如果`$input_dir`为null，则执行以下操作。

7. `Write-Error -Message "Error! Input directory not set" -Category NotSpecified -RecommendedAction "Set path to input directory"`：打印错误消息，指示输入目录未设置，并提供建议的操作。

8. `ElseIf (-not (Test-Path -Path $input_dir -PathType Container))`：如果输入目录不存在，则执行以下操作。

9. `Write-Error -Message "Error! Input directory not found" -Category NotSpecified`：打印错误消息，指示输入目录未找到。

10. `If ( $null -eq $output_dir)`：如果`$output_dir`为null，则执行以下操作。

11. `Write-Error -Message "Error! Output directory not set" -Category NotSpecified-RecommendedAction "Set path to output directory"`：打印错误消息，指示输出目录未设置，并提供建议的操作。

12. `ElseIf ( -not (Test-Path -Path $output_dir -PathType Container) )`：如果输出目录不存在，则执行以下操作。

13. `Write-Error -Message "Error! Output directory not found" -Category NotSpecified`：打印错误消息，指示输出目录未找到。

14. `$files = get-ChildItem -Path $input_dir*`：获取输入目录下的所有文件，并将它们保存到`$files`变量中。

15. `Write-Output "Found "$files.Length" files to process"`：打印找到的文件数量。

16. `For ($i = 0; $i -lt $files.Length; $i++)`：循环处理每个文件。

17. `Write-Output  "* Processing " $files[$i]`：打印正在处理的文件名。

18. `$BaseName = Get-Item $files[$i] | Select-Object -ExpandProperty BaseName`：获取文件的基本名称（不带扩展名）。

19. `$BaseName = $BaseName -replace "\..+"`：使用正则表达式将基本名称中的扩展名部分移除。

20. `$lung_name = $output_dir + $BaseName + +".nrrd"`：构建输出文件的路径。

21. `python -m CTLungSeg.lung_extraction --input $files[$i] --output $lung_name`：调用Python命令行，执行CTLungSeg.lung_extraction模块进行肺部提取操作，并传递输入和输出文件路径作为参数。

22. `If ( $? )`：如果前一个命令执行成功，则执行以下操作。

23. `Write-Output  -InputObject "[done]"`：打印处理完成的消息。

24. `Write-Output -InputObject "[failed]"`：打印处理失败的消息。

25. `exit 1`：退出脚本并返回错误代码1。

这段代码的作用是批量处理肺部提取任务。它首先验证输入和输出目录是否设置和存在，然后遍历输入目录下的所有文件，对每个文件执行肺部提取操作，并将结果保存到输出目录中。如果某个文件处理失败，则会打印失败消息并退出脚本。

### Scripts

#### 目录及文件准备

```shell
# 创建一个名为"INPUT"的目录（文件夹），位于当前目录下的"Examples"目录中。-Path参数指定了目录的路径，-Name参数指定了目录的名称，-ItemType参数指定了创建的是一个目录。
New-Item -Path "Examples" -Name "INPUT" -ItemType "directory"

# 同上
New-Item -Path "Examples" -Name "LUNG" -ItemType "directory"

# 将位于"Examples\COVID-19-CT"目录下的"coronacases_002.nii.gz"文件移动到"Examples\INPUT"目录中。-Path参数指定了要移动的文件的路径，-Destination参数指定了目标路径。
Move-Item -Path "Examples\COVID-19-CT\coronacases_002.nii.gz" -Destination "Examples\INPUT"

#同上
Move-Item -Path "Examples\COVID-19-CT\coronacases_005.nii.gz" -Destination "Examples\INPUT"
```

#### 脚本执行

```shell
# 执行名为"lung_extraction.ps1"的PowerShell脚本，并传递两个参数：输入目录的路径和LUNG目录的路径。脚本的作用可能是对输入目录中的文件进行肺部提取操作，并将结果保存到LUNG目录中。
lung_extraction.ps1 .\Examples\INPUT\ .\Examples\LUNG\
```

> 以上语句在shell中执行有误,改为以下执行方式: 分别输入脚本名,再输入两个参数

```shell
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

Try the new cross-platform PowerShell https://aka.ms/pscore6

PS D:\PycharmProjects\A_Prerequisite4Entrance\ImplementCOVID19LungSeg> ./lung_extraction.ps1

cmdlet lung_extraction.ps1 at command pipeline position 1
Supply values for the following parameters:
input_dir: ./Examples/INPUT/
output_dir: ./Examples/LUNG/
Found 
2
 files to process
* Processing 


    Directory: D:\PycharmProjects\A_Prerequisite4Entrance\ImplementCOVID19LungSeg\Examples\INPUT


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----        2020-03-31     10:29       70065923 coronacases_002.nii.gz
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 10/10.0 [02:48<00:00, 16.89s/it]
lungmask 2024-05-23 19:56:20 Postprocessing
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 64.39it/s]
./Examples/LUNG/coronacases_002.nrrd
Process ended after 203.2576744556427 seconds
[done]
* Processing 
-a----        2020-03-31     10:11       96466369 coronacases_005.nii.gz                                                                                                                                                               
15it [03:48, 15.26s/it]                                                                                                                                                                                                                
lungmask 2024-05-23 20:01:33 Postprocessing
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 5/5 [00:00<00:00, 626.71it/s]
./Examples/LUNG/coronacases_005.nrrd
Process ended after 263.36569929122925 seconds
[done]
```

## lung_extraction.sh

### Scripts

#### 目录及文件准备

同上

#### 脚本执行

同上

## lung_extraction.py

为`lung_extraction.sh(.ps1)`所执行的目标代码

1. `#!/usr/bin/env python`: 这是一个 shebang 行,用于指定该脚本由 Python 解释器执行。
2. `# -*- coding: utf-8 -*-`: 这一行指定了源代码的字符编码为 UTF-8。
3. 导入所需的 Python 库:
   - `argparse`: 用于解析命令行参数
   - `numpy`: 用于数值计算
   - `SimpleITK`: 用于医学影像处理
   - `time`: 用于测量程序执行时间
   - `lungmask.mask`、`CTLungSeg.utils`、`CTLungSeg.method` 和 `CTLungSeg.segmentation`: 自定义模块
4. 定义作者信息。
5. `parse_args()` 函数解析命令行参数,接受两个参数:
   - `--input`: 输入文件名
   - `--output`: 输出文件名
6. `main(image)` 函数是主要处理逻辑:
   - 使用 `lungmask.mask.apply()` 函数获取肺部掩码
   - 将掩码二值化,去除左右肺的区分
   - 使用 `CTLungSeg.method.apply_mask()` 函数将掩码应用于原始图像
   - 使用 `CTLungSeg.segmentation.remove_vessel()` 函数移除血管
   - 使用 `CTLungSeg.utils.shift_and_threshold()` 函数对图像进行平移和阈值处理
7. `if __name__ == '__main__':` 块是程序的入口点:
   - 记录程序开始执行时间
   - 调用 `parse_args()` 函数获取命令行参数
   - 使用 `CTLungSeg.utils.read_image()` 函数读取输入文件
   - 调用 `main(image)` 函数对输入图像进行处理
   - 使用 `CTLungSeg.utils.write_image()` 函数将处理结果写入输出文件
   - 记录程序结束执行时间,并打印执行时长

总的来说,这段代码实现了一个肺部分割的功能,首先使用 `lungmask` 库获取肺部掩码,然后使用自定义的 `CTLungSeg` 模块对掩码进行处理,最终生成一个去除血管的肺部图像。整个过程由命令行参数控制输入和输出文件。

# Labeling

