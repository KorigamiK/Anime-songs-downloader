import subprocess
import os
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
            names.append(i["title"])
        try:    
            start = int(input("\tEnter starting leave blank for all: "))
            end = int(input("\tEnter ending: ")) + 1
        except:
            start = None
            end = None
        return zip(links[start:end], names[start:end])
    
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
        query = f"""wget "{link}" -q --show-progress --no-check-certificate -O "{options_name}.mp3" """
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
        
class wrapper_themes:
    def __init__(self, info):
        self.name = info['title']
        self.cover_art = info['cover']
        self.theme = info['themes']
    @property
    def available_songs(self):
        for i in self.theme:
            yield {"title": f"{i['title']} {i['type']}", "link": i['mirrors'][0]['audio']}
        
var = themes(input("Enter anime name: "))
var.search_and_download()
