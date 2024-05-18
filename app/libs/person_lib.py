class Person_Libs():
    def __init__(self,id=None, name=None,mobile=None, address=None,position=None):
        self.id=id
        self.name=name
        self.mobile=mobile
        self.address=address
        self.position=position


    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getMobile(self):
        return self.mobile
    def getAddress(self):
        return self.address
    def getPosition(self):
        return self.position


    def setId(self, id):
        self.id=id
    def setName(self, name):
        self.name=name
    def setMobile(self, mobile):
        self.mobile=mobile
    def setAddress(self, address):
        self.address=address

    def setPosition(self, position):
        self.position=position

    def __str__(self):
      return ('{},{},{},{},{}'.format( self.id, self.name, self.mobile, self.address, self.position))