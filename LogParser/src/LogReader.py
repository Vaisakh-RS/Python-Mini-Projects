import yaml
from datetime import datetime
from LogParser import LogParser
import logging

logger=logging.getLogger(__name__)

#Load and read the config file
def load_config(configPath):
    with open(configPath , 'r') as file:
        logPath = yaml.safe_load(file)
        return logPath

class LogReader:
    def __init__(self,config_path):
        self.config_data=load_config(config_path)

    def parse_all(self):
       self.result={}
       for source in self.config_data["sources"]:
           name=source["name"]
           path=source["path"]
           parser=LogParser(path)
           parser.parse()
           self.result[name]=parser.log_entries
       return self.result

    #filter by log level from auth and db logs
    def filter(self):
        auth_logs = [entry for entry in self.result.get('auth',[]) if entry.log_level in ('ERROR', 'WARNING')]
        db_logs = [entry for entry in self.result.get('database',[]) if entry.log_level in ('ERROR', 'WARNING')]
        return auth_logs,db_logs

    def pair_logs(self,auth_errors,db_errors,window_seconds=150):
        pairs=[]
        for x in auth_errors:
            x_time=datetime.strptime(x.timestamp,"%Y-%m-%d %H:%M:%S")
            for y in db_errors:
                 y_time=datetime.strptime(y.timestamp,"%Y-%m-%d %H:%M:%S")
                 time_diff=abs(x_time-y_time)
                 if time_diff.total_seconds()<=window_seconds:
                     pairs.append((x,y))
            logger.info(f"Found {len(pairs)} correlated pairs")
        return pairs

test=LogReader("LogParser\config.yaml")
res=test.parse_all()
auth_errors,db_errors=test.filter()
pairs=test.pair_logs(auth_errors,db_errors)
print(pairs)


