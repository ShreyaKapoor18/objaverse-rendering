import objaverse
import os
import glob


views_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'views')
uids = objaverse.load_uids()
annotations = objaverse.load_annotations()
categories = ['characters-creatures', 'cultural-heritage-history', 'furniture-home', 'art-abstract', 
                  'science-technology', 'architecture', 'cars-vehicles', 'places-travel', 'people', 'food-drink',
                  'fashion-style', 'sports-fitness', 'music', 'news-politics', 'animals-pets', 'nature-plants',
                  'electronic-gadgets', 'weapons-military']

for category in categories:
    if not os.path.exists(os.path.join((views_path), category)):
        os.mkdir(os.path.join(views_path, category))

for file in glob.glob(os.path.join(views_path, '*')):
    uid = file.split('/')[-1]
    if uid not in categories:
        print(uid)
        if len(annotations[uid]['categories']) == 1:
            category = annotations[uid]['categories'][0]['name']
        if len(annotations[uid]['categories']) == 2:
            category = annotations[uid]['categories'][1]['name']
        cmd = f'mv {file} {views_path}/{category}'
        os.system(cmd)
        print(cmd)








