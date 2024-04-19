# TML Blocks - ServiceNow Incident Management

SpotApps are ThoughtSpot’s out-of-the-box solution templates built for specific use cases and data sources. They are built on ThoughtSpot Modeling Language (TML) Blocks, which are pre-built pieces of code that are easy to download and implement directly from the product.

The ServiceNow Incident Management SpotApp mimics the ServiceNow data model. When you deploy it, ThoughtSpot creates several Worksheets, Answers, and Liveboards, based on your ServiceNow data in your cloud data warehouse.

# Artifacts 
- [ServiceNow Incident Schema](https://github.com/thoughtspot/tmlblock-servicenow/blob/main/ServiceNow%20Incident%20Management_schema.csv) - The following table describes the schema for the ServiceNow Incident Management SpotApp.
- [ServiceNow Incident Managment TML](https://github.com/thoughtspot/tmlblock-servicenow/blob/main/ServiceNow%20Incident%20Management%20TML.zip) - stores the template for SpotApp solution

# Prerequisites
Before you can deploy the ServiceNow Incident Management SpotApp, you must complete the following prerequisites:

## Review and Sync Data

- **Developer Account in ServiceNow**: You must have a developer account in ServiceNow.
- **Review Required Data**: Review the required tables and columns for the SpotApp.
- **Ensure Column Compatibility**: Ensure that your columns match the required column type listed in the schema for your SpotApp.
- **Sync Data**: Sync all tables and columns from ServiceNow to your cloud data warehouse. While only specific tables and columns may be required, ThoughtSpot recommends syncing all tables and columns from ServiceNow to your CDW. The columns can be ServiceNow’s out-of-the-box columns, or any custom columns that you are using instead of the out-of-the-box columns.

## Credentials and Access

- **Obtain Credentials and SYSADMIN Privileges**: Obtain the necessary credentials and SYSADMIN privileges to connect to your cloud data warehouse. Ensure that the cloud data warehouse contains the data you would like ThoughtSpot to use to create Answers, Liveboards, and Worksheets.
- **Unique Connection Name**: Ensure that the connection name for each new SpotApp is unique.
- **Load Data**: Ensure that ServiceNow data is loaded into your cloud data warehouse.

# Implementation Steps

## Create the New CDW Connections 

1. Create new embrace connection 
2. Select ServiceNow tables on the cloud data warehouse 
3. Tables from the ServiceNow schema that are required for Spotapps

  **Required**:
- INCIDENT
- CMN_LOCATION
- SYS_USER
- SYS_USER_GROUP
- TASK_SLA
- CONTRACT_SLA
- SERVICE_OFFERING
- SERVICES
- CONFIG_ITEM
- CORE_COMPANY

Note: These are the original table names from ServiceNow

## Export Connection YAML File and TML Files 
After you complete the prerequisites, you are ready to deploy the ServiceNow Incident Management SpotApp and begin leveraging its pre-built content.

1. Download [TML file](https://github.com/thoughtspot/tmlblock-servicenow/blob/main/ServiceNow%20Incident%20Management%20TML.zip) 
2. Navigate to the Data Tab
3. Import the files containing TML for the worksheets and verify that it has all been imported without any errors.
4. Import the files for the liveboards and verify that it has all been imported without any errors.

# Liveboard Screenshots 

### Significant Events Examination
![Screen Shot 2022-04-12 at 4 01 36 PM](https://user-images.githubusercontent.com/102629468/163068512-7c235b92-6d02-4225-bb7a-13b3898cf402.png)


### Incident Management Overview 
![Screen Shot 2022-04-12 at 4 01 50 PM](https://user-images.githubusercontent.com/102629468/163068514-eaf21866-6aa4-47fc-9f92-e985fd2a47a4.png)


### Incident Management Performance 
![Screen Shot 2022-04-12 at 4 02 14 PM](https://user-images.githubusercontent.com/102629468/163068550-fccd26c8-0a8f-45da-9a14-74214350eb60.png)




