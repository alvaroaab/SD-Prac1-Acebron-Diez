from cos_backend import COSBackend
import json

def map_count_words(file, args):
    cos_params = args.get('cos_params')
    num_partition = args.get('num_partition')
    bucket_name = args.get('bucket_name')
    file_name = args.get('file_name')
    
    cos = COSBackend(cos_params)
    num_words = len(file.split())
    file_to_create = "cw_"+file_name+str(num_partition)
    cos.put_object(bucket_name,file_to_create,str(num_words))
    
    return {'finish': "OK"}

def map_word_count(file, args):
    cos_params = args.get('cos_params')
    num_partition = args.get('num_partition')
    bucket_name = args.get('bucket_name')
    file_name = args.get('file_name')
    
    cos = COSBackend(cos_params)
    split_file = file.split()
    new_dict = {}
    
    for word in split_file:
        paraula = str(word)
        if paraula not in new_dict.keys():
            new_dict[paraula]=1
        else:
            new_dict[paraula]+=1
    
    cos.put_object(bucket_name,str("wc_"+file_name+str(num_partition)),json.dumps(new_dict))    
    return {'finish': "OK"}


def main(args):
    cos = COSBackend(args.get('cos_params'))
    space = args.get('space')
    byte_range = "bytes=" + str(int(space[0])) + "-" + str(int(space[1]))
    file = cos.get_object(args.get('bucket_name'), args.get('file_name'), extra_get_args={'Range':byte_range})
    if int(args.get('program')) == 1:
        return map_count_words(file, args)
    else:
        return map_word_count(file, args)