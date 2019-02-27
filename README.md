# market-basket-analysis

Finds Frequent Item Sets(of 3 or more items) with a given support from a list of transactions. 

Itemset is a set of one or more items from the transactions. Frequent Itemset is an Itemset that has co-occuring frequency that is greater than or equal to support. Support is a fraction equal to frequency of itemset in the data to total number of transactions. 

Refer [here](https://towardsdatascience.com/association-rules-2-aa9a77241654) for a  simple intuitive explanation and [here](http://infolab.stanford.edu/~ullman/mmds/ch6.pdf) for a comprehensive guide.

*Example:*

Input is a data file with list of transactions, each transaction is represented in a line in the data file. 

example_data.csv

> Item1 Item5 Item9 Item10

> Item2 Item5 Item9 Item11

> Item2 Item5 Item9 Item10

> Item2 Item15 Item19 Item10 

> Item21 Item25 Item29 Item10 

> Item2 Item5 Item9 Item10

Output(with support = 2/6(freq of itemset/total no.of transactions)):

> <item set size (3) >, <co-occuring freq = 2>, <Item 5>, <Item 9>, <Item 10>
  
> <item set size (3) >, <co-occuring freq = 3>, <Item 2>, <Item 5>, <Item 9>
  
> <item set size (4) >, <co-occuring freq = 2>, <Item 2>, <Item 5>, <Item 9> <Item 10>
  


## Method 1 (son_apriori.py):

Uses concepts from [SON algorithm and Apriori algorithm](https://github.com/fars-data-analysis/FIS/blob/master/project_report/report.pdf).

Uses Python 3 and [efficient-apriori package](https://pypi.org/project/efficient-apriori/0.4.5/).

Requirements: 
- Python 3.x
- efficient-apriori 

Installation:
- If required, install python from [Anaconda](https://www.anaconda.com/distribution/).
- git clone https://github.com/DeepthiMo/market-basket-analysis
- pip install requirements.txt

Usage: (from terminal)
> python3 son_apriori.py

(stores the results to a file named output.txt located in the same folder the script was run from.)

Configuration: 
- To modify the input file path or the required minimum support parameters, open the file son_apriori.py and edit the variables DATA_FILE and MIN_SUPPORT.


Method 1 does not scale for low values of support(< 0.01). Also Method 1 will not scale for large datasets[(ref)](https://arxiv.org/pdf/1701.09042.pdf). Method 2 is better equipped to handle both these cases.


## Method 2(fpgrowth.ipynb):

Uses [fpgrowth algorithm](https://github.com/fars-data-analysis/FIS/blob/master/project_report/report.pdf)

Uses pySpark & MLLib

Installation & Usage - Option 1:

[Download Docker](https://www.docker.com/get-started) in your cloud machine. 

git clone https://github.com/DeepthiMo/market-basket-analysis

Create a docker container using docker image (all-spark-notebook)[https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-all-spark-notebook] from docker hub and mount your machine’s directory where code is placed to docker container:

docker run -p 8889:8889 --name freqItemSets -v ~/your_directory_path:/home/jovyan jupyter/all-spark-notebook:137a295ff71b 

For additional details, please see here for an excellent guide on [docker](https://www.dataquest.io/blog/docker-data-science/)

Installation & Usage - Option 2:

Set up a free account with [Databricks Community Edition](https://databricks.com/try-databricks?utm_source=databricks&utm_medium=homev2tiletest)

[Import](https://docs.databricks.com/user-guide/notebooks/notebook-manage.html#import-a-notebook)  fpgrowth notebook from [here](https://databricks-prod-cloudfront.cloud.databricks.com/public/4027ec902e239c93eaaa8714f173bcfc/889751718678323/2378717504364781/5287256604884445/latest.html).

Create a [cluster](https://docs.databricks.com/user-guide/clusters/create.html#cluster-create) in databricks. Go to fpgrowth notebook and attach to the cluster. 

[Upload](https://docs.databricks.com/user-guide/importing-data.html#import-data) your dataset to datbricks file system and update location of the file in the fpgrowth notebook.

#Connect to your data store and data file as needed
data = sc.textFile("/FileStore/tables/retail_25k.txt")
