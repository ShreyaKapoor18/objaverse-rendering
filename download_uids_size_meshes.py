## Visualize the objects according to the Number of geometries
import multiprocessing
import objaverse
import glob


objaverse.BASE_PATH = 'objects'
objaverse._VERSIONED_PATH = 'objects'
num_geometries_objects = { '1' : ['9490b6ec7ea34b19a204dceca9bc6af8', '958bea47f15349c5a2b888f5180c3023'], 
    '2' : ['2ec20f15b08c4c2fb16e4df5d837b893', '5cfdc9a812524f4e9bcb5907a3175530'], 
    '5': ['5072a6cbabee47d7b2d7b74865bbc03b', '07bbf4c6cb8e4ea59a9afadae21f82cf'], 
    '20': ['18390cb5d75a4f03931551d542f322f4', '23ab40ea94f34f0c80abf29defbe284d']}

processes = multiprocessing.cpu_count()

for key in num_geometries_objects.keys():
    objects = objaverse.load_objects(
        uids= num_geometries_objects[key],
        download_processes=processes    
    )
    print(processes)



