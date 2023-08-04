
import glob
import objaverse

rendering_path = '/home/janus/iwi9-datasets/views_release/*'
results_file = 'results/object_names_50.txt'
results_file = open(results_file, 'r').read()
annotations = objaverse.load_annotations()

for folder in glob.glob(rendering_path):
    object_idname = folder.split('/views_release/')[1]
    print(object_idname)
    if object_idname in results_file:
        annotation = annotations[object_idname]
        print(annotation)


