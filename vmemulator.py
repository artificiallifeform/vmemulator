import sys

from Parser import Parser
from Code import Code

from commands import commands

# ./vmemulator <filename.vm> -> filename.asm

def init(vmFile):
    file_loc = vmFile.split('\\')
    file_name = file_loc[-1].split('.')[0]

    with open(vmFile, 'r') as f:
        while True:
            line = f.readline()

            if line.startswith('\n') or line.startswith('//'):
                continue


            if not line:
                break
            # Operation on parser
            parsed_c = Parser(line.replace('\n', '')).get_command()
            Code(parsed_c, file_name, commands).execute_operation()
init(sys.argv[1])