# data_collection_and_etl - Christian Schoeberl (cschoebe) 
Scripts for data download, cleanup, and upload to remote database

## Data Chosen
For this assignment, I chose to select data from the state of Texas since that is my homestate and I have not looked at the 2019 ACS data at the block group level since it was released. Given my personal experience growing up in the state and recent academic literature, I chose to select variables from the ACS dataset pertaining to White and Hispanic/Latino demographic activity. The selected data from 2019 serve as a foundation for investigating the changes both within and between the selected ethnic groups across years and geographic location. Any researchers, residents, policymakers, etc. would find this data to be a useful metric for recent population changes. 

## Transformation & Structure 
In order to cut down time on transformation & cleanup, I specifically targeted variables that were collected at the block-group level. The entire ACS dataset contains thousands of variables covering many aspects of life. By researching the documents provided by the ACS collectors, I was able to narrow my selection criteria to variables I knew would be present for the desired level of granularity. The column names were changed from their coded values to more readable formats for ease of access and understanding. 

## Selected variables: <ACS coding> = <short description> = <SQL column name> 
B01003_001E = estimated total population = total_pop
B01001H_001E = white alone, estimated total population = white_pop
B01001I_001E = hispanic/latino, estimated total population = hl_pop
B01002H_001E = white alone, median age = white_ma
B01002I_001E = hispanic/latino, median age = hl_ma

## Loading
Loading was by far the most complicated aspect of this project. Many tools exist to move data from a pandas dataframe to an SQL server, but I wanted to ensure this code remained secure and modular. In order to accomplish this goal, I chose to use psycogp2's postgres library wtih separate configuration files. This allows me to keep the details of the destination database private on git and another other platforms while still being able to code efficiently. I chose to write my dataframe to a local .csv file to be processed by psycogp2. The major limitation of my code is the resource and time requirements of larger datasets, which will be limited by local machine specs. 
