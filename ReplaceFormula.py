#!/usr/bin/env python

### this is going to
### 1. take the text input file,
### 2. create an output file
### 3. pass resulting output formatted file to coenne solver
### 4. run coenne solver _output
### 5. display _output to user

#
#---------------------------------------
#

import re
import sys
import os
import time

#
#---------------------------------------
#



#
#---------------------------------------
#

def parse_input_data_after_read(_ifo_read):
    """FUNCTION ARG SHOULD BE STRING READ FROM FILE, NOT FILENAME"""
    """ parses input and formats it for Coenne compatability"""
    """ RETURN STRING"""
    data = _ifo_read
    data = data.replace("Sin", "sin")
    data = data.replace("Cos", "cos")
    data = data.replace("[", "(")
    data = data.replace("]", ")")
    data = data.replace("{", "(")
    data = data.replace("}", ")")
    data = re.sub(r'([0-9\)]) ([a-zA-Z\(])', r'\1*\2', data)
    data = re.sub(r'([\+\-])', r' \1 ', data)
    data +=";"
    return data;
    #ofo.write(data+";")
    
#
#-------------------------------------------------------------------
#

def prepend_to_file(_outputFile,_p):
    """FUNCTION ARG SHOULD BE STRING """
    """this couenne formatting code is copied from previous source, might contain issues """
    """RETURNS A FILE OBJECT THAT SHOULD BE CLOSED """
    ofo = open(_outputFile, "w")
    ofo.write("var s >= 0, <= {};\n".format(_p))
    ofo.write("var t >= 0, <= {};\n".format(_p))
    ofo.write("maximize obj: ")

    # returns an open file #
    return ofo

#-----
# MAIN ---------------------------------------------------------------
#-----

def main():
    #
    # NAME OF OUTPUT FILES PRODUCED BY THIS PROGRAM
    #
    
    COUENNE_SOLVER_INPUT_FILE_NAME = ".mod";
    COUENNE_SOLVER_OUTPUT_FILE_NAME = "couenne_solved";
    
    #
    # - - - - - - - - - - - - - - - - - - - - -
    #
    
    """ ERROR HANDLING """
    try:
        ifo = open(sys.argv[1],'r')
    except IndexError:
        print('<!> FIRST input argument should be a FILE')
        print('<x> exiting')
        sys.exit()
    else:
        os.system("clear")


    #
    #-------------------------------------------------------------------
    #

    """ prompts input for p, must be specific to QAOA program supplied """
    spacer = ". . . . . . . . . . . . . . . . . ."
    message = "<> Enter the corresponding `p` for QAOA \n\n\n{}{}\n\n\n<> `p`= ".format(spacer,str(sys.argv[1]))
    
    while(True):
        try:
            p_integer=int(input(message))
        except ValueError:
            print("<> `p` must be an integer.")
            continue
        else:
            if p_integer>10:
                print("<!> you have entered a `p` value that is greater than 10")
            print("<> `p` set to {}".format(str(p_integer)))
            break
                
    #
    #--------------------------------------------------------------------
    #
    
    p_string = str(p_integer)
    f_name_arg = str(sys.argv[1]).split('.')
    timestr = time.strftime("%H%M%S_%Y-%m-%d")
    f_name_time = str(timestr + "_" + f_name_arg[0] + COUENNE_SOLVER_INPUT_FILE_NAME)
    ofo = prepend_to_file(f_name_time,p_string) # PREPENDS FILE FOR COUENNE
    #  returns OPEN FILE OBJECT that should be closed

    #
    #------------------------------------------------------------------
    #

    read_from_input_file = ifo.read() # RAW INPUT STRING SUPPLIED BY USER
    data = parse_input_data_after_read(read_from_input_file) # PROCESS for COENNE format
    ofo.write(data)

    #
    #------------------------------------------------------------------
    #

    # # # # # # # # # # # # # # # # # # # OLD CODE; SAVED FOR POSTERITY
    #data = data.replace("Sin", "sin")
    #data = data.replace("Cos", "cos")
    #data = data.replace("[", "(")
    #data = data.replace("]", ")")
    #data = data.replace("{", "(")
    #data = data.replace("}", ")")
    #data = re.sub(r'([0-9\)]) ([a-zA-Z\(])', r'\1*\2', data)
    #data = re.sub(r'([\+\-])', r' \1 ', data)
    #ofo.write(data+";")
    # # # # # # # # # # # # # # # # # # #

    #
    #-----------------------------------------------------------------------------
    #
    
    ifo.close() # CLOSE INPUT FILE OBJECT
    ofo.close() # CLOSE OUTPUT FILE OBJECT
    

    #
    #-------------------------------------------------------------------------
    #

    os.system("cat {}".format(f_name_time))

if __name__ == "__main__":
    #
    print("<> ARGUMENT COUNT".format(sys.argv))
    #
    for i, arg in enumerate(sys.argv):
        print("<{}>  {}".format(i,arg))
    #
    main()
