#

TIME = /usr/bin/time


help:
	@echo no help

#  grep \"Software\":  data/catalog.json  | sed s/'        '\"Software\":// | sed s/\",//g | sed s/' '\"// | sort > code_nasa_gov.names

#   takes about 5.5 mins
list1:
	$(TIME) ./ads1.py code_nasa_gov.names > code_nasa_gov.txt
