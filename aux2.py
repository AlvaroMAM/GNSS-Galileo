class User:
    def __init__(self,name,email,isAdmin,playing_games, my_games):
        self.userName= name
        self.userEmail=email
        self.juegosParticipados = playing_games
        self.misJuegos = my_games
        self.isAdmin = isAdmin

    def getUserName(self):
        return self.userName

    def setUserName(self,name):
        self.userName = name

    def getEmail(self):
        return self.userEmail

    def setEmail(self,email):
        self.userEmail = email
    
    def setJuegosParticipados(self,juegos):
        self.juegosParticipados = juegos
    
    def getJuegosParticipados(self):
        return self.juegosParticipados
    
    def setMisJuegos(self, mygames):
        self.misJuegos = mygames
    
    def getMisJuegos(self):
        return self.misJuegos

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
