from LogParser import LogEntry , LogParser

def test_iserror():
    entry1=LogEntry("2026-08-19 09:58:03" ,"INFO", "service started successfully")
    entry2=LogEntry("2026-08-19 09:58:03" ,"ERROR", "service started successfully")
    result1=entry1.is_error()
    result2=entry2.is_error()
    #assert result2==True
    assert result1==False

def test_sortbyserverity():
    parser=LogParser("test.log")
    parser.log_entries=[LogEntry("2026-08-19 09:58:03" ,"INFO", "service started successfully"),LogEntry("2026-08-19 09:58:03" ,"ERROR", "service started successfully")]
    parser_result = parser.filter_by_severity("ERROR")
    assert parser_result==[LogEntry("2026-08-19 09:58:03" ,"INFO", "service started successfully")]