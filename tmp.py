from PIL import Image
import imagehash

hash0 = imagehash.average_hash('images/download.png') 
hash1 = imagehash.average_hash(Image.open('images/download1.png')) 
print(hash0-hash1)
