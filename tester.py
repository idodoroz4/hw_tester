"""
get yaml file with with input and outputs to a given hw
--- # beginning of yaml file
ex1: {input1: output1, input2: output2, input3: output3}
ex2: {input1: output1, input2: output2}
... # end of yaml file
"""
from imp import load_source
import os
import yaml
from logger import Logger
from logger import Statements as st


HW = "hw7"
STUDENTS_DIR = 'd:\\my_students\\'
STUDENTS_file = "%s%s" % (STUDENTS_DIR,"students.txt")
YAML_FILE = "%s%s" % (STUDENTS_DIR ,"test.yaml")
class HW_Tester:
    def __init__(self,init=False):
        self.init = init
        self.logger = None
        self.functions = None
        self.tests = None
        self.students = self._get_students(STUDENTS_file)
        self.prepare_folders()

    def sort_tests(self,tests):
        test_names = tests.keys()
        test_names.sort()
        return test_names

    @staticmethod
    def _get_students(student_file):
        with open(student_file,'r') as sf:
            student_list = sf.readlines()

        # remove spaces from begin and end of name (if there are any)
        student_list = [name.strip() for name in student_list]
        return student_list

    def prepare_folders(self):
        # creating a __init__.py file in student folder,
        # in order to import his hw as a module
        for student in self.students:
            if self.init and os.path.isdir("%s%s" % (STUDENTS_DIR,student)):
                for the_file in os.listdir("%s%s" % (STUDENTS_DIR,student)):
                    file_path = os.path.join("%s%s" % (STUDENTS_DIR,student), the_file)
                    try:
                         os.unlink(file_path)
                    except Exception as e:
                        print (e)
            if not os.path.isdir("%s%s" % (STUDENTS_DIR,student)):
                os.makedirs("%s%s" % (STUDENTS_DIR,student))
            open(
                    "%s%s\\__init__.py" % (STUDENTS_DIR,student),
                    'w'
                ).close()

    def import_test_file(self):
        with open(YAML_FILE, 'r') as stream:
            try:
                self.tests = (yaml.load(stream))
                self.functions = self.tests.keys()
                self.functions.sort()
            except yaml.YAMLError as e:
                print (e)

    def check_docstring (self,stu_hw,func):
        try:
            curr_func = getattr(stu_hw,func)
            docsting = getattr(curr_func,'__doc__')
        except Exception as e:
            return

        if docsting:
            self.logger.append_line(st.LOG_FUNCTION_DOCSTRING % 'PASS')
        else:
            self.logger.append_line(st.LOG_FUNCTION_DOCSTRING % 'FAIL')


    def test_module(self):
        if not self.init:
            for student in self.students:
                self.logger = Logger("%s%s" % (STUDENTS_DIR,student))
                try:
                    stu_hw = load_source("","%s%s\\%s.py" % (
                        STUDENTS_DIR,
                        student,
                        HW
                    ))
                    self.test_student(stu_hw)
                except Exception as e:
                    self.logger.append_line(st.NO_HOMEWORK,e.message)


    def test_student(self,stu_hw):

        # going over each function in student's Homework file
        for func in self.functions:
            self.logger.append_line(st.LOG_FUNCTION_PREFIX % func)
            num_of_tests = len(self.tests[func])
            sorted_test_names = self.sort_tests(self.tests[func])
            self.check_docstring(stu_hw,func)
            # going over each test related to a single function
            for test in sorted_test_names:
                my_input = tuple(self.tests[func][test]['input'])
                try:
                    curr_func = getattr(stu_hw,func)
                    stu_output = curr_func(*my_input)
                except Exception as e:
                    self.logger.append_line(st.NO_FUNCTION % func,e.message)
                    break

                expected_output = tuple(self.tests[func][test]['output'])
                res = self.compare_outputs(stu_output,expected_output)
                if res:
                    self.log_test_result_line(True,self.logger,sorted_test_names.index(test) + 1,num_of_tests,expected_output,stu_output,my_input)
                else:
                    self.log_test_result_line(False,self.logger,sorted_test_names.index(test) + 1,num_of_tests,expected_output,stu_output,my_input)


    def log_test_result_line(self,res,logger,test_num,num_of_tests,expected,got,my_input):
        if len(expected) == 1:
            expected = expected[0]
        if len(my_input) == 1:
            my_input = my_input[0]
        if res:
            logger.append_line(st.LOG_LINE % (test_num,num_of_tests,"PASS",str(expected),got,str(my_input)))
        else:
            logger.append_line(st.LOG_LINE % (test_num,num_of_tests,"FAIL",str(expected),got,str(my_input)))


    def compare_outputs(self,stu_out,expected_output):
        if stu_out == None:
            return None
        elif len(expected_output) == 1:
            return expected_output[0] == stu_out
        elif expected_output > 1:
            return tuple(stu_out) == tuple(expected_output)



