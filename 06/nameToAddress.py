def nameAtsToAddress(clearlist):
	for item in clearlist:
		if item.startswith("@"):
			if item[1:].isdigit():
				
			clearlist.remove(item)
		if item.startswith("("):