def remove(filelines):
	removed =[]
	for line in filelines:
		if line.isspace():
			# print('line {} startswith slash n'.format(line))
			pass
		else:
			clearedline = line.replace(' ','').replace('	','').split('//',1)[0]
			# print("cleared: {}".format(clearedline))
			if clearedline == "":
				# print('cleared one line: {}'.format(line))
				# print('line {} is cleared'.format(line))
				pass
			else: 
				# print('appending {}'.format(clearedline))
				removed.append(clearedline)
			# print(removed)
	return removed
	#
	# else:
	# 	if sys.argv[2] == "no-comments":
	# 		for line in fhandle:
	# 			if line.isspace():
	# 				continue
	# 			else:
	# 				outhandle.write(line.replace(' ','').replace('	','')
	# 					.split('//',1)[0])
	# 		outhandle.close()
	# 		fhandle.close()
	# 	else:
	# 		print("invalid argument")
