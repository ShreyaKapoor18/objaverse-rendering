
import multiprocessing
import objaverse

objaverse.__version__

annotations = objaverse.load_annotations()
random_object_uids = list(annotations.keys())
processes = multiprocessing.cpu_count()
objects = objaverse.load_objects(uids=random_object_uids, download_processes=processes)