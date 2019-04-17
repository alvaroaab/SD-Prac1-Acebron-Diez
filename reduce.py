from cos_backend import COSBackend
import json

def reduce_count_words(args):
    file_name = args.get('file_name')
    num_partitions = args.get('num_partitions')
    cos = COSBackend(args.get('cos_params'))
    bucket_name = args.get('bucket_name')
    total_words = 0
    
    for i in range(num_partitions):
        file = "cw_"+file_name+str(i)
        total_words += int(cos.get_object(bucket_name, file))
        cos.delete_object(bucket_name, file)

    cos.put_object(bucket_name, "final_"+file_name, str(total_words))
    
    #for i in range(num_partitions):
    #    file_to_delete = "cw_"+file_name+str(i)
    #    cos.delete_object(bucket_name, file_to_delete)
        
    return {'finish': "OK"}
    
def reduce_word_count(args):
    file_name = args.get('file_name')
    num_partitions = args.get('num_partitions')
    cos = COSBackend(args.get('cos_params'))
    bucket_name = args.get('bucket_name')
    result_dict = {}
    
    for i in range(num_partitions):
        file = "wc_"+file_name+str(i)
        file_dict = json.loads(cos.get_object(bucket_name, file))
        cos.delete_object(bucket_name, file)   
        result_dict = {key: result_dict.get(key, 0) + file_dict.get(key, 0)
                  for key in set(result_dict) | set(file_dict)} 
          
    cos.put_object(bucket_name, "final_"+file_name, json.dumps(result_dict))
    return {'finish': "OK"}

def main(args):
    if int(args.get('program')) == 1:
        return reduce_count_words(args)
    else:
        return reduce_word_count(args)