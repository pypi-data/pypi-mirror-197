import logging
import libABCD

def init(n,loglevel=logging.DEBUG,fileloglevel=logging.INFO,cleansession=True,connect=True):
    # setting system-wide name
    libABCD.name=n
    libABCD.network_info["name"]=n
    # setting logger
    libABCD.logger=logging.getLogger(libABCD.name)
    libABCD._init_log_settings(libABCD.logger)
    libABCD.setstdout(loglevel)
    libABCD.setfilelog(fileloglevel)
    if connect:
        libABCD.connect(n,cleansession)
