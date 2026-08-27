from dataclasses import dataclass
import logging

logger=logging.getLogger(__name__)
logger.setLevel("DEBUG")

#print to the console and to a log file
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler("app.log", mode="a")

log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
console_handler.setFormatter(log_formatter)
file_handler.setFormatter(log_formatter)

# 4. Bind handlers to your logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)


@dataclass
class LogEntry:
    timestamp: str
    log_level: str
    message: str

#normal methods will always have self as the first parameter
    def is_error(self):
        return self.log_level.upper() =="ERROR"

class LogParser:
    def __init__(self,file_path):
        self.file_path=file_path
        self.log_entries=[]

    def parse(self):
        try:
            with open(self.file_path ,"r",encoding="utf-8") as file:
                for linenumber , line in enumerate(file , start=1):
                    try:
                        words=line.split()
                        timestamp=words[0] +" "+ words[1]
                        log_level=words[2]
                        message=words[3:]
                    except IndexError:
                        logger.warning(f"Index out of bounds on line {linenumber}")
                        continue
                    final_message=" ".join(message)
                    logs=LogEntry(timestamp,log_level,final_message)
                    self.log_entries.append(logs)
        except FileNotFoundError:
            logger.error(f"File not found:{self.file_path}")
       


    def filter_by_severity(self, level):
        return [entry for entry in self.log_entries if entry.log_level==level] # [ <what to put in the new list> for <item> in <iterable> if <condition> ]

    def count_by_severity(self):
        entries={"ERROR":0 , "INFO":0 , "WARNING":0, "OTHER":0}
        for entry in self.log_entries:
            if(entry.log_level)=="ERROR":
                entries["ERROR"]+=1
            elif(entry.log_level)=="INFO":
                entries["INFO"]+=1
            elif(entry.log_level)=="WARNING":
                entries["WARNING"]+=1
            else:
                entries["OTHER"]+=1
        return entries
# or def count_by_severity(self):
#     entries = {}
#     for entry in self.log_entries:
#         entries[entry.log_level] = entries.get(entry.log_level, 0) + 1 -->"give me the current count for this key, or 0 if it doesn't exist yet"
#     return entries
                
Parser=LogParser("D:/Py Projects/LogParser/sample.log")
# test.parse()
# print(test.log_entries)
# print(len(test.log_entries))