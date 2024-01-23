# 1. Description
This is an home-made ETL wich explore data for football player of the Belgium Pro League.

The principal stages are:
- Extraction of data on https://www.sofifa.com
- Transformation of price and wage to number
- Load it in an SQL DB (MySQL).

# 2. Our Environement
For this purpose we used tools listed belows on ***windows 11***
 - Python 3.12.1
 - WampServer 3.3.0
   - MySQL 8.0.31
   - Apache 2.4.54.2

# 3. How to install 
To use, test or deploy our home-made (Specific) ETL, you must ensure to have the same environement as our listed below.
And follow the following steps :
- Create a python virtual env  
  ``pip venv -m <venv_name>``
- Install library freeze into requirements.txt  
  ``pip install -m requirements.txt``
- After doign this you can launcg the ETL using the command   
  ``python -m luigi --module pipeline_extract Extract --local-scheduler``

Thanks.