import random
import string
from urllib.parse import  urlencode, urljoin
from requests import request

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo0LCJ1c2VyX25hbWUiOiJyYWtlc2hAeW9wbWFpbC5jb20iLCJyYW5kb21faWQiOiJlMzNiNDMyZi0xMTY3LTQ5M2YtOTg0Yy1kMGEwOWM2ZmJjZDEifQ.lsNE9nN0OnmHpxrqmIwq9jQZBD4qpZNCN8KzBw74UrQ"


class Payload(object):
    patient_payload_format = {
        "clinic_id": "integer",
        "patient": {
            "patient_id": "string_45",
            "patient_first_name": "string_45",
            "patient_middle_name": "string_45",
            "patient_last_name": "string_45",
            "patient_date_of_birth": "date_yyyy-mm-dd",
            "patient_sex": "string_45",
            "patient_email": "string_45",
            "patient_ethnicity": "string_45",
            "patient_mobile": "string_45",
            "patient_race": "string_45",
            "patient_preferred_language": "string_45",
            "patient_country_code": "string_45",
            "patient_state": "string_45",
        },
        "clinician": {
            "clinician_email": "string_45",
            "clinician_first_name": "string_45",
            "clinician_last_name": "string_45",
            "clinician_middle_name": "string_45",
            "npi_id": "string_45",
        },
    }

    patient_payload = {
        "clinic_id": 1,
        "patient": {
            "patient_id": "test994",
            "patient_first_name": "Robert",
            "patient_middle_name": "P",
            "patient_last_name": "William",
            "patient_date_of_birth": "2022-05-08",
            "patient_sex": "male",
            "patient_email": "patient_003@yopmail.com",
            "patient_ethnicity": "Hispanic/latino",
            "patient_mobile": "9087668744",
            "patient_race": "white",
            "patient_preferred_language": "en",
            "patient_country_code": "+91",
            "patient_state": "NV",
        },
        "clinician": {
            "clinician_email": "clinician_01@yopmail.com",
            "clinician_first_name": "Rakesh",
            "clinician_last_name": "S",
            "clinician_middle_name": "Singh",
            "npi_id": "1947",
        },
    }

    appointment_payload = {
        "clinic_id": "integer",
        "patient": {
            "patient_id": "string_45",
            "patient_first_name": "string_45",
            "patient_middle_name": "string_45",
            "patient_last_name": "string_45",
            "patient_date_of_birth": "date_yyyy-mm-dd",
            "patient_sex": "string_45",
            "patient_email": "string_45",
            "patient_ethnicity": "string_45",
            "patient_mobile": "string_45",
            "patient_race": "string_45",
            "patient_preferred_language": "string_45",
            "patient_country_code": "string_45",
            "patient_state": "string_45",
        },
        "clinician": {
            "clinician_email": "string_45",
            "clinician_first_name": "string_45",
            "clinician_last_name": "string_45",
            "clinician_middle_name": "string_45",
            "npi_id": "string_45",
        },
        "appointment": {
            "appointment_id": "int",
            "appointment_date": "datetime_yyyy-mm-dd hh:mm:ss",
        },
    }

class FunctionValueList(object):
    value_list = []
    function_list =[]


    def string_funct_value_list(self,key,strlen) -> None:
        self.value_list.append(" ")
        self.function_list.append(f"{key}_allow_blank")

        self.value_list.append("null")
        self.function_list.append(f"{key}_allow_null")

        rand_str = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(strlen))
        self.value_list.append(rand_str)
        self.function_list.append(f"{key}_allow_alpha_numeric")
        return self.value_list,self.function_list
    
    def process_string(self,keys,key,value,payload):
        value_list,fun_name_list = self.string_funct_value_list(key,int(value.split("_")[1]))
        temp = payload[keys][key] 
        for i in range(0,len(value_list)):
            payload[keys][key]=value_list[i]
            # response = MHTMiddleWare().call_middleware(payload)
            # if response.status != 200:
            #     print(f"{fun_name_list[i]} failed.")
        payload[keys][key] = temp
    

    def int_funct_value_list(self,key):
        self.value_list.append(" ")
        self.function_list.append(f"{key}_allow_blank")

        self.value_list.append("null")
        self.function_list.append(f"{key}_allow_null")

        rand_str = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(strlen))
        self.value_list.append(rand_str)
        self.function_list.append(f"{key}_allow_alpha_numeric")
        return self.value_list,self.function_list


    def process_int(self,keys,key,value,payload):
        value_list,fun_name_list = self.int_funct_value_list(key,int(value.split("_")[1]))
        temp = payload[keys][key] 
        for i in range(0,len(value_list)):
            payload[keys][key]=value_list[i]
            # response = MHTMiddleWare().call_middleware(payload)
            # if response.status != 200:
            #     print(f"{fun_name_list[i]} failed.")
        payload[keys][key] = temp



class MHTMiddleWare(object):
    base_url = "http://localhost:8001/"

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
            if payload:
                middleware_api = request("POST", url, headers=headers, json=payload)
            else:
                middleware_api = request("GET", url, headers=headers)
            return middleware_api.json()
        except Exception as e:
            raise Exception(str(e))


class Patient(Payload):
    payload = {}

    def create_patient(self):
        self.populate_dict()

    def populate_dict(self, keys=None, values=None):
        if keys and values:
            for key, value in values.items():
                if keys not in self.payload:
                    self.payload[keys] = {}
                if not isinstance(value, dict):
                    if value.split("_")[0] == "string":
                        FunctionValueList().process_string(keys,key,value,self.patient_payload)
                        # value_list,fun_name_list = FunctionValueList().string_format(key,int(value.split("_")[1]))
                        # for i in range(0,len(value_list)):
                        #     self.patient_payload[keys][key]=value_list[i]
                        #     response = MHTMiddleWare().call_middleware(self.patient_payload)
                        #     if response.status != 200:
                        #         print(f"{fun_name_list[i]} failed.")
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
