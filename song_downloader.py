import subprocess
import os
import eyed3

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
try:
    import requests
except Exception:
    install('requests')
    print('INSTALLATION COMPLETE. RESTART REQUIRED!')
    exit()
    
class themes:
    def __init__(self, search):
        self.search = search
    @property
    def mal_ids(self):
        correct_format = self.search.replace(" ","%20")
        url = f"https://themes.moe/api/anime/search/{correct_format}"
        response = requests.get(url)
        return response.json()
    @staticmethod
    def get_info(malid):
        req = requests.get(f"https://animethemes-api.herokuapp.com/api/v1/anime/{malid}")
        return req.json()
    
    def get_links(self, option = 0):
        a = wrapper_themes(self.get_info(self.mal_ids[option]))
        links = []
        names = []
        for j,i in enumerate(a.available_songs):
            print("\t",j, i["title"])
            links.append(i["link"])
            names.append(i["title"]+".mp3")
        try:    
            start = int(input("\tEnter starting leave blank for all: "))
            end = int(input("\tEnter ending: ")) + 1
        except:
            start = None
            end = None
        return zip(links[start:end]+[a.cover_art], names[start:end]+[a.name+".jpg"])
    
    def search_result(self):
        results = []
        for j,i in enumerate(self.mal_ids):
            b = wrapper_themes(themes.get_info(i))
            print(j, b.name)
            results.append(b.name)
        option = int(input("Enter anime number: "))
        self.name = results[option]
        return option
        
    @staticmethod
    def download(link, options_name = ""):
        query = f"""wget "{link}" -q --show-progress --no-check-certificate -O "{options_name}" """
        subprocess.run(query, shell=True)
        
    def search_and_download(self):
        dow_urls_with_options = self.get_links(self.search_result())
        if not os.path.exists("./"+self.name):
            os.mkdir("./"+self.name)
            os.chdir("./"+self.name)
        else:
            os.chdir("./"+self.name)
        for i,j in dow_urls_with_options:
            themes.download(i,j)
            if '.jpg' in j:
                themes.embeder()
                
    @staticmethod
    def embeder():
        for j in os.listdir():
            if '.jpg' in j:
                image = j 
        for j in os.listdir():
            if '.mp3' in j:
                themes.embed_art(j, image)
        os.remove(image)       
    @staticmethod
    def embed_art(mp3, photo) :
        audiofile = eyed3.load(mp3)
        if (audiofile.tag == None):
            audiofile.initTag()
        audiofile.tag.images.set(3, open(photo,'rb').read(), 'image/jpeg')
        audiofile.tag.save()
        
class wrapper_themes:
    def __init__(self, info):
        self.name = info['title']
        self.cover_art = info['cover']
        self.theme = info['themes']
        
    @property#gives title and audio links
    def available_songs(self):
        for i in self.theme:
            yield {"title": f"{i['type']} {i['title']}", "link": i['mirrors'][0]['audio']}
        
var = themes(input("Enter anime name: "))
var.search_and_download()
