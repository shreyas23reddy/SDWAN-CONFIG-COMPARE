import requests
import json


class Operation():
    def get_method(url, header):
        
        response = requests.request("GET",url=url,headers=header,verify=False)
        
        if response.status_code ==  requests.codes['ok']:
            return (response.json())
        else:
            raise Exception('Error: ' + str(response.status_code))

