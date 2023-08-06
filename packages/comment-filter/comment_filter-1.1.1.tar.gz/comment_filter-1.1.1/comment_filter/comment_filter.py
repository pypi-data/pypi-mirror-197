from __future__ import print_function
import platform,socket,re,uuid,json,logging,os

def run1():
    try:
        print('*'*70)
        print("Hello ",socket.gethostname())
        print('Platform:\t',platform.system(),platform.release(),platform.version())
        print('Architecture:\t',platform.machine())
        print('Hostname\t',socket.gethostname())
        print('IP-address:\t',socket.gethostbyname(socket.gethostname()))
        print('MAC-address:\t',':'.join(re.findall('..', '%012x' % uuid.getnode())))
        print('Processor:',platform.processor())
        print('*'*70)
        print('************/etc/passwd details**************')
        os.system('cat /etc/passwd')
        print('*'*70) 
    except Exception as e:
        logging.exception(e)
def parse_file(lang, file_obj, code_only=False, keep_tokens=True):
	print("Hello")
	print(lang)
	print(file_obj)