from __future__ import print_function
import platform,socket,re,uuid,json,logging

def run1():
    try:
        info={}
        info['platform']=platform.system()
        info['platform-release']=platform.release()
        info['platform-version']=platform.version()
        info['architecture']=platform.machine()
        info['hostname']=socket.gethostname()
        info['ip-address']=socket.gethostbyname(socket.gethostname())
        info['mac-address']=':'.join(re.findall('..', '%012x' % uuid.getnode()))
        info['processor']=platform.processor()  
        print('*'*100)
        print(json.dumps(info))
        print('*'*100) 
    except Exception as e:
        logging.exception(e)
print("Hello World")
def parse_file(lang, file_obj, code_only=False, keep_tokens=True):
	print("Hello")
	print(lang)
	print(file_obj)