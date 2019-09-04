import sys
import re
from constant import *

class Code_Writer():
    def __init__(self, file_name):
        self.asm_file = open(file_name,"w")
        self.label_num = 1;
        self.current_file_name = ""
        self.write_Init("256")

    def __exit__(self, exception_type, exception_value, traceback):
        self.asm_file.close()

    def set_current_file_name(self,file_name):
        self.current_file_name = file_name

    def write_comment(self,comment):
        self.asm_file.writelines(comment+"\n")

    def write_label(self,label):
        self.asm_file.writelines("  "+label+"\n")

    def write_code(self,code):
        self.asm_file.writelines("      "+code+"\n")

    def get_new_label(self):
        self.label_num += 1;
        return self.label_num

    def write_Init(self,SP_address):
        self.write_code("@"+SP_address)
        self.write_code("D=A")
        self.write_code("@SP")
        self.write_code("M=D")
        self.WriteCall("Sys.init","0")
        return

    def write_to_stack(self):
        self.write_code("@SP")
        self.write_code("A=M")
        self.write_code("M=D")
        self.write_code("@SP")
        self.write_code("M=M+1")

    def read_from_stack(self):
        self.write_code("@SP")
        self.write_code("M=M-1")
        self.write_code("A=M")

    def WritePushPop(self, command_type, segment, index):
        self.write_comment( "//" + command_type + " " + segment + " " + index )
        if command_type == "push":
            if segment == "constant":
                self.write_code("@"+index+"")
                self.write_code("D=A")
                self.write_to_stack()

            elif segment == "temp":
                self.write_code("@" + str(5+int(index)))
                self.write_code("D=M")
                self.write_to_stack()

            elif segment == "pointer":
                if index == "0":
                    self.write_code("@THIS")
                elif index == "1":
                    self.write_code("@THAT")
                else:
                    print "ERROR: pointer have error index "
                self.write_code("D=M")
                self.write_to_stack()

            elif segment == "static":
                self.write_code("@" + self.current_file_name + "." + index)
                self.write_code("D=M")
                self.write_to_stack()

            elif segment in ["local","argument","this","that"]:
                if segment == "local":
                    segment = "LCL"
                elif segment == "argument":
                    segment = "ARG"
                elif segment == "this":
                    segment = "THIS"
                elif segment == "that":
                    segment = "THAT"

                self.write_code("@"+segment)
                self.write_code("A=M")
                for i in range(int(index)):
                    self.write_code("A=A+1")
                self.write_code("D=M")
                self.write_to_stack()

        elif command_type == "pop":
            if segment == "temp":
                self.read_from_stack()
                self.write_code("D=M")
                self.write_code("@" + str(5 + int(index)))
                self.write_code("M=D")

            elif segment == "pointer":
                self.read_from_stack()
                self.write_code("D=M")
                if index == "0":
                    self.write_code("@THIS")
                elif index == "1":
                    self.write_code("@THAT")
                else:
                    print "ERROR: pointer have error index "
                self.write_code("M=D")

            elif segment == "static":
                self.read_from_stack()
                self.write_code("D=M")
                self.write_code("@" + self.current_file_name + "." + index)
                self.write_code("M=D")

            elif segment in ["local","argument","this","that"]:
                if segment == "local":
                    segment = "LCL"
                elif segment == "argument":
                    segment = "ARG"
                elif segment == "this":
                    segment = "THIS"
                elif segment == "that":
                    segment = "THAT"

                self.read_from_stack()
                self.write_code("D=M")
                self.write_code("@"+segment)
                self.write_code("A=M")
                for i in range(int(index)):
                    self.write_code("A=A+1")
                self.write_code("M=D")

    def WriteArithmetic(self, command_type):
        self.write_comment("//" + command_type)
        if command_type in ["add","sub","and","or"]:
            self.read_from_stack()
            self.write_code("D=M")
            self.read_from_stack()
            if command_type == "add":
                self.write_code("D=D+M")
            elif command_type == "sub":
                self.write_code("D=M-D")
            elif command_type == "and":
                self.write_code("D=D&M")
            elif command_type == "or":
                self.write_code("D=D|M")
            self.write_to_stack()

        elif command_type in ["neg","not"]:
            self.read_from_stack()
            if command_type == "neg":
                self.write_code("D=-M")
            elif command_type == "not":
                self.write_code("D=!M")
            self.write_to_stack()

        elif command_type in ["eq","gt","lt"]:
            l1 = self.current_file_name + "$" + "LABEL_" + str(self.get_new_label())
            l2 = self.current_file_name + "$" + "LABEL_" + str(self.get_new_label())
            self.read_from_stack()
            self.write_code("D=M")
            self.read_from_stack()
            self.write_code("D=M-D")
            self.write_code("@"+l1)
            if command_type == "eq":
                self.write_code("D;JEQ")
            elif command_type == "gt":
                self.write_code("D;JGT")
            elif command_type == "lt":
                self.write_code("D;JLT")
            self.write_code("D=0")
            self.write_to_stack()
            self.write_code("@"+l2)
            self.write_code("0;JMP")
            self.write_label("("+l1+")")
            self.write_code("D=-1")
            self.write_to_stack()
            self.write_label("("+l2+")")

    def WriteLabel(self, label):
        self.write_comment("// label " + label)
        self.write_label("(" + self.current_file_name + "$" + label + ")")

    def WriteGoto(self, label):
        self.write_comment("// goto " + label)
        self.write_code("@" + self.current_file_name + "$" + label)
        self.write_code("0;JMP")

    def WriteIf(self, label):
        self.write_comment("// if-goto " + label)
        self.read_from_stack()
        self.write_code("D=M")
        self.write_code("@" + self.current_file_name + "$" + label)
        self.write_code("D;JNE")

    def WriteFunction(self, function_name, nVars):
        self.write_comment("// " + function_name + " " + nVars)
        self.write_label("(" + function_name + ")")
        self.write_code("D=0") # initial local variables to 0
        for i in range(int(nVars)):
            self.write_to_stack()

    def WriteCall(self, function_name, nArgs):
        self.write_comment("// call " + function_name + " " + nArgs)
        # push return address ---1
        return_label = function_name + "$ret." + str(self.get_new_label())
        self.write_code("@"+return_label)
        self.write_code("D=A")
        self.write_to_stack()
        # push LCL ---2
        self.write_code("@LCL")
        self.write_code("D=M")
        self.write_to_stack()
        # push ARG ---3
        self.write_code("@ARG")
        self.write_code("D=M")
        self.write_to_stack()
        # push THIS ---4
        self.write_code("@THIS")
        self.write_code("D=M")
        self.write_to_stack()
        # push THAT ---5
        self.write_code("@THAT")
        self.write_code("D=M")
        self.write_to_stack()
        # ARG = SP - 5 - nArgs
        self.write_code("@SP")
        self.write_code("D=M")
        self.write_code("@5")
        self.write_code("D=D-A")
        self.write_code("@"+nArgs)
        self.write_code("D=D-A")
        self.write_code("@ARG")
        self.write_code("M=D")
        # LCL = SP
        self.write_code("@SP")
        self.write_code("D=M")
        self.write_code("@LCL")
        self.write_code("M=D")
        # goto function_name
        self.write_code("@"+function_name)
        self.write_code("0;JMP")
        # put return label
        self.write_label("(" + return_label + ")")

    def WriteReturn(self):
        self.write_comment("// return")
        # save endframe to R15
        self.write_code("@LCL")
        self.write_code("D=M")
        self.write_code("@R15")
        self.write_code("M=D")
        # save return address to R14
        self.write_code("@R15")
        self.write_code("D=M")
        self.write_code("@5")
        self.write_code("D=D-A")
        self.write_code("A=D")
        self.write_code("D=M")
        self.write_code("@R14")
        self.write_code("M=D")
        # put return value to *ARG
        self.read_from_stack()
        self.write_code("D=M")
        self.write_code("@ARG")
        self.write_code("A=M")
        self.write_code("M=D")
        # SP = ARG + 1
        self.write_code("@ARG")
        self.write_code("D=M+1")
        self.write_code("@SP")
        self.write_code("M=D")
        # restore THAT
        self.write_code("@R15")
        self.write_code("D=M")
        self.write_code("@1")
        self.write_code("D=D-A")
        self.write_code("A=D")
        self.write_code("D=M")
        self.write_code("@THAT")
        self.write_code("M=D")
        # restore THIS
        self.write_code("@R15")
        self.write_code("D=M")
        self.write_code("@2")
        self.write_code("D=D-A")
        self.write_code("A=D")
        self.write_code("D=M")
        self.write_code("@THIS")
        self.write_code("M=D")
        # restore ARG
        self.write_code("@R15")
        self.write_code("D=M")
        self.write_code("@3")
        self.write_code("D=D-A")
        self.write_code("A=D")
        self.write_code("D=M")
        self.write_code("@ARG")
        self.write_code("M=D")
        # restore LCL
        self.write_code("@R15")
        self.write_code("D=M")
        self.write_code("@4")
        self.write_code("D=D-A")
        self.write_code("A=D")
        self.write_code("D=M")
        self.write_code("@LCL")
        self.write_code("M=D")
        # goto return address
        self.write_code("@R14")
        self.write_code("A=M")
        self.write_code("0;JMP")
