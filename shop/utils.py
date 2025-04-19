
from uuid import uuid4
import os
def create_randomint(count):
    import random
    print(10**(count-1))
    return random.randint(10**(count-1),10**(count)-1)
def send_sms(message,phone):
    print(message,'\n',phone)
    
    # try:
    #     api = KavenegarAPI('N',)
    #     params = {
    #         'sender': '2000660110',#optional
    #         'receptor': phone,#multiple mobile number, split by comma
    #         'message': message,
    #     } 
    #     response = api.sms_send(params)
    #     print(response)
    # except APIException as e: 
    #     print(e)
    #     print('a')
    # except HTTPException as e: 
    #     print(e)
    #     print('a')
#_________________________________NEXT_____________________________
class FileUplode:
    def __init__(self,dir,perfix):
        self.dir=dir
        self.perfix=perfix
    def uplode_to(self,instanse,filename):
        name,ext=os.path.splitext(filename)
        return f'{self.dir}/{self.perfix}/{uuid4()}{ext}'