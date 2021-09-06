#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 20:53:35 2021

@author: christianschoeberl
@file: etl_cschoebe.py
"""
import pandas as pd
import censusdata 
import psycopg2
from config import config
from io import StringIO


#declaring modular variables
src = "acs5"
year = 2019
#ID finding code - saving for future state code 
#state_search = 'Texas'
#states = censusdata.geographies(censusdata.censusgeo([('state','*')]), src, 
#                                                    year)
#print(states[state_search])
texas_id = '48'

#Variable list:
#<api.census.gov/data/2019/acs/acs5/variables.html>

#variable selection: comparing population sizes & median ages of 
#latino/hispanic and white communities as TX undergoes a demographic shift 

#B01003_001E = estimated total population 
#B01001H_001E = white alone, estimated total population
#B01001I_001E = hispanic/latino, estimated total population
#B01002H_001E = white alone, median age 
#B01002I_001E = hispanic/latino, median age 
variable_list = ['B01003_001E','B01001H_001E','B01001I_001E',
                            'B01002H_001E', 'B01002I_001E']

#extracting data from census package 
data = censusdata.download(src, year, 
                           censusdata.censusgeo([('state', texas_id),
                                                 ('county', '*'),
                                                 ('block group', '*')]),
                           variable_list)
data.columns = ['TOTAL_POP','WHITE_POP','HL_POP','WHITE_MA','HL_MA']

#connecting to database and creating new table 
#ADD .ini to GITIGNORE before SUBMITTING
params = config()
connection = psycopg2.connect(**params, options="-c search_path=acs")
cursor = connection.cursor()
cursor.execute("DROP TABLE IF EXISTS cschoebe_acs_data;")
#modular = change sql to adapt to new table 
#possibly make new method? 
sql = '''CREATE TABLE cschoebe_acs_data(
total_pop varchar(15), 
white_pop varchar(15),
hl_pop varchar(15), 
white_ma varchar(15),
hl_ma varchar(15))'''
cursor.execute(sql)

#writing to local .csv and uploading data
buffer = StringIO()
data.to_csv(buffer, header=False, index=False)
buffer.seek(0)
cursor.copy_from(buffer, 'cschoebe_acs_data', sep=",")
#committing changes
connection.commit()
#closing cursor
cursor.close()
