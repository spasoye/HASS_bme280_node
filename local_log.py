import time
import os

class local_log:
    log_path = ""
    log_file = None
    
    def __init__(self, name):
        timestamp = time.localtime()
        self.log_path = name
        print("Log file: ", name)

    def log_write(self, data):
        open(self.log_path, "a")
        print("Checking size: ", self.log_path)
        file_stat = os.stat(self.log_path)
        print("Log file size: ", file_stat[6])
        # max log file size is 500
        if file_stat[6] > 500:
            print("Log file to big")
            os.remove(self.log_path)
            
        with open(self.log_path, "a") as f:
            print("Appending to log", self.log_path)
            timestamp = time.localtime()
            timestamp_str = str("%02d" % timestamp[3])+":"+str("%02d" % timestamp[4])+":"+str("%02d" % timestamp[5])
            f.write(timestamp_str +": "+ data+"\n")
            f.close()

    def log_close(self):
        self.log_file.close()
