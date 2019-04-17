import yaml
from ibm_cf_connector import CloudFunctions
import sys
import asyncio
from cos_backend import COSBackend
import json

#finalResult = {}
async def perform_cloud(name,params):
	#global finalResult
	ibm_cf.invoke_with_result(name, params)

with open('ibm_cloud_config', 'r') as config_file:
	res = yaml.safe_load(config_file)

if len(sys.argv) != 3:
	print("Han d'haver dos parametres: El fitxer a analitzar i el numero de particions")
	sys.exit()

bucket_name = 'acebron-diez-sd'
program = int(input("Seleccioni programa:\n1. CountingWords\n2. WordCount\n"))
if (program == 1 or program == 2):
	cos_backend = COSBackend(res.get('ibm_cos'))
	ibm_cf = CloudFunctions(res['ibm_cf'])
	file = sys.argv[1]
	file_size = int(cos_backend.head_object(bucket_name,file).get('content-length'))
	partition_size = file_size / int(sys.argv[2])
	params = {'program': program,'file_name':file,'cos_params':res.get('ibm_cos'),'bucket_name':bucket_name}
	loop = asyncio.get_event_loop()
	tasks = []
	for i in range(int(sys.argv[2])) :
		params['num_partition'] = i
		params['space'] = (i * partition_size, (i + 1) * partition_size)
		tasks.append(loop.create_task(perform_cloud('map', params.copy())))
	#Esperem fins que acabin les tasques al cloud.
	loop.run_until_complete(asyncio.gather(*tasks))
	#Tasques acabades:
	params['num_partitions'] = int(sys.argv[2])
	result = ibm_cf.invoke_with_result('reduce', params)
	if result.get('finish') == "OK":
		if program == 1:
			result = int(cos_backend.get_object(bucket_name, 'final_'+file))
			print("El fitxer "+file+" conte "+str(result)+" paraules.")
		else:
			result = json.loads(cos_backend.get_object(bucket_name, 'final_'+file))
			print(result)
	else:
		print("Error al fer el reduce")
		print(result)
		
else:
	print("Error: Havia de seleccionar 0 o 1 segons la opcio.")
