from io import BytesIO
from PIL import Image
import os
import random
from time import sleep

import requests
from entities.data_scrapper import DataScrapper
from entities.match_data import MatchData
from entities.progress import print_progress
from bs4 import BeautifulSoup


class CreateThumbnail:
    def __init__(self, data_scrapper: DataScrapper, data: MatchData) -> None:
        self.scrapper = data_scrapper
        self.lol_data = data
        self.__thumb_path = os.path.abspath(r'.\media\thumb\thumb.png')
        self.__replay_file_dir = os.path.abspath(r'.\media\replays')
        file = os.listdir(self.__replay_file_dir)[0].split(".")[0]
        self.__static_thumb_path = os.path.join(
            os.path.abspath(r'.\media\AllThumbs'), f'{file}.png')
        self.total = 100
        print_progress(1, self.total, prefix='Creating Thumbnail:')
        self.skins = {
            "Yuumi": [0, 1, 11, 19, 28, 37, 39],
        }

    def exceptionHandle(self, name):
        # print(name)
        if(name == "AurelionSol"):
            return "aurelion-sol"
        elif (name == "KaiSa"):
            return "Kai-sa"
        elif (name == "VelKoz"):
            return "vel-koz"
        elif (name == "KhaZix"):
            return "kha-zix"
        elif (name == "NunuWillump"):
            return "Nunu"
        elif (name == "BelVeth"):
            return "Belveth"
        elif (name == "RenataGlasc"):
            return "Renata"
        elif (name == "TwistedFate"):
            return "Twisted-fate"
        elif (name == "LeeSin"):
            return "lee-sin"
        elif (name == "RekSai"):
            return "rek-sai"
        elif (name == "KSante"):
            return "k-sante"
        elif (name == "KogMaw"):
            return "Kog-maw"
        elif (name == "JarvanIV"):
            return "jarvan-iv"
        elif (name == "MasterYi"):
            return "Master-yi"
        else:
            return name

    def iconReplace(self, name):
        if (name == "KaiSa"):
            return "Kaisa"
        elif (name == "VelKoz"):
            return "Velkoz"
        elif (name == "KhaZix"):
            return "Khazix"
        elif (name == "NunuWillump"):
            return "Nunu"
        elif (name == "BelVeth"):
            return "Belveth"
        elif (name == "RenataGlasc"):
            return "Renata"
        elif (name == "TwistedFate"):
            return "Twisted-fate"
        elif (name == "LeeSin"):
            return "lee-sin"
        elif (name == "RekSai"):
            return "RekSai"
        elif (name == "Wukong"):
            return "MonkeyKing"
        else:
            return name

    def getSkin(self, name):
        # url = "https://www.leagueoflegends.com/en-gb/champions/{name}/"
        # make get request and use beautifulsoup and find the skin img urls
        url = "https://www.leagueoflegends.com/en-gb/champions/{}/".format(
            name)
        # print(url)
        r = requests.get(url)
        # if r.status_code is '404':
        #     url = "https://www.leagueoflegends.com/en-pl/champions/{}/".format(name)
        #     r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        skinsImgTag = soup.find_all('img')
        skinsUrls = list(set([skin.get('src') for skin in skinsImgTag]))
        filtered_urls = [
            skinUrl for skinUrl in skinsUrls if skinUrl is not None and "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/" in skinUrl]
        
        return filtered_urls

    def create_thumbnail(self):
        print_progress(5, self.total, prefix='Creating Thumbnail:')
        champion = self.lol_data['mvp']['champion']
        championRaw = champion
        champion = champion.replace("'", "& ")
        champion = champion.replace("&", "")
        if (len(champion.split()) == 1):
            champion = champion.capitalize()
        champion = champion.replace(" ", "")
        # champion = self.lol_data['mvp']['champion']
        # print(champion)
        championTemp = champion
        champion = self.exceptionHandle(champion)
        print_progress(8, self.total, prefix='Creating Thumbnail:')
        # if champion=="KaiSa":
        #     champion=="Kaisa"
        rank = self.lol_data['mvp']['rank']
        ranks = {
            "Iron": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/1.png",
            "Bronze": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/2.png",
            "Silver": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/3.png",
            "Gold": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/4.png",
            "Platinum": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/5.png",
            "Diamond": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/6.png",
            "Master": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/7.png",
            "GrandMaster": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/8.png",
            "Challenger": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/9.png"
        }
        print_progress(12, self.total, prefix='Creating Thumbnail:')
        rankIcon = ranks.get(rank)
        if (rankIcon is None):
            rankIcon = "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/9.png"
        spellImgs = os.listdir("assets/img/spell")
        print_progress(19, self.total, prefix='Creating Thumbnail:')
        spellImg = random.sample(spellImgs, 3)
        spellImgNew = self.lol_data['mvp']['spell']
        spellImgNew = [s+'.png' for s in spellImgNew]
        spellImg = spellImgNew
        print_progress(25, self.total, prefix='Creating Thumbnail:')

        loser = self.lol_data['loser']
        imgUrl = ""
        count = 0
        # print(champion)
        # print("match region:",self.lol_data['region'],os.path.exists(f"assets/img/{self.lol_data['region']}.png"))
        if (os.path.exists(f"assets/img/{self.lol_data['region']}.png")):
            region = self.lol_data['region']
        else:
            region = "EUW"
        # print(champion)
        skins = self.getSkin(champion)
        # print(skins)
        if (len(skins) == 0):
            print("\n==> Thumbnail creation failed \n==> Sent message to developer!\n==> Take a screenshot and sent mail to : tamilcomway@gmail.com")
            # print("==> Champion Temp: " + champonTemp)
            print("==> Champion name: " + str(champion))
            print("==> Raw Champion name: " + str(championRaw))
            print("==> URL:", imgUrl)
            return False
        imgUrl = random.choice(skins)

        print_progress(40, self.total, prefix='Creating Thumbnail:')
        oppIconImg = self.iconReplace(championTemp.replace(" ", ""))
        loserIcon = self.iconReplace(loser.replace(" ", ""))
        self.__create_html(
            kda=self.lol_data['mvp']['kda'].split("/"),
            imgUrl=imgUrl,
            mvp=self.lol_data['mvp']['name'],
            vs=self.lol_data['loser'],
            rank=rank.upper(),
            patch=self.lol_data['patch'],
            rankIcon=rankIcon,
            spellImg=spellImg,
            opponentIcon=f'https://opgg-static.akamaized.net/meta/images/lol/champion/{oppIconImg}.png',
            region=region,
            loserIcon=f'https://opgg-static.akamaized.net/meta/images/lol/champion/{loserIcon}.png',
        )
        print_progress(50, self.total, prefix='Creating Thumbnail:')
        html_path = os.path.abspath('assets/thumbnail.html')
        self.scrapper.driver.get('file://' + html_path)
        timer = 51
        for i in range(10):
            sleep(0.5)
            print_progress(timer+i*2, self.total, prefix='Creating Thumbnail:')
        self.scrapper.driver.set_window_size(1280, 805)
        print_progress(81, self.total, prefix='Creating Thumbnail:')
        screenshot = self.scrapper.driver.get_screenshot_as_png()
        print_progress(91, self.total, prefix='Creating Thumbnail:')
        with Image.open(BytesIO(screenshot)) as img:
            img = img.convert('RGB')
            img = img.resize((1280, 720))
            img.save(self.__thumb_path, quality=70)
            img.save(self.__static_thumb_path, quality=70)
        print_progress(100, self.total, prefix='Creating Thumbnail:')

        self.scrapper.driver.quit()
        return True

    def __create_html(self, kda: str, mvp: str, vs: str, rank: str, patch: str, imgUrl: str, rankIcon: str, spellImg: list, opponentIcon: str, region, loserIcon):
        none_vars = []
        if kda is None:
            none_vars.append('kda')
        if mvp is None:
            none_vars.append('mvp')
        if vs is None:
            none_vars.append('vs')
        if rank is None:
            none_vars.append('rank')
        if patch is None:
            none_vars.append('patch')
        if imgUrl is None:
            none_vars.append('imgUrl')
        if rankIcon is None:
            none_vars.append('rankIcon')
        if spellImg is None:
            none_vars.append('spellImg')
        if none_vars:
            # print(f"One or more arguments are None: {', '.join(none_vars)}")
            return
        with open("./assets/template.html", "r", encoding='utf-8') as f:
            HTML = f.read()
            # print(HTML)
        HTML = HTML.replace("backgroundImageLOL", imgUrl.replace("'", ""))
        HTML = HTML.replace("rankIconLOL", rankIcon)
        HTML = HTML.replace("loserIconLOL", loserIcon)
        HTML = HTML.replace("opponentIconLOL", opponentIcon)
        HTML = HTML.replace("patchLOL", patch)
        HTML = HTML.replace("rankLOL", rank)
        HTML = HTML.replace("regionLOL", region)
        HTML = HTML.replace("spellImg0LOL", spellImg[0])
        HTML = HTML.replace("spellImg1LOL", spellImg[1])
        HTML = HTML.replace("spellImg2LOL", spellImg[2])
        HTML = HTML.replace("mvpLOL", mvp)
        HTML = HTML.replace("kda0LOL", kda[0])
        HTML = HTML.replace("kda1LOL", kda[1])
        HTML = HTML.replace("kda2LOL", kda[2])

        with open("./assets/thumbnail.html", "w", encoding='utf-8') as f:
            f.write(HTML)


if __name__ == "__main__":
    from usecases.data import load
    lol_data: MatchData = load()
    thumb_creator = CreateThumbnail(
        data_scrapper=DataScrapper(), data=lol_data)
    thumb_creator.create_thumbnail()