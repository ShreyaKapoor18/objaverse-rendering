## Visualize the objects according to the Number of geometries
import multiprocessing
import objaverse
import glob


objaverse.BASE_PATH = 'objects'
objaverse._VERSIONED_PATH = 'objects'
num_geometries_objects = {
    '5': [ '92a16ad274d74e9eb9ec3a8c6f724c12','8e2da20d1b794e8aa50ae447c2c8a0d5','270254c0b1c64c19add8f2818d9a2f88'], 
    '20': [ 'a710033f37104a128fed1e6b9ccd6eae', 'a2c74f694f3b41e28ec5c069acff8e61', '9590ca9bbe8444fab91b347fff0675bb' , 
           '690ad276dc334ee38cc528697847af39']}
processes = multiprocessing.cpu_count()

for key in num_geometries_objects.keys():
    objects = objaverse.load_objects(
        uids= num_geometries_objects[key],
        download_processes=processes    
    )
    print(processes)



