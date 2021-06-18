from PIL import Image

img='images/download.png'

image= Image.open(img)

new_image = Image.new("RGBA", image.size, "WHITE") 
new_image.paste(image, (0, 0), image)              
new_image.convert('RGB').save(img, "PNG")   
