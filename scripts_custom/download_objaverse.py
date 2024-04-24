
import objaverse
objaverse.__version__


annotations = objaverse.load_annotations()
objects = objaverse.load_objects(uids=random_object_uids, download_processes=processes)