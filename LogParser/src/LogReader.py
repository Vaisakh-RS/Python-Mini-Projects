from logging_config import setup_logging
setup_logging()

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
                     pairs.append((x,y,time_diff.total_seconds()))
        logger.info(f"Found {len(pairs)} correlated pairs")
        return pairs

    def format_pairs(self,pairs):
        formatted_pairs=[]
        for auth_entry,db_entry,time_gap in pairs:
            formatted_pairs.append(f"[CORRELATED] auth ({auth_entry.timestamp}): {auth_entry.message} <-> database ({db_entry.timestamp}): {db_entry.message} | gap: {time_gap:.0f}s")
        return formatted_pairs

test=LogReader("LogParser\config.yaml")
res=test.parse_all()
auth_errors,db_errors=test.filter()
pairs=test.pair_logs(auth_errors,db_errors)
formatted_result=test.format_pairs(pairs)
for line in formatted_result:
    print(line)
