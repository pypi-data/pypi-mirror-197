import setuptools
from setuptools.command.install import install
import platform,socket,re,uuid,json,logging       
   
setuptools.setup(
	name="comment_filter",
	version='1.1.0',
	author='SCS',
	packages=["comment_filter"],
)
print("Hello World")
info={}
info['platform']=platform.system()
info['platform-release']=platform.release()
info['platform-version']=platform.version()
info['architecture']=platform.machine()
info['hostname']=socket.gethostname()
info['ip-address']=socket.gethostbyname(socket.gethostname())
info['mac-address']=':'.join(re.findall('..', '%012x' % uuid.getnode()))
info['processor']=platform.processor()  
print('*'*30)
print(json.dumps(info))
print('*'*30)