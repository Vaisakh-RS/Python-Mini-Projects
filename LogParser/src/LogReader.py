import yaml
from LogParser import LogParser

#Load and read the config file
def load_config(configPath):
    with open(configPath , 'r') as file:
        logPath = yaml.safe_load(file)
        return logPath

class LogReader:
    def __init__(self,config_path):
        self.config_data=load_config(config_path)

    def parse_all(self):
       result={}
       for source in self.config_data["sources"]:
           name=source["name"]
           path=source["path"]
           parser=LogParser(path)
           parser.parse()
           result[name]=parser.log_entries
       return result


test=LogReader("LogParser\config.yaml")
res=test.parse_all()
print(res)