import os
import sys
import requests
import dredger
import logging
import time
from datetime import date, timedelta
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Following is for logging
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler('logs.log',mode="a")
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)


logger.addHandler(file_handler)
logger.addHandler(stdout_handler)

def ordinal(i):
    if i == 1:
        return "st"
    elif i == 2:
        return "nd"
    elif i == 3:
        return "rd"
    else:
        return "th"

def download_pdf_file(url,primary_payload,secondary_payload,download_path,filename):
    headers = {"User-Agent":"PostmanRuntime/7.30.0","Accept":"*/*","Connection":"keep-alive"}
    resp = requests.post(url,headers=headers,data=primary_payload,verify=False)
    status_code = resp.status_code
    logger.info(f"Status code: {status_code} for payload:{primary_payload}")
    
    if status_code==200:
        with open(download_path+"/"+filename,mode="wb+") as f:
            f.write(resp.content)
        return status_code
    else:
        resp_with_secondary = requests.post(url,headers=headers,data=secondary_payload,verify=False)
        logger.info(f"Status code: {resp_with_secondary.status_code} for payload:{secondary_payload}")
        # logger.info(f"Status code: {resp.status_code} for payload:"+"{'Filename': 'ipo-docs\\IPIndia_Docs\\PAT\\2022\\09_2022\\Part-1.pdf'")
        if resp_with_secondary.status_code==200:
            with open(download_path+"/"+filename,mode="wb+") as f:
                f.write(resp_with_secondary.content)
            return resp_with_secondary.status_code
        else:
            tertiary_payload = {"FileName":secondary_payload["FileName"].replace("part.pdf","docx.pdf")}
            time.sleep(1)
            resp_with_tertiary = requests.post(url,headers=headers,data=tertiary_payload,verify=False)
            logger.info(f"Status code: {resp_with_tertiary.status_code} for payload:{tertiary_payload}")
            if resp_with_tertiary.status_code==200:
                with open(download_path+"/"+filename,mode="wb+") as f:
                    f.write(resp_with_tertiary.content)
                return resp_with_tertiary.status_code
            else:
                quaternary_payload = {"FileName":secondary_payload["FileName"].replace("part.pdf","part_compressed.pdf")}
                time.sleep(1)
                resp_with_quaternary = requests.post(url,headers=headers,data=quaternary_payload,verify=False)
                logger.info(f"Status code: {resp_with_quaternary.status_code} for payload:{quaternary_payload}")
                
                if resp_with_quaternary.status_code==200:
                    with open(download_path+"/"+filename,mode="wb+") as f:
                        f.write(resp_with_quaternary.content)
                        return resp_with_quaternary.status_code
                else:
                    quinary_payload = {"FileName":secondary_payload["FileName"].replace("part.pdf","part final.pdf")}
                    time.sleep(1)
                    resp_with_quinary = requests.post(url,headers=headers,data=quinary_payload,verify=False)
                    # logger.info("ipo-docs\\IPIndia_Docs\\PAT\\2023\\09_2023\\Official Journal (09-2023) 03.03.2023  1st part final.pdf")
                    logger.info(f"Status code: {resp_with_quinary.status_code} for payload:{quinary_payload}")
                    
                    if resp_with_quinary.status_code == 200:
                        with open(download_path+"/"+filename,mode="wb+") as f:
                            f.write(resp_with_quinary.content)
                            return resp_with_quinary.status_code
                    else:
                        logger.warning(f"Status code: {resp_with_quinary.status_code} for filename:{filename}")
                

def bulk_downloader(year):
    ipindia_api = "https://search.ipindia.gov.in/IPOJournal/Journal/ViewJournal"

    # if len(year)==1:
        #IpIndia has changed the storage folders on following dates
        # -- 20th Aug 2021 (IPIndia_Docs\PAT\Part-"+str(i)+".pdf)|(IPIndia_Docs\PAT\Official Journal ({str(current_week)}-{str(year)}) {start_date.strftime('%d.%m.%Y')} {i}{ordinal(i)} part.pdf")
        # -- 2nd Jan 2015(IPIndia_Docs\IPOJournal\1_{m}_1\official-journal-{publication_date}-part{n}) - m starts from 5003/24 and increases by 2 every week
        # -- 3rd Jan 2014 (same as above) - m starts from 118 and increase by 1
        #since 1st Jan 2005 (ipo-docs\IPIndia_Docs/ipr/patent/journal_archieve/journal_{yyyy}/pat_arch_{mmyyyy}/official_journal_{publication_date}_part_{n}.pdf)
        # pass
    start_date = dredger.date_on_day(date(year,12,31),4)
    
    while year > 2005:
        download_location = "./patent_data/pdfs/"+str(year)
        if (os.path.exists(download_location)):
            pass
        else:
            os.mkdir(download_location)

        #At maximum there can be maximum 53 weekdays in a year
        today = date.today()
        if (year==today.year):
            current_week = dredger.weekday_count(today,4)
            start_date = dredger.date_on_day(today,4)
            sequence = 5003
        elif (year==2022):
            start_date = date(2022,3,4)
            current_week = dredger.weekday_count(start_date,4)
        elif (year==2021):
            start_date = date(2021,8,13)
            current_week = dredger.weekday_count(start_date,4)
        else:
            current_week = 53
            sequence = 5003
        
        while current_week>0:
            #Storage location depends on the date of publication
            if start_date>date(2021,8,13):
                base_location = "ipo-docs\\IPIndia_Docs\\PAT\\"+str(year)+"\\"+"{:02d}".format(current_week)+"_"+str(year)+"\\"
            elif start_date<=date(2021,8,13) and start_date>date(2015,1,1):
                sequence -= 1
                base_location =  f"ipo-docs\\IPIndia_Docs\\IPOJournal\\1_"+str(sequence)+"_1\\"
            elif start_date<=date(2015,8,13):
                base_location = f"ipo-docs\\IPIndia_Docs\\IPOJournal\\"
            for i in range(1,10):
                #Following two file locations are possible
                primary_file_location = base_location+"Part-"+str(i)+".pdf"
                secondary_file_location = base_location + f"Official Journal ({current_week:02d}-{str(year)}) {start_date.strftime('%d.%m.%Y')} {i}{ordinal(i)} part.pdf"

                primary_payload = {'FileName':primary_file_location}
                secondary_payload = {'FileName':secondary_file_location}
                output_filename = start_date.strftime("%Y%m%d")+"-"+str(i)+".pdf"
                
                logger.info(f"Attempting to download {current_week}/{year} part-{i} in: {download_location}-{i} | output filename is :{output_filename}")
                
                download_status = download_pdf_file(ipindia_api,primary_payload,secondary_payload,download_location,output_filename)

                if download_status != 200:
                    current_week -= 1
                    break
            if current_week<52:
                start_date = start_date-timedelta(days=7)

        year -= 1

bulk_downloader(2023)
