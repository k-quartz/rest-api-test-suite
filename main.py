import random
import string
from urllib.parse import  urlencode, urljoin
# from requests import request
from config import *
from payload import *

token = accessToken


class Payload(object):
    patient_payload_format = payload_format

    patient_payload = payload

    appointment_payload = appointment_payload


class FunctionValueList(object):

    def string_funct_value_list(self,key,strlen) -> None:
        value_list = []
        function_list = []
        value_list.append(" ")
        function_list.append(f"{key}_allow_blank")

        value_list.append("null")
        function_list.append(f"{key}_allow_null")

        rand_str = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(strlen))
        value_list.append(rand_str)
        function_list.append(f"{key}_allow_alpha_numeric")

        return value_list,function_list
    
    def process_string(self,parent_key,key,value,payload):
        value_list,function_list = self.string_funct_value_list(key,int(value.split("_")[1]))
        temp = payload[parent_key][key] 
        for i in range(0,len(value_list)):
            payload[parent_key][key]=value_list[i]
            # response = MHTMiddleWare().call_middleware(payload)
            # if response.status != 200:
            #     print(f"{fun_name_list[i]} failed.")
            print(key,"=========",payload)
            payload[parent_key][key] = temp
        
    

    def int_funct_value_list(self,key):
        value_list = []
        function_list = []
        value_list.append(" ")
        function_list.append(f"{key}_allow_blank")

        value_list.append("null")
        function_list.append(f"{key}_allow_null")

        rand_str = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(strlen))
        value_list.append(rand_str)
        function_list.append(f"{key}_allow_alpha_numeric")
        return value_list,self.function_list


    def process_int(self,parent_key,key,value,payload):
        value_list,fun_name_list = self.int_funct_value_list(key,int(value.split("_")[1]))
        temp = payload[parent_key][key] 
        for i in range(0,len(value_list)):
            payload[parent_key][key]=value_list[i]
            # response = MHTMiddleWare().call_middleware(payload)
            # if response.status != 200:
            #     print(f"{fun_name_list[i]} failed.")
            print(payload)
            payload[parent_key][key] = temp



class MHTMiddleWare(object):
    base_url = baseUrl

    def call_middleware(self,url, payload=None, token=None, query_params=None):
        try:
            headers = {
                'Content-type': 'application/json',
                'Accept': 'application/json'
            }
            url = self.base_url + url
            if token:
                headers.update({'Authorization': token})
            if query_params:
                url = f"{url}?{urlencode(query_params)}"
            # if payload:
            #     middleware_api = request("POST", url, headers=headers, json=payload)
            # else:
            #     middleware_api = request("GET", url, headers=headers)
            return middleware_api.json()
        except Exception as e:
            raise Exception(str(e))


class Patient(Payload):
    payload = {}

    def create_patient(self):
        self.populate_dict()

    def populate_dict(self, parent_key=None, parent_value=None):
        if parent_key and parent_value:
            for key, value in parent_value.items():
                if parent_key not in self.payload:
                    self.payload[parent_key] = {}
                if not isinstance(value, dict):
                    if value.split("_")[0] == "string":
                        FunctionValueList().process_string(parent_key,key,value,self.patient_payload)
                        # value_list,fun_name_list = FunctionValueList().string_funct_value_list(key,int(value.split("_")[1]))
                        # for i in range(0,len(value_list)):
                        #     temp = self.patient_payload[parent_key][key]
                        #     self.patient_payload[parent_key][key]=value_list[i]
                        # #     response = MHTMiddleWare().call_middleware(self.patient_payload)
                        #     print(key,"=======",self.patient_payload)
                        #     self.patient_payload[parent_key][key] = temp
                        # #     if response.status != 200:
                        # #         print(f"{fun_name_list[i]} failed.")
                else:
                    self.populate_dict(key, value)
        else:
            for key, value in self.patient_payload_format.items():
                if not isinstance(value, dict):
                    self.payload[key] = value
                    
                else:
                    self.populate_dict(key, value)


patient = Patient()
patient.create_patient()
