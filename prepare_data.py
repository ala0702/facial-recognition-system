import os
import shutil
import random
from tqdm import tqdm

base_path = r'C:\Users\ALA\.cache\kagglehub\datasets\rajnishe\facescrub-full\versions\1'
actors_dir = os.path.join(base_path, 'actor_faces')
actresses_dir = os.path.join(base_path, 'actress_faces')

output_dir = 'data_processed'
folders = ['gallery', 'test_known', 'test_unknown']

for f in folders:
    os.makedirs(os.path.join(output_dir, f), exist_ok=True)

def get_valid_identities(path):
    identities = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    return [d for d in identities if len(os.listdir(os.path.join(path, d))) >= 11]

# get list of people
all_actors = get_valid_identities(actors_dir)
all_actresses = get_valid_identities(actresses_dir)
    
# our database gallery - 50 facetów, 50 kobiet
chosen_actors_gallery = random.sample(all_actors, 50)
chosen_actresses_gallery = random.sample(all_actresses, 50)

# get rid of already chosen people for unknown set
remaining_actors = list(set(all_actors) - set(chosen_actors_gallery))
remaining_actresses = list(set(all_actresses) - set(chosen_actresses_gallery))

# select unknown people - 60 facetów, 60 kobiet
unknown_actors = random.sample(remaining_actors, 60)
unknown_actresses = random.sample(remaining_actresses, 60)

def process_set(names, src_root, is_gallery=True):
    for name in tqdm(names, desc=f"Przetwarzanie {'Galerii' if is_gallery else 'Obcych'}"):
        person_path = os.path.join(src_root, name)
        images = os.listdir(person_path)
        random.shuffle(images)
        
        if is_gallery:
            # Pierwsze zdjęcie do galerii, reszta do test_known
            shutil.copy(os.path.join(person_path, images[0]), 
                        os.path.join(output_dir, 'gallery', f"{name}_ref.jpg"))
            
            test_images = images[1:11] 
            for img in test_images:
                shutil.copy(os.path.join(person_path, img), 
                            os.path.join(output_dir, 'test_known', f"{name}_{img}"))
        else:
            shutil.copy(os.path.join(person_path, images[0]), 
                        os.path.join(output_dir, 'test_unknown', f"{name}_unknown.jpg"))


process_set(chosen_actors_gallery, actors_dir, is_gallery=True)
process_set(chosen_actresses_gallery, actresses_dir, is_gallery=True)
process_set(unknown_actors, actors_dir, is_gallery=False)
process_set(unknown_actresses, actresses_dir, is_gallery=False)

print(f"\n ZROBIONE:)! Pliki znajdziesz w folderze: {os.path.abspath(output_dir)}")