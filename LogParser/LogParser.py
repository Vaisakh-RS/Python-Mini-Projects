from dataclasses import dataclass

@dataclass
class LogEntry:
    timestamp: str
    log_level: str
    message: str

#normal methods will always have self as the first parameter
    def is_error(self):
        return self.log_level.upper() =="ERROR"

#log1=LogEntry("02026-08-19 09:58:03" , "INFO" , "service started successfully")
#log2=LogEntry("02026-08-20 10:54:03" , "ERROR" , "service terminated with timeout")



class LogParser:
    def __init__(self,file_path):
        self.file_path=file_path
        self.log_entries=[]

    def parse(self):
        with open(self.file_path ,"r",encoding="utf-8") as file:
            for line in file:
                words=line.split()
                timestamp=words[0] +" "+ words[1]
                log_level=words[2]
                message=words[3:]
                final_message=" ".join(message)
                logs=LogEntry(timestamp,log_level,final_message)
                self.log_entries.append(logs)

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
                
test=LogParser("D:/Py Projects/sample.log")
test.parse()
errors=test.count_by_severity()
print(errors)