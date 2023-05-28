import matplotlib.pyplot as plt
import os
import glob
import matplotlib.pyplot as plt

categories = ['characters-creatures', 'cultural-heritage-history', 'furniture-home', 'art-abstract', 
                  'science-technology', 'architecture', 'cars-vehicles', 'places-travel', 'people', 'food-drink',
                  'fashion-style', 'sports-fitness', 'music', 'news-politics', 'animals-pets', 'nature-plants',
                  'electronic-gadgets', 'weapons-military']
views_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'views')
path = os.path.join(views_path, categories[0])
print(path)
print(glob.glob(os.path.join(path,'*', '000.png')))
for category in categories:
    fig, ax = plt.subplots(2,5)
    path = os.path.join(views_path, category)
    for file, i in zip(glob.glob(os.path.join(path, '*', '000.png')), range(10)):
        print(file)
        img = plt.imread(file)
        if i >= 5:
            ax[1, i%5].imshow(img)
            ax[1, i%5].set_xticks([])
            ax[1, i%5].set_yticks([])

        else:
            ax[0, i].imshow(img)
            ax[0,i].set_xticks([])
            ax[0, i].set_yticks([])
    #ax.set_axes('off')
    #plt.axes('off')
    plt.subplots_adjust(wspace=0, hspace=0)
    fig.tight_layout()
    plt.suptitle(category)
    plt.savefig(f'rendering_full_views/full_{category}.png')

