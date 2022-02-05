import requests
TESTING_URL ='http://127.0.0.1:5001/'


"""
    def getMyGames(self):
        return self.my_games

    def setMyGames(self,my_games):
        self.my_games = my_games

    def getPlayingGames(self):
        return self.playing_games

    def setPlayingGames(self,playing_games):
        self.playing_games = playing_games
"""
class User:
    def __init__(self,name,email,isAdmin):
        self.userName= name
        self.userEmail=email
        #self.my_games = games
        #self.playing_games = playing_games
        self.isAdmin = isAdmin

    def getUserName(self):
        return self.userName

    def setUserName(self,name):
        self.userName = name

    def getEmail(self):
        return self.userEmail

    def setEmail(self,email):
        self.userEmail = email

    def setIsAdmin(self, isAdmin):
        self.isAdmin = isAdmin

    def disconnect(self):
        self.setEmail("")
        self.setUserName("")
        #self.setMyGames([])
        #self.setPlayingGames([])
        self.setIsAdmin(False)

class Image:
    def __init__(self,i,name,date,dateProc,imageB):
        self.index = i
        self.imageName = name
        self.imageDate = date
        self.imageDateProc = dateProc
        self.imageBytes = imageB
    def getName(self):
        return self.imageName
    def getDate(self):
        return self.imageDate
    def getDateProc(self):
        return self.imageDateProc
    def getImageBytes(self):
        return self.imageBytes
    def getIndex(self):
        return self.index
    def setName(self,name):
        self.imageName = name
    def setDate(self,date):
        self.imageDate = date
    def setDateProc(self,dateProc):
        self.imageDateProc = dateProc
    def setImageBytes(self,iB):
        self.imageBytes = iB
    def setIndex(self,i):
        self.index = i
