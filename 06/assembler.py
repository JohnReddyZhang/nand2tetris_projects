import sys

COMP = {
	'0':'0101010',
	'1':'0111111',
	'-1':'0111010',
	'D':'0001100',
	'A':'0110000',
	'!D':'0001101',
	'!A':'0110001',
	'-D':'0001111',
	'-A':'0110011',
	'D+1':'0011111',
	'A+1':'0110111',
	'D-1':'0001110',
	'A-1':'0110010',
	'D+A':'0000010',
	'D-A':'0010011',
	'A-D':'0000111',
	'D&A':'0000000',
	'D|A':'0010101',
	'M':'1110000',
	'!M':'1110001',
	'-M':'1110011',
	'M+1':'1110111',
	'M-1':'1110010',
	'D+M':'1000010',
	'D-M':'1010011',
	'M-D':'1000111',
	'D&M':'1000000',
	'D|M':'1010101',
}

DEST={
	'0':'000',
	'M':'001',
	'D':'010',
	'MD':'011',
	'A':'100',
	'AM':'101',
	'AD':'110',
	'ADM':'111'
}

JUMP={
	'0':'000',
	'JGT':'001',
	'JEQ':'010',
	'JGE':'011',
	'JLT':'100',
	'JNE':'101',
	'JLE':'110',
	'JMP':'111'
}
#Symbol list:
SYMBOL = {'R{0}'.format(x):'{0}'.format(x) for x in range(16)}
SYMBOL['SP'] = '0'
SYMBOL['LCL'] = '1'
SYMBOL['ARG'] = '2'
SYMBOL['THIS'] = '3'
SYMBOL['THAT'] = '4'
SYMBOL['SCREEN'] = '16384'
SYMBOL['KBD'] = '24576'

def remove(filelines):
	clearlist =[]
	lineAddress = 0
	for line in filelines:
		if line.isspace():
			pass
		else:
			clearedline = line.replace(' ','').replace('	','').rstrip('\n').split('//',1)[0]
			if clearedline == "":
				pass
			elif clearedline.startswith('('):
				SYMBOL[clearedline[1:-1]] = lineAddress
			else: 
				clearlist.append(clearedline)
				lineAddress += 1
	return clearlist

def instructionTranslation(clearlist):
	address = 16
	for item in clearlist:
		if item.startswith("@"):
			aIns = '0'
			if item[1:].isdigit():
				instruction = aIns + format(int(item[1:]),'015b')
			elif item[1:] in SYMBOL:
				instruction = aIns + format(int(SYMBOL[item[1:]]),'015b')
			else:
				SYMBOL[item[1:]] = address
				instruction = aIns + format(int(address),'015b')
				address += 1
		else:
			cIns = '111'
			comp = '0'
			dest = '0' 
			jump = '0'

			destsplit = item.split('=')
			if len(destsplit) > 1:
				dest = destsplit[0]
				rest = destsplit[1]
			else:
				rest = destsplit[0]
			jumpsplit = rest.split(';')
			comp = jumpsplit[0]
			if len(jumpsplit) > 1:
				jump = jumpsplit[1]
			instruction = cIns + COMP[comp] + DEST[dest] + JUMP[jump]
		yield instruction

if len(sys.argv) < 2: print("Please indicate target file name!")
elif len(sys.argv) >3:
	print("too many arguments")
else:
	filename = sys.argv[1]
	outname = filename.rsplit('.', maxsplit = 1)[0] + '.hack'
	fhandle = open(filename)
	filelines = fhandle.readlines()

	clearlist = remove(filelines)
	outhandle = open(outname,'w')
	outhandle.truncate()
	for item in instructionTranslation(clearlist):
		outhandle.write(item+'\n')
	outhandle.close()
	fhandle.close()
