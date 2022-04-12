# TML Blocks - ServiceNow Incident Management

Incident Management trends and KPI’s are now accessible via search and point-and-click interactive visualizations.
The ServiceNow Incident Management TML Blocks is built on top of a subset of the native ServiceNow data model. This means that in order to get up and running, you simply need to transfer your data, as-is, into a Cloud Data Warehouse. Once the data is stored in a CDW such as Snowflake, RedShift or GBQ, just use ThoughtSpot Embrace to connect to the data and import the ServiceNow Incident Management SpotApp.

# Artifacts 

- Input_Connection_YAML - stores the user’s connection YAML file
- Input_Table_TML - stores the user’s table TML files
- Output_SpotApps - contains the final zip file to be imported
- SpotApps_Scripts - contains the py script files used by SpotApp
- Spotapps_Original_TML - stores the template for SpotApp solution

# Implementation Steps

## Create the New CDW Connections 

1. Create new embrace connection 
2. Select ServiceNow tables on the cloud data warehouse 
3. Tables from the ServiceNow schema that are required for Spotapps

  **Required**:
  - task
  - incident
  - incident_task
  - problem
  - Problem_task

  **Optional**:
  - cmn_location
  - core_company
  - sys_user
  - sys_user_group

Note: These are the original table names from ServiceNow

## Export Connection YAML File and TML Files 

1. Select new Embrace Connection with ServiceNow tables 
2. Remap Connection 
3. Download YAML file 
4. Navigate to the Data Tab
5. Select the ServiceNow tables
6. Click on Export TML

## Run Script 

1. Unzip the spotapp zip file
2. Copy the connection yaml file into the folder titled “Input_Connection_YAML”
3. Copy the table TML files into the folder titled “Input_Table_TML”
4. Run the script through the terminal

For macOS, copy folder to ‘Documents’ folder
cd ~/Documents/Spotapps
python3 spotapps.py

## Column Description from the Mapping CSV

A - User friendly column names in the Spotapp worksheet. <br />
B, C, D, E - Original table and columns, join table and column names are listed from the original ServiceNow schema. <br />
F, G - Details about the joins in the Spotapp worksheet (join type and join required for spotapp to work). <br />
H, I - Shows the Table and Column names from the user’s CDW. <br />
J, K - Shows the tables and columns that are required for spotapp to work; these tables and columns should be present in the user’s CDW. <br />
L, M - the tables and columns that are missing in the user’s CDW are indicated by Y. If column value is Y, then it indicates that our script did not find the table/column in the user’s connection.  <br />
N, O - Mapping table and mapping column to be set by the user. When we find a missing column and indicate it in L, M by setting it to Y, we expect a value in these columns to point us to the corresponding columns in the user’s CDW.  <br />
Example: we did not find ‘task’ table in the user’s CDW connection, user has renamed table to ‘servicenow_task’; then we need the value in column N to be set to ‘servicenow_task’ wherever we see a Y for the task table (screenshot on the next slide). <br />

## Import TML Files

- Import the files containing TML for the worksheets and verify that it has all been imported without any errors.
- Import the files for the liveboards and verify that it has all been imported without any errors.

# Liveboard Screenshots 

### Significant Events Examination
![Screen Shot 2022-04-12 at 4 01 36 PM](https://user-images.githubusercontent.com/102629468/163068512-7c235b92-6d02-4225-bb7a-13b3898cf402.png)


### Incident Management Overview 
![Screen Shot 2022-04-12 at 4 01 50 PM](https://user-images.githubusercontent.com/102629468/163068514-eaf21866-6aa4-47fc-9f92-e985fd2a47a4.png)


### Incident Management Performance 
![Screen Shot 2022-04-12 at 4 02 14 PM](https://user-images.githubusercontent.com/102629468/163068550-fccd26c8-0a8f-45da-9a14-74214350eb60.png)




