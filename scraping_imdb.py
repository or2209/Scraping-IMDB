from bs4 import BeautifulSoup
import requests, openpyxl
from tkinter import *

class scraping:

    val =""
    genres = ["Action", "Adult", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Documentary", "Drama", "Family",
          "Fantasy", "Film Noir", "Game Show", "History", "Horror", "Musical", "Music", "Mystery", "News", "Reality-TV",
          "Romance", "Sci-Fi", "Short", "Sport", "Talk-Show", "Thriller", "War", "Western"]
    MPAA_rating=["MPAA - G","PG-13","PG","R","NC-17"]

    def __init__(self):
        self.output=""

    def checkIfGenre(self,name):
        if name in self.genres:
            return True
        return False

    def checkIfMpaa(self,name):
        for rating in self.MPAA_rating:
            if rating in name:
                return rating
        return False


    def getGenreAndMpaa(self,soup1):
        flag_comma=True
        flag_mpaa=False
        geners = soup1.find('ul',
                        class_="ipc-metadata-list ipc-metadata-list--dividers-all Storyline__StorylineMetaDataList-sc-1b58ttw-1 esngIX ipc-metadata-list--base").text
        # genre=soup1.findAll('li', {'data-testid': 'storyline-genres'})
        for ultag in soup1.find_all('ul', {
        'class': 'ipc-metadata-list ipc-metadata-list--dividers-all Storyline__StorylineMetaDataList-sc-1b58ttw-1 esngIX ipc-metadata-list--base'}):

            for litag in ultag.find_all('li'):

                for litag2 in litag.find_all('li'):
                    # print(litag2.text + "fdfddf")
                    if (self.checkIfGenre(litag2.text)) == True:
                        if flag_comma!=True:
                            self.output += ','
                        flag_comma=False
                        self.output += litag2.text
                    mpaa=self.checkIfMpaa(litag2.text)
                    if mpaa != False:
                        flag_mpaa=True
                        if flag_comma==True:
                            self.output+='empty field'
                            self.output += "|"
                        self.output += "|"
                        self.output += mpaa
                        self.output += '|'
        if flag_mpaa==False:
            self.output += '|'
            self.output += 'empty field'
            self.output += "|"

        self.getDuration(soup1)



    def getDuration(self, soup1):
        flag=True
        for ultag in soup1.find_all('ul', {
        'class': 'ipc-inline-list ipc-inline-list--show-dividers TitleBlockMetaData__MetaDataList-sc-12ein40-0 dxizHm baseAlt'}):

            for litag in ultag.find_all('li'):
                if 'h' in litag.text and 'm' in litag.text:
                    flag=False
                    self.output+=litag.text
                    self.output+='|'
            if flag==True:
                self.output +='empty field'
                self.output+='|'

            self.getDirectors(soup1)

    def getDirectors(self,soup1):
        flag=False
        list_directors=[]
        for ultag in soup1.find_all('ul', {
        'class': 'ipc-metadata-list ipc-metadata-list--dividers-all title-pc-list ipc-metadata-list--baseAlt'}):

            for litag in ultag.find_all('li'):
                if 'Director' in litag.text:
                    flag=True
                if 'Writers' in litag.text or 'Stars' in litag.text:
                    flag=False
                for litag2 in litag.find_all('ul'):
                    for litag3 in litag2.find_all('a'):
                        if flag==True:
                            list_directors.append(litag3.text)
        list_directors = list(dict.fromkeys(list_directors))
        length_list=len(list_directors)
        for count, value in enumerate(list_directors):
            if count==length_list-1:
                self.output += value + '|'
            else:
                self.output+=value+','
        if len(list_directors) == 0:
            self.output += 'empty field'
            self.output += '|'

        self.getStars(soup1)



    def getStars(self, soup1):
        flag=False
        list_Stars = []
        for ultag in soup1.find_all('ul', {
            'class': 'ipc-metadata-list ipc-metadata-list--dividers-all title-pc-list ipc-metadata-list--baseAlt'}):

            for litag in ultag.find_all('li'):
                # print(litag)
                if 'Stars' in litag.text:
                    flag = True
                else:
                    flag=False
                for litag2 in litag.find_all('ul'):
                    for litag3 in litag2.find_all('a'):
                        if flag == True:
                            list_Stars.append(litag3.text)

        list_Stars = list(dict.fromkeys(list_Stars))
        if 'Stars' in list_Stars:
            list_Stars.remove('Stars')
        if 'Star' in list_Stars:
            list_Stars.remove('Star')
        length_list = len(list_Stars)
        for count, value in enumerate(list_Stars):
            if count == length_list - 1:
                self.output += value
            else:
                self.output += value + ','
        if len(list_Stars) == 0:
            self.output += 'empty field'

    def ceckDevelopmentPhase(self,soup1):
        div = soup1.find_all('div', attrs={'class': 'SubNav__SubNavContent-sc-11106ua-3 cKmYsV'})
        for tag in div:
            if 'In development' in tag.text:
                return True
        return False

    def createGui(self):

        def submit():
            self.val = entry.get()  # gets entry text
            window.destroy()

        def delete():
            entry.delete(0, END)  # deletes the line of text

        def backspace():
            entry.delete(len(entry.get()) - 1, END)  # delete last character

        window = Tk()
        window.title("user input")
        label = Label(window, text="movie name: ")
        label.config(font=("Consolas", 30))
        label.pack(side=LEFT)
        submit = Button(window, text="submit", command=submit)
        submit.pack(side=RIGHT)
        delete = Button(window, text="delete", command=delete)
        delete.pack(side=RIGHT)
        backspace = Button(window, text="backspace", command=backspace)
        backspace.pack(side=RIGHT)

        entry = Entry()
        entry.config(font=('Ink Free', 50))  # change font
        entry.config(bg='#111111')  # background
        entry.config(fg='#00FF00')  # foreground
        entry.config(width=10)  # width displayed in characters
        entry.pack()
        window.mainloop()
        self.start()

    def start(self):
        try:
            f = open("output_file.txt", "w")
            source = requests.get("https://www.imdb.com/find?q=" + (self.val) + '&ref_=nv_sr_sm')
            source.raise_for_status()

            soup = BeautifulSoup(source.text, 'html.parser')

            movies = soup.find('div', class_="findSection").find_all('tr')

            for movie in movies:

                link = movie.find('td', class_="result_text").find("a").get("href")

                source1=requests.get("https://www.imdb.com" + link)

                source1.raise_for_status()
                soup1 = BeautifulSoup(source1.text, 'html.parser')

                #check if movie title are in the development phase
                development_phase=self.ceckDevelopmentPhase(soup1)

                if development_phase==False:

                    print("\n")
                    name = soup1.find('div', class_="TitleBlock__TitleContainer-sc-1nlhx7j-1 jxsVNt").h1.text
                    self.output += name + '|'
                    self.getGenreAndMpaa(soup1)

                print(self.output)
                f.write(self.output)
                f.write("\n")
                self.output=""

        except Exception as e:
            print(e)

        f.close()


scrape=scraping()
scrape.createGui()