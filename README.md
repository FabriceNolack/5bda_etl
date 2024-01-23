# 1. Description
This is an home-made ETL wich specific purpose: explore the Belgium Pro League  football players (Male) price and wage.

The principal stages are:
- Extraction data from https://www.sofifa.com
- Transformation price and wage to number
- Load data into an SQL DataBase (MySQL).

We collect on the web site (sofifa) this information for ech players:
- abbreviate name
- full name
- age
- position on the staduim
- club name
- country
- start contract year
- end contract year
- price (value)
- wage

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
- Create an ``.env`` file from the provided template ``.env.template`` with suitable insight
- After doing this you can launch the ETL using the command   
  ``python -m luigi --module pipeline_extract Extract --local-scheduler``
  this command launch the extraction and save the result into data/raw.csv
- To launch the other stages of the ETL use the same command
  ``python -m luigi --module <python_file> <python_class_extended_luigi_Task> --local-scheduler``

To Know more about Luigi you can follow this link https://luigi.readthedocs.io/en/stable/

Thanks.