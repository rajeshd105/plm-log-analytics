import os
import logging

logger = logging.getLogger(__name__)

def process_apache_logs(log_path,node):
    """
    This function helps to process Windchill Apache logs
    
    Parameter:
    log_path str: Windchill Apache logs path
    node str: Windchill Cluster node
    Return: list
    processed log data for Analysis
    """
    logdata = []
    # files = os.listdir(log_path)
    try:
        # for f in files:
        #     fpath = log_path+"/"+f
            # print(fpath)
        logger.info(log_path + " file started for processing!..")
        with open(log_path, 'r') as f:
            for row in f.readlines():
                if 'wt.httpgw.HTTPServer' not in row:
                    cleanedLogvalue = row.strip().replace("[","").replace("]","").replace("\"","").split()
                    # cleanedLogvalue[3] = cleanedLogvalue[3].split(':')[0]  # Cleanup Date attribute, removed timestamp
                    cleanedLogvalue[3] = cleanedLogvalue[3].replace(':',' ',1)  # converted to DateTIME format
                    cleanedLogvalue.pop(4)  # Remove timezone value +0100
                    cleanedLogvalue.pop(6)  # Remove HTTP/1.1 
                    cleanedLogvalue[5] = cleanedLogvalue[5].replace("\'","\"") # Cleanup of ' due to database import failure
                    if cleanedLogvalue[2] == '-' and 'trustedAuth' in cleanedLogvalue[5]:
                        userid = cleanedLogvalue[5].rsplit("=",1)
                        cleanedLogvalue[2] = userid[1]
                    
                    templist = cleanedLogvalue[2:7] # Excluded IP and end portion values
                    if '/servlet' in cleanedLogvalue[5]:
                        technology = cleanedLogvalue[5].split('servlet/')[1].split("/")[0].split('?')[0]
                        if len(technology) > 50:
                            technology = technology[:50]
                        templist.append(technology)
                        if 'servlet/IE' in cleanedLogvalue[5] and '/tasks' in cleanedLogvalue[5]:
                            wccustomization = cleanedLogvalue[5].split('tasks')[1].split("?")[0]
                            endpoint = cleanedLogvalue[5].split('tasks')[1].split("?")[0].split('/')[-1]
                            wccustomization = wccustomization.replace(f'/{endpoint}',"")
                            templist.append(wccustomization)
                            templist.append(endpoint)
                        elif 'servlet/odata' in cleanedLogvalue[5]:
                            wccustomization = (cleanedLogvalue[5].split('odata')[1].split("?")[0])
                            endpoint = (cleanedLogvalue[5].split('odata')[1].split("?")[0].split('/')[-1])
                            wccustomization = wccustomization.replace(f'/{endpoint}',"")
                            templist.append(wccustomization.split("(")[0])
                            templist.append(endpoint.split("(")[0]) # Added split to avoid object specific info in endpoint
                        elif 'servlet/rest' in cleanedLogvalue[5]:
                            wccustomization = (cleanedLogvalue[5].split('rest')[1].split("?")[0])
                            endpoint = (cleanedLogvalue[5].split('rest')[1].split("?")[0].split('/')[-1])
                            wccustomization = wccustomization.replace(f'/{endpoint}',"")
                            templist.append(wccustomization)
                            templist.append(endpoint)
                        else:   # To manage database update empty values added
                            templist.append('')
                            templist.append('')
                    elif 'infoengine' in cleanedLogvalue[5] and '/jsp' in cleanedLogvalue[5]:
                        technology = 'infoengine'
                        templist.append(technology)
                        wccustomization = (cleanedLogvalue[5].split('/jsp')[1].split("?")[0])
                        endpoint = (cleanedLogvalue[5].split('/jsp')[1].split("?")[0].split('/')[-1])
                        wccustomization = wccustomization.replace(f'/{endpoint}',"")
                        templist.append(wccustomization)
                        templist.append(endpoint)
                    else:
                        templist.append('') # To manage datbase update empty values added
                        templist.append('')
                        templist.append('')
                    templist.append(node) # To record which cluster machine logs are captured
                    logdata.append(templist)
        # break
        return logdata
    except Exception:
        logger.error("Error Occurred while processing log files" + Exception)

    return None
