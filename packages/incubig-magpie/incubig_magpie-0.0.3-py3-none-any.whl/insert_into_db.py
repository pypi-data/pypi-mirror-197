import mysql.connector
from decouple import config

#connection variables
rds_host=config('rds_host')
rds_user=config('rds_user')
rds_password=config('rds_password')
rds_db_name=config('rds_db_name')

connection = mysql.connector.connect(host=rds_host,user=rds_user,password=rds_password,db=rds_db_name)
cursor = connection.cursor()

applications_file_path = "./patent_data/csvs/applications.csv"
inventors_file_path = "./patent_data/csvs/inventors.csv"
assignees_file_path = "./patent_data/csvs/assignees.csv"
classification_file_path = "./patent_data/csvs/classification.csv"

applications_col_name = "(application_number,application_date,publication_number,publication_date,publication_country,main_cpc,industry,sector,sub_sector,title,abstract)"
inventors_col_name = "(publication_number,publication_date,name,city,address_code,country)"
assignees_col_name = "(publication_number,publication_date,name,city,address_code,country)"
classification_col_name = "(publication_number, publication_date, cpc, industry, sector, sub_sector)"

def insert_into_tables():
    #Loading data into applications table
    query = f"LOAD DATA LOCAL INFILE '{applications_file_path}' INTO TABLE applications FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n' {applications_col_name};"
    cursor.execute(query)
    connection.commit()
    print("Inserted all recored in applications table")

    #Loading data into inventors table
    query = f"LOAD DATA LOCAL INFILE '{inventors_file_path}' INTO TABLE inventors FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n' {inventors_col_name};"
    cursor.execute(query)
    connection.commit()
    print("Inserted all recored in inventors table")

    #Loading data into assignees table
    query = f"LOAD DATA LOCAL INFILE '{assignees_file_path}' INTO TABLE assignees FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n' {assignees_col_name};"
    cursor.execute(query)
    connection.commit()
    print("Inserted all recored in assignees table")

    #Loading data into classification table
    query = f"LOAD DATA LOCAL INFILE '{classification_file_path}' INTO TABLE classification FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n' {classification_col_name};"
    cursor.execute(query)
    connection.commit()
    print("Inserted all recored in classification table")


