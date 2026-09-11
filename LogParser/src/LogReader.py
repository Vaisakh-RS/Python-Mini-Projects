from dataclasses import asdict
import json
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

#parse the log inputs from each sources
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

#pair two logs if they fall under the window_seconds timeframe
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

#format the correlated logs
    def format_pairs(self,pairs):
        formatted_pairs=[]
        for auth_entry,db_entry,time_gap in pairs:
            formatted_pairs.append(f"[CORRELATED] auth ({auth_entry.timestamp}): {auth_entry.message} <-> database ({db_entry.timestamp}): {db_entry.message} | gap: {time_gap:.0f}s")
        return formatted_pairs

    def export_to_json(self,pairs,output_path="correlation_report.json"):
        pairs_dict= [{"auth_entry":asdict(auth_entry),"db_entry":asdict(db_entry),"time_gap":gap} for auth_entry,db_entry,gap in pairs]
        with open(output_path,"w") as f:
            json.dump(pairs_dict,f,indent=2)
        logger.info(f"Exported {len(pairs_dict)} correlated pairs to {output_path}")
        return pairs_dict

test=LogReader("LogParser\config.yaml")
res=test.parse_all()
auth_errors,db_errors=test.filter()
pairs=test.pair_logs(auth_errors,db_errors)
formatted_result=test.format_pairs(pairs)
for line in formatted_result:
    print(line)
test.export_to_json(pairs)