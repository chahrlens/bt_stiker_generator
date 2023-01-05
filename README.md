
# Bt Sicker Generator 
It is a simple python script compatible with neser Star Business database.  The objective is to generate a sticker for each item, a description of the document to which the price and quantity belongs is added to each item, at the end it generates a PDF document with all the tickets selected by document.

## Requeriments
Python 3.7

Pip3
## Python Libs Requeriments
mysql-connector-python

Blabel

Pandas
## Install Requeriments

Get  Pip
```bash
sudo apt-get install python3-pip
```
Install Script Libs Requeriments

[![Mysql-connector-python](https://pypi.org/)](https://pypi.org/project/mysql-connector-python/)

```bash
pip3 install mysql-connector-python
```
[![Blabel](https://pypi.org/)](https://pypi.org/project/blabel/)
```bash
pip3 install blabel
```
[![Pandas](https://pypi.org/)](https://pypi.org/project/Pandas3/)
```bash
pip3 install pandas
```

## Usage
In order to enjoy it,  make sure you have python 3.7+ installed,  you must also have python3-pip installed in order to install the script requirements. So far it has only been tested on Linux host, for Windows  user has not been tested yet only with Linux on WSL2. For the first time run the


```bash
python3 set_atados.py file
```


The first time it runs, I don't know what it does, but it has created a file with the name "config.con", this file saves parameters that will be used to connect to the database server
