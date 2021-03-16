"""
import all the reqiured librariers
"""
import requests
import json
from itertools import zip_longest
import difflib


from auth_header import Authentication as auth
from operations import Operation 




def url(vmanage_host,vmanage_port,api):
    """ return the URL for the privide API ENDpoint """
    """ function to get the url provide api endpoint """
    
    return f"https://{vmanage_host}:{vmanage_port}{api}"





def device_config(deviceIP):
    """
    To get DEVICE UUID - GET METHOD
    API-ENDPOINT - '/dataservice/system/device/vedges?deviceIP='+deviceIP+"&"
    returns (device_edge)
      "uuid": "37016829-0684-4f80-6430-d6760b00ce12",
      "templateStatus": "Success",
      "chasisNumber": "37016829-0684-4f80-6430-d6760b00ce12",
      "configStatusMessageDetails": "",
      "configOperationMode": "vmanage",
      "deviceModel": "vedge-cloud"
      "validity": "valid",
      "vedgeCertificateState": "certinstalled",
      "deviceIP": "5.5.5.5",
      "system-ip": "5.5.5.5",
      "model_sku": "None",
      "site-id": "56",
      "host-name": "vedge5",
      "version": "19.2.3",
      "vbond": "10.10.10.3",
      "vmanageConnectionState": "connected",
      "lastupdated": 1615817944413,
      "reachability": "reachable",
      "uptime-date": 1614690360000,
      "defaultVersion": "19.2.3",
      "availableVersions": [],
      "template": "Dual-VE-Tloc",
      "templateId": "e11e1bb3-f0e4-49a7-ab8b-c3f70c4fb584",
      "lifeCycleRequired": true,
      "expirationDate": "NA",
      "hardwareCertSerialNumber": "NA",
      "subjectSerialNumber": "NA"

      
    
    1. if - Checks if the System IP is present in the fabric
    2. elif - checks if the System IP is in CLI, IF in CLI MODE this will not work
    3. elif - vmanage mode
    
        GET the attached Config if the System attached to a feature template. - GET METHOD
        API ENDPOINT - /dataservice/template/config/attached/
        returns (device config)

    """

    
    api_device_edge = '/dataservice/system/device/vedges?deviceIP='+deviceIP+"&"
    url_device_edge = url(vmanage_host,vmanage_port,api_device_edge)
    device_edge = Operation.get_method(url_device_edge,header)

    
    
    if device_edge['data'] == []:
        return( " Unable to find the System IP " + deviceIP )
    
    elif device_edge['data'][0]["configOperationMode"] == "cli":
        return( "SystemIP " + deviceIP + " is in CLI mode unable to compare " )
    
    elif device_edge['data'][0]["configOperationMode"] == "vmanage":
        
        
        api_Template_Device_config = '/dataservice/template/config/attached/'+device_edge['data'][0]["uuid"]+"?type=CFS"
        url_Template_Device_config = url(vmanage_host,vmanage_port,api_Template_Device_config)
        Template_Device_config = Operation.get_method(url_Template_Device_config , header)

        return Template_Device_config['config']






"""
Input credintials

vmanage_host = '10.10.10.81'
vmanage_port = '8443'
username = 'admin'
password = 'admin'

deviceIP_1 = '5.5.5.5'
deviceIP_2 = '4.4.4.4'

"""
vmanage_host = input("vmanage host IP/DNS name :")
vmanage_port = input("vmanage port :")
username = input("Username :")
password = input("Password : ")

deviceIP_1 = input("please enter the SystemIP of the first  device : ")
deviceIP_2 = input("please enter the SystemIP of the second device : ")






filename = "C:/Users/shreredd/Desktop/compare" + "_" + deviceIP_1 + "_" + deviceIP_2 + ".txt"

""" GET the TOKEN from Authnetication call"""
header= auth.get_header(vmanage_host, vmanage_port,username, password)

""" Call Device Config function """
Template_Device_config_1 = device_config(deviceIP_1)
Template_Device_config_2 = device_config(deviceIP_2)
   




""" compare 2 device config in a same file"""
with open(filename, "w") as compare:
    Template_Device_config_two = Template_Device_config_2.split("\n")
    Template_Device_config_one = Template_Device_config_1.split("\n")
    for l1,l2 in zip_longest(Template_Device_config_one, Template_Device_config_two, fillvalue=""):
        text_to_write = f" {l1 : <140} {l2}\n"
        compare.write(text_to_write)

"""udiff two config"""

for line in difflib.unified_diff(Template_Device_config_two, Template_Device_config_one):
    print (line)


""" write device config to seprate file"""
with open("C:/Users/shreredd/Desktop/config_"+deviceIP_2+".txt","w" ) as file2:
    file2.write(Template_Device_config_2)

with open("C:/Users/shreredd/Desktop/config_"+deviceIP_1+".txt","w" ) as file1:
    file1.write(Template_Device_config_1)






    
