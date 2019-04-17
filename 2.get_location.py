from multiprocessing import Pool
from datetime import datetime
import requests, time, os

list_of_files = os.listdir()			## List of files
clean_add_list = []					 ## Cleaned up address list, no \n
call_list = []						  ## Always have 4 in it all the time
output_list = ["Latitude\tLongitude\tAddress\tStatus"]
pool_num = 10
complete = 0
#######Insert the new API key below if needed#######
#####################API Key########################
API_key = #ENTER API KEY HERE 			   #
input_file = "1.address_list.txt"		   #
output_name = '3.output_list.txt'		   #
####################################################

starter = 'https://maps.googleapis.com/maps/api/geocode/json?address='
ender = '&key=' + API_key

with open(input_file) as f:
	content = f.readlines()

for each in content:
	clean_add_list.append(each.rstrip())


def f(x):
	address = x.rstrip()
	new_address = address.replace(" ", "+")
	push_request = starter + new_address + ender

	#get the result
	response = requests.get(push_request)

	#stores the result in JSON which will be extracted later
	resp_json_payload = response.json()

	try:
		lat_long = str(resp_json_payload['results'][0]['geometry']['location']['lat'])+"\t"+ str(resp_json_payload['results'][0]['geometry']['location']['lng'])+ "\t" + address
		return lat_long + "\t" + resp_json_payload['status'] 
	except:
		print("For",x, "Current status of the API: ", resp_json_payload['status'])
		return "No Data\tNo Data\t" + address + '\t' +resp_json_payload['status']
	

		
while len(content) != 0:
	call_list = []
	for i in range(1,pool_num+1):
		if len(content) == 0:
			break
		call_list.append(content.pop(0))

	if __name__ == '__main__':
		with Pool(pool_num) as p:
			z = p.map(f, call_list)
			complete = complete + int(len(z))
			print(complete)
			output_list = output_list + z #p.map(f, call_list)

with open(output_name, 'w') as z:
		for item in output_list:
			z.write("%s\n" % item)
