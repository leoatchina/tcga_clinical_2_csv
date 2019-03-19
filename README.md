# 合并tcga网站上下载的clinical xml文件到一个csv
从tcga网站上下载的xml文件，一个xml对应一个受试者，有着非常之多的「TAG」, 每个TAG代表一个临床指标，由于种种原因，有些xml文件中，会缺少在另外xml中有的指标。不同的癌种之间，还有着不同的特异指标。
一般情况下，进行TCGA数据挖掘时，就是针对一个类型的癌症进行分析， 因此只需要把相应的TAG提取出来后，再补上空白值，形成key值相同的dict，就能合并到一个文件中。
以及为思路，我写了这个脚本。

## 使用（不支持windows)
把下载的xml文件放到`clin`文件夹下（随便放，多深的子目录都能发现)，`python3 tcga_clinical_2_csv.py`，会在当前目录下生成`merge.csv`。
当然你可以指定文件夹和合并文件 ，  `python3 tcga_clinical_2_csv.py  BRCA BRCA.csv`

## 大体流程
1. 用`*unix`系统的`find`命令提取所有目标文件夹下的`xml`文件
2. 对每个`xml`
    - 获取xml root node
      - 如果node有子node，继续遍历子node
      - 返回当前node和子node合并的dict
3. 获得所有dict后，遍历dict得到全部key，并把dict的缺失key补成空白
4. 写入csv文件

其中有很多技巧请看源代码学习
