import sys
import re
import os

variables = {'R0':0, 'R1':1, 'R2':2, 'R3':3, 'R4':4,
            'R5':5, 'R6':6, 'R7':7, 'R8':8, 'R9':9,
            'R10':10, 'R11':11, 'R12':12, 'R13':13, 'R14':14, 'R15':15,
            'SCREEN':16384, 'KBD':24576,
            'SP':0, 'LCL':1, 'ARG':2, 'THIS':3, 'THAT':4}
comp_instr = {
'0'  :'0101010',
'1'  :'0111111',
'-1' :'0111010',
'D'  :'0001100',
'A'  :'0110000', 'M'  :'1110000',
'!D' :'0001101',
'!A' :'0110001', '!M' :'1110001',
'-D' :'0001111',
'-A' :'0110011', '-M' :'1110011',
'D+1':'0011111',
'A+1':'0110111', 'M+1':'1110111', '1+A':'0110111', '1+M':'1110111',
'D-1':'0001110',
'A-1':'0110010', 'M-1':'1110010',
'D+A':'0000010', 'D+M':'1000010', 'A+D':'0000010', 'M+D':'1000010',
'D-A':'0010011', 'D-M':'1010011',
'A-D':'0000111', 'M-D':'1000111',
'D&A':'0000000', 'D&M':'1000000', 'A&D':'0000000', 'M&D':'1000000',
'D|A':'0010101', 'D|M':'1010101', 'A|D':'0010101', 'M|D':'1010101'}

jmp_instr = {
'null':'000',
'JGT':'001',
'JEQ':'010',
'JGE':'011',
'JLT':'100',
'JNE':'101',
'JLE':'110',
'JMP':'111'}

labels = {}
instructions = []
bitstream = []
def main():
    file_path =  sys.argv[1]
    f = open(file_path)
    dir_path = os.path.dirname(file_path)
    file_name = os.path.basename(file_path).split(".")[0]
    line_number = 0
    variable_address = 16

    for line in f: # find all labels
        line = line.split('//') # earse comment
        line = line[0].strip()  # earse space and newline
        if len(line) != 0:
            a = re.match(r'\((.*?)\)', line) # find (label)
            if a != None: # is label
                #print "  " + a.group(1) + " " + str(line_number)
                labels[a.group(1)] = line_number
            else:
                instructions.append(line)
                line_number += 1
                
    if dir_path == "":
        bin_file = open(file_name+".bin","w+")
    else:
        bin_file = open(dir_path+"/"+file_name+".bin","w+")
        
    for inst in instructions: # compile asm file
            instruction = re.search(r'@(.*)', inst)
            if instruction != None:  # A instruction
                A_instr = instruction.group(1)
                if A_instr.isdigit(): # is memory address
                    temp = int(A_instr)
                elif A_instr in labels: # is label
                    temp = labels[A_instr]
                elif A_instr in variables: # is variable
                    temp = variables[A_instr]
                else: # variable first appears
                    variables[A_instr] = variable_address
                    variable_address += 1
                    temp = variables[A_instr]
                #print format(temp,'b').zfill(16)
                bin_file.write(format(temp,'b').zfill(16)+'\n')
            else: # C instructions
                C_instr = re.search(r'(.*?);?(J.*)', inst)
                jmp = 'null'
                if C_instr != None: # has jmp instruction
                    instr = C_instr.group(1)
                    jmp = C_instr.group(2)
                    instr = re.search(r'([ADM]*)=?(.+)', instr)
                    dest = instr.group(1)
                    comp = instr.group(2)
                    #print dest + '=' + comp + ';' + jmp
                else:
                    instr = re.search(r'([MDA]*)=?(.+)', inst)
                    dest = instr.group(1)
                    comp = instr.group(2)
                    #print dest + '=' + comp
                temp = ''
                temp += ('1' if dest.find('A')!=-1 else '0')
                temp += ('1' if dest.find('D')!=-1 else '0')
                temp += ('1' if dest.find('M')!=-1 else '0')
                #print '111' + comp_instr[comp] + temp + jmp_instr[jmp]
                bin_file.write('111' + comp_instr[comp] + temp + jmp_instr[jmp]+'\n')
    bin_file.close()
if __name__ == "__main__":
    main()
