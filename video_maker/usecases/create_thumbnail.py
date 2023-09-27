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
        self.__static_thumb_path = os.path.join(os.path.abspath(r'.\media\AllThumbs'),f'{file}.png')
        self.total=100
        print_progress(1, self.total, prefix='Creating Thumbnail:')
        self.skins ={
            "Yuumi":[0,1,11,19,28,37,39],
        }
    def exceptionHandle(self,name):
        # print(name)
        # if(name == "Wukong"):
        #     return "MonkeyKing"
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
            return "bel-veth"
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
        elif (name == "Dr.Mundo"):
            return "dr-mundo"
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
        elif (name == "RekSai"):
            return "RekSai"
        elif (name == "Wukong"):
            return "MonkeyKing"
        elif (name == "Dr.Mundo"):
            return "DrMundo"
        else:
            return name
    def getSkin(self, name):
        # url = "https://www.leagueoflegends.com/en-gb/champions/{name}/"
        # make get request and use beautifulsoup and find the skin img urls
        url = "https://www.leagueoflegends.com/en-gb/champions/{}/".format(name)
        # print(url)
        r = requests.get(url)
        # if r.status_code is '404':
        #     url = "https://www.leagueoflegends.com/en-pl/champions/{}/".format(name)
        #     r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        skinsImgTag = soup.find_all('img')
        skinsUrls = list(set([skin.get('src') for skin in skinsImgTag]))
        filtered_urls = [skinUrl for skinUrl in skinsUrls if skinUrl is not None and "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/" in skinUrl]

        return filtered_urls
    
    def create_thumbnail(self):
        print_progress(5, self.total, prefix='Creating Thumbnail:')
        champion = self.lol_data['mvp']['champion']
        champion = champion.replace("'", "& ")
        champion = champion.replace("&","")
        if(len(champion.split())==1):
            champion = champion.capitalize()
        champion = champion.replace(" ", "")
        # champion = self.lol_data['mvp']['champion']
        # print(champion)
        championTemp = champion
        champion = self.exceptionHandle(champion)
        print_progress(8, self.total, prefix='Creating Thumbnail:')
        # if champion=="KaiSa":
        #     champion=="Kaisa"
        rank=self.lol_data['mvp']['rank']
        ranks= {
            "Iron": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/1.png",
            "Bronze": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/2.png",
            "Silver": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/3.png",
            "Gold": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/4.png",
            "Platinum": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/5.png",
            "Emerald": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/6.png",
            "Diamond": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/7.png",
            "Master": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/8.png",
            "GrandMaster": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/9.png",
            "Challenger": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/10.png"
        }
        print_progress(12, self.total, prefix='Creating Thumbnail:')
        rankIcon=ranks.get(rank)
        if(rankIcon is None):
            rankIcon="https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/9.png"
        spellImgs=os.listdir("assets/img/spell")
        print_progress(19, self.total, prefix='Creating Thumbnail:')
        spellImg=random.sample(spellImgs, 3)
        spellImgNew=self.lol_data['mvp']['spell']
        spellImgNew=[s+'.png' for s in spellImgNew]
        spellImg=spellImgNew
        print_progress(25, self.total, prefix='Creating Thumbnail:')
        
        loser=self.lol_data['loser']
        imgUrl=""
        count=0
        # print(champion)
        # print("match region:",self.lol_data['region'],os.path.exists(f"assets/img/{self.lol_data['region']}.png"))
        if(os.path.exists(f"assets/img/{self.lol_data['region']}.png")):
            region=self.lol_data['region']
        else:
            region="EUW"
        # print(champion)
        skins = self.getSkin(champion)
        # print(skins)
        if(len(skins)==0):
            print("\n==> Thumbnail creation failed \n==> Sent message to developer!\n==> Take a screenshot and sent mail to : tamilcomway@gmail.com")
            # print("==> Champion Temp: " + champonTemp)
            print("==> Champion name: " + str(champion))
            print("==> URL:",imgUrl)
            return False
        imgUrl=random.choice(skins)

        print_progress(40, self.total, prefix='Creating Thumbnail:')
        oppIconImg = self.iconReplace(championTemp.replace(" ",""))
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
            region=region
        )
        print_progress(50, self.total, prefix='Creating Thumbnail:')
        html_path = os.path.abspath('assets/thumbnail.html')
        self.scrapper.driver.get('file://' + html_path)
        timer=51
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

    def __create_html(self, kda: str, mvp: str, vs: str, rank: str, patch: str, imgUrl: str,rankIcon:str,spellImg:list,opponentIcon:str,region):
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
        HTML = """<!DOCTYPE html>
<html>
<head>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;800&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Nanum Gothic', sans-serif;
        }
        .container {
            background-image: url('"""+imgUrl.replace("'","")+"""');
            background-size: cover;
            width: 1280px;
            height: 720px;
            display: flex;
            align-items: center;
            position: relative; /* Add position relative to container */
        }
        .frame {
            width: 500px;
            height: 650px;
            margin-left: 50px;
            background-color: rgba(0, 0, 0, .6);
            filter: drop-shadow(0px 20px 10px rgba(0, 0, 0, 0.3));
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            font-weight: 800;
        }
        .kda {
            margin-top: 2rem;
            color: white;
            font-size: 2.5rem;
            display: flex;
            justify-content: center;
            background-color: rgba(0, 0, 0, .5);
            filter: drop-shadow(0px 20px 10px rgba(0, 0, 0, 0.3));
            border-radius:50%;
            width:4rem;
            height:4rem;
            align-items: center;
            border: 2px solid white;
            margin: 2px -2px 5px 18px;
        }
        .match {
            display: flex;
            flex-direction: column;
            align-items: center;
            color: white;
        }
        .mvp {
            font-size: 3.5rem; /* set the font size to 10% of the viewport width */
            position: absolute;
            bottom: 158px;
            white-space: nowrap;
        }
        .vs {
            font-size: 2rem;
        }
        .region {
            background-color: aquamarine;
            color: #444;
            padding: .5rem 1.5rem;
            border-radius: 2rem;
            font-size: 2rem;
        }
        .patch {
            color: white;
            font-size: 3rem;
            position: absolute; /* Add position absolute to patch div */
            top: 0; /* Position it at the top */
            right: 0; /* Position it at the right */
            margin: 3rem; /* Add margin to create some space */
            background-color: rgba(0, 0, 0, .4);
            filter: drop-shadow(0px 20px 10px rgba(0, 0, 0, 0.3));
            font-weight: bold;
        }
        .kdatext{
            font-size: 64px;
            padding: 0px 2.5rem;
            background-color: #c9c8c6;
            color:black;
            width:13rem;
            font-weight: bold;
            border-radius:2rem;
            text-align-last: end;
            align-self: self-end;
            margin-bottom: 3px;
        }
        .line {
            border: none;
            border-top: 5px solid white;
            margin: 1rem 2rem;
            padding:2px;
            width:450px;
            color:white;
            position: absolute;
            bottom: 110px;
          }
          .players{
            width:70px;
            height:70px;
            border-radius:50px;
            background-color: rgba(255, 255, 255, .1);
            filter: drop-shadow(0px 20px 10px rgba(0, 0, 0, 0.3));
            border: 3px solid white;
            margin: 0px 2px;
          }
          .players1{
            width:167px;
            height:167px;
            border-radius:50%;
            background-color: rgba(255, 255, 255, .1);
            filter: drop-shadow(0px 20px 10px rgba(0, 0, 0, 0.3));
            border: 5px solid white;
            margin: 0px 14px;
          }
          .playerlist{
            position: absolute;
            bottom: 234px;
          }
          .mainplayers{
            position: absolute;
            bottom: 420px;
          }
          .challenger{
            display: flex;
            flex-direction: column;
            align-items: center;
            color: white;
            font-size: 3rem;
            position: absolute;
            bottom: 335px;
            }
            .bottom{
                position: absolute;
                bottom: 31px;
            }
    </style>
</head>
<body>
    <div class="container">
        <div class="frame">
            <div class="mainplayers">
                <img class="players1" src='"""+rankIcon+"""'>
                <img class="players1" src='"""+opponentIcon+"""'/>
            </div>
            <div class="challenger">
                <p>"""+rank+"""</p>
            </div>
            <div class="playerlist">
                <img class="players" src='../assets/img/"""+region+""".png'/>
                <img class="players" src='"""+spellImg[0]+"""'/>
                <img class="players" src='../assets/img/spell/"""+spellImg[1]+"""'/>
                <img class="players" src='../assets/img/spell/"""+spellImg[2]+"""'/>
            </div>
            <div class="match">
                <p class="mvp">"""+mvp+"""</p>
            </div>
            <hr class="line"/>
            <div class="bottom" style='display:flex'>
                <p class="kdatext">KDA</p>
                <p >
                    <p class="kda">"""+kda[0]+"""</p>
                    <p class="kda">"""+kda[1]+"""</p>
                    <p class="kda">"""+kda[2]+"""</p>
                </p>
            </div>
        </div>
        <div class="patch">
            <p>"""+patch+"""</p>
        </div>


    </div>
</body>
</html>
"""
        with open("./assets/thumbnail.html", "w",encoding='utf-8') as f:
            f.write(HTML)

if __name__ ==  "__main__":
    from usecases.data import load
    lol_data: MatchData = load()
    thumb_creator = CreateThumbnail(data_scrapper=DataScrapper(), data=lol_data)
    thumb_creator.create_thumbnail()