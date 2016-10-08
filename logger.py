"""
create a log that summarise the tests
"""

class Logger:
    def __init__(self,student_dir):
        self.file_name = "%s\\results.log" % student_dir
        open(self.file_name,'w').close()

    def append_line(self,line,e=None):
        with open(self.file_name,'a') as sf:
            sf.write(line)
            if e:
                sf.write('\t%s%s\n' % ('Python Error: ',e))


class Statements:
    NO_HOMEWORK = "Homework havn't been submitted\n"
    NO_FUNCTION = "\tFAIL: Function %s has an error\n"

    LOG_FUNCTION_PREFIX = "Function %s:\n"
    LOG_LINE = "\tTest [%d/%d] %s:\t\tExpected: %s\t\tGot: %s\t\t Input: %s\n"
    LOG_FUNCTION_DOCSTRING = '\tTest DocSting: %s\n'






