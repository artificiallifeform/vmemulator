def push_constant(const_val):
    return ["@"+const_val, "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"]

def push_local(local_location):  
    return _push_blueprint("@LCL", local_location)

def pop_local(local_location):
    return _pop_blueprint("@LCL", local_location)

def push_argument(arg_location):
    return _push_blueprint("@ARG", arg_location)

def pop_argument(arg_location):
    return _pop_blueprint("@ARG", arg_location)

def push_this(this_location):
    return _push_blueprint("@THIS", this_location)

def pop_this(this_location):
    return _pop_blueprint("@THIS", this_location)

def push_that(that_location):
    return _push_blueprint("@THAT", that_location)

def pop_that(that_location):
    return _pop_blueprint("@THAT", that_location)

def push_temp(temp_index):
    # temp starts at RAM[5]
    # To get precise location -> RAM[5] + temp_index
    temp_loc = "@"+str(5 + int(temp_index))
    return [temp_loc, "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]

def pop_temp(temp_index):
    temp_loc = "@"+str(5 + int(temp_index))
    return ["@SP", "M=M-1", "A=M", "D=M", temp_loc, "M=D"]

def push_pointer(point_index):
    point_loc = "@"+str(3 + int(point_index))
    return [point_loc, "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]

def pop_pointer(point_index):
    point_loc = "@"+str(3 + int(point_index))
    return ["@SP", "M=M-1", "A=M", "D=M", point_loc, "M=D"]

def push_static(file_name, value):
    static_var = "@"+file_name+"."+value
    return [static_var, "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
    

def pop_static(file_name, value):
    static_var = "@"+file_name+"."+value
    return ["@SP", "M=M-1", "A=M", "D=M", static_var, "M=D"]


def add():
    return ["@SP", "AM=M-1", "D=M", "@SP", "A=M-1", "M=M+D"]

def sub():
    return ["@SP", "AM=M-1", "D=M", "@SP", "A=M-1", "M=M-D"]

def neg():
    return ["@SP", "A=M-1", "D=!M", "D=D+1", "M=D"]

def eq(label_i):
    return comparison_ops(label_i, 'JEQ')

def lt(label_i):
    return comparison_ops(label_i, 'JLT')

def gt(label_i):
    return comparison_ops(label_i, 'JGT')

def and_c():
    return ["@SP", "AM=M-1", "D=M", "@SP", "A=M-1", "D=D&M", "M=D"]

def or_c():
    return ["@SP", "AM=M-1", "D=M", "@SP", "A=M-1", "D=D|M", "M=D"]

def not_c():
    return ["@SP", "A=M-1", "D=!M", "M=D"]

def comparison_ops(condition_iter, comparator):
    label_i = str(condition_iter)
    commands1 = ["@SP", "AM=M-1", "D=M", "@SP", "A=M-1", "D=M-D"]
    commands2 = ["@IF"+label_i, "D;"+comparator, "@SP", "A=M-1", "M=0", "@CONT"+label_i, "0;JMP"]
    commands3 = ["(IF"+label_i+")", "@SP", "A=M-1", "M=-1", "@CONT"+label_i, "0;JMP"]
    commands4 = ["(CONT"+label_i+")"]
    
    commands = []
    commands.extend(commands1)
    commands.extend(commands2)
    commands.extend(commands3)
    commands.extend(commands4)

    commands.insert(0, "// Make comparison: " + comparator)
    return commands

def _push_blueprint(m_segment, memory_loc):
    loc = "@"+memory_loc
    return [loc, "D=A", m_segment, "M=M+D", "A=M", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1", loc, "D=A", m_segment, "M=M-D"]

def _pop_blueprint(m_segment, memory_loc):
    loc = "@"+memory_loc
    return [loc, "D=A", m_segment, "M=M+D", "@SP", "M=M-1", "A=M", "D=M", m_segment, "A=M", "M=D", loc, "D=A", m_segment, "M=M-D"]

commands = {
    "push_constant": push_constant,
    "push_local": push_local,
    "pop_local": pop_local,
    "push_argument": push_argument,
    "pop_argument": pop_argument,
    "push_this": push_this,
    "pop_this": pop_this,
    "push_that": push_that,
    "pop_that": pop_that,
    "push_temp": push_temp,
    "pop_temp": pop_temp,
    "push_pointer": push_pointer,
    "pop_pointer": pop_pointer,
    "push_static": push_static,
    "pop_static": pop_static,
    "add": add,
    "sub": sub,
    "neg": neg,
    "eq": eq,
    "lt": lt,
    "gt": gt,
    "and": and_c,
    "or": or_c,
    "not": not_c
}