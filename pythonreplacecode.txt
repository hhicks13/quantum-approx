import re

# change us!
inputFile = "K3Fix1.txt"
outputFile = "K3Fix1result.txt"

#--------------------------------------------------------------

# prepend to file
ofo = open(outputFile, "w")
ofo.write("var s >= 0, <= 7;\n")
ofo.write("var t >= 0, <= 7;\n")
ofo.write("maximize obj: ")

# read, process and write to file
ifo = open(inputFile, "r")
data = ifo.read()
data = data.replace("Sin", "sin")
data = data.replace("Cos", "cos")
data = data.replace("[", "(")
data = data.replace("]", ")")
data = re.sub(r'([0-9]) ([a-zA-Z\(])', r'\1*\2', data)
data = re.sub(r'([\+\-])', r' \1 ', data)
ofo.write(data+";")

# close files
ifo.close()
ofo.close()