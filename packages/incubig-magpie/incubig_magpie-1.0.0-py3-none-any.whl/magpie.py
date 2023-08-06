import time
import dredger
import xmltodict
import traceback
from azure.storage.blob import BlobClient

def extract_file():
    pass

def deconcate(file,separator=b'<?xml version="1.0" encoding="UTF-8"?>\r\n'):
    #Variables to store patents
    output = []
    count = 0
    content = ''

    start_time =time.time()

    for line in file.readlines():
        if line == separator:
            count += 1 
            if count > 1:
                output.append(content)
            content = separator.decode('utf-8')
        else:
            content += line.decode('utf-8')

    end_time = time.time()

    print(f"Extracted {count} individual patents from file in {end_time-start_time} seconds")

    return output

def upload(endpoint,container_name,file_type,input_date):
    if file_type == "uspto_applications":
        dredger.get_uspto_file(file_type,input_date)
        blobclient = BlobClient.from_connection_string(endpoint, container=container_name, blob="my_blob")

def upload_to_azure(endpoint,container_name,file_name):
    pass

def upload_to_aws():
    pass

def extract_grant_info(patent):
    obj = xmltodict.parse(patent)
    
    try:
        #Checking if obj['us-patent-application'] tag exits in xml
        obj['us-patent-grant']
        go_ahead_flag = True
    except:
        go_ahead_flag = False
    finally:
        if go_ahead_flag:
            try:
                #Extracting publication data
                kind = obj['us-patent-grant']['us-bibliographic-data-grant']['publication-reference']['document-id']['kind']
                patent_number = obj['us-patent-grant']['us-bibliographic-data-grant']['publication-reference']['document-id']['country']+obj['us-patent-grant']['us-bibliographic-data-grant']['publication-reference']['document-id']['doc-number']+kind
                grant_date = obj['us-patent-grant']['us-bibliographic-data-grant']['publication-reference']['document-id']['date']
                grant_term = 0
                
                #Extracting Application Data
                application_number = obj['us-patent-grant']['us-bibliographic-data-grant']['application-reference']['document-id']['doc-number']
                  
                patent_json = {"application-number":application_number,"patent_number": patent_number,"kind":kind, "grant_date":grant_date, "grant_term":grant_term}
                patent_sql = f"UPDATE applications SET patent_number = '{patent_number}' , kind = '{kind}' , grant_date = '{grant_date}' , grant_term = '{grant_term}' , status = 'Active' WHERE application_number = '{application_number}' AND status = 'Pending'; \n"
                
                return patent_sql
            except:
                print("Encountered error in " +str(patent_number))
                print(traceback.format_exc()+ "\n")