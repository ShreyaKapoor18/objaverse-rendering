import json

filename = f'/home/hpc/b112dc/b112dc10/git/objaverse-rendering/slurm_files' \
            '/output/test_distribution_load_slurm.804924.out'
f = open(filename, 'r')

dict_counts_new = {}
for line in f.readlines()[39:]:
    print(line)
    if ':' in line and 'Error' not in line and 'Location' not in line:
        print(line)
        object_name = line.split(':')[0].strip(' ')
        count = int(line.split(':')[1].strip('\n').strip(" "))
        dict_counts_new[object_name] = count

with open('results/backup_dict.json', 'w') as file:
    json.dump(dict_counts_new, file, indent=4)
        




