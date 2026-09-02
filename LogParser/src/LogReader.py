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
       self.result={}
       for source in self.config_data["sources"]:
           name=source["name"]
           path=source["path"]
           parser=LogParser(path)
           parser.parse()
           self.result[name]=parser.log_entries
       return self.result

    def filter(self):
      # Safely combines the two lists first, then filters the levels
        combined_lists = self.result.get('auth', []) + self.result.get('database', [])

        filtered_logs = [
            entry for entry in combined_lists 
            if entry.log_level in ('ERROR', 'WARNING')
        ]

        return filtered_logs



test=LogReader("LogParser\config.yaml")
res=test.parse_all()
res2=test.filter()
print(res2)

