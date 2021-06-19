from ping3  import ping
import random ,re,os
from random import shuffle
from flask import flash
from PIL import Image
import imagehash


special_words = ['!', '@', '#', '$', '%', '^', '&','*', ':', '"', '?', '/', '(', ')', '+', '_']
#---------------------------------------------------------------------------------------------------------------------------------------------------        

class pw_maker():
        
    def password_maker(favourite_number,some_words):

        def emptyns_remover(x):
            return x !=''
        rand_list = some_words.split(" ")
        sent_list= list(filter(emptyns_remover,rand_list))
        password=''
        for letter in sent_list:
            password = password+letter[0]

        def the_mixer(pw,num):
            cont=0
            new_pass=''
            for i in pw:
                for n in num:
                    rand = random.randint(0,9)
                    if rand > 5 and cont < len(num):
                        new_pass=new_pass+num[cont]
                        cont=cont+1
                    break
                new_pass=new_pass+i    
            return new_pass

        pw_with_num = the_mixer(password,favourite_number)
        return the_mixer(pw_with_num,special_words)

    def conventer_to_list(word):
        def emptyns_remover(x):
            return x !=''
        rand_list = word.split(" ")
        return len(list(filter(emptyns_remover,rand_list)))
#---------------------------------------------------------------------------------------------------------------------------------------------------        
class pinger():
    def test_if_real(email):
        temp=str(email).split("@")
        link=str(temp[1])
        if ping(link):
            return False
        else:
            return True
#---------------------------------------------------------------------------------------------------------------------------------------------------        
class age():
    def to_integer(dt_time):
        return 10000*dt_time.year + 100*dt_time.month + dt_time.day
#---------------------------------------------------------------------------------------------------------------------------------------------------        
class how_strong():
    def how_strong(pw):
        cont=0
        if re.search(r'\d', pw):
            cont=cont+10
        if re.search(r'[a-z]', pw):
            cont=cont+26
        if re.search(r'[A-Z]', pw):
            cont=cont+26
        if re.search(r'[^a-zA-Z0-9]', pw):
            cont=cont+30
        return len(pw)*cont
    #---------------------------------------------------------------------------------------------------------------------------------------------------        

class directory():
    def directory_maker(userid):
        directory="static/images/"+str(userid)
        if not os.path.exists(directory):
            os.makedirs(directory)
        img_list =  os.listdir(directory)
        if len(img_list) <5:
            flash(" u need 2 upload 5 photos at lest !!")
        return directory
    def directory_scaner(directory):
        img_list =  os.listdir(directory)
        shuffle(img_list)
        return img_list



def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def hash_this_img(image):
    new_image = Image.new("RGBA", image.size, "WHITE") 
    new_image.paste(image, (0, 0), image)              
    new_image.convert('RGB')
    return imagehash.average_hash(new_image)  