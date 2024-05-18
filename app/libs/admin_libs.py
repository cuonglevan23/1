
class Admin_Libs():
    def __init__(self, name=None,gender=None, mobile=None, email=None,
                 address=None, password=None, status=None):
        self.name=name
        self.gender=gender
        self.mobile=mobile
        self.email=email
        self.address=address
        self.password=password
        self.status=status

    def getName(self):
        return self.name
    def getGender(self):
        return self.gender

    def getMobile(self):
        return self.mobile

    def getEmail(self):
        return self.email

    def getAddress(self):
        return self.address

    def getPassword(self):
        return self.password

    def getStatus(self):
        return self.status



    def setName(self, name):
        self.name=name
    def setGender(self, gender):
        self.gender=gender

    def setMobile(self, mobile):
        self.mobile=mobile

    def setEmail(self, email):
        self.email=email

    def setAddress(self, address):
        self.address=address

    def setPassword(self, password):
        self.password=password
    def setStatus(self, status):
        self.status=status

    def __str__(self):
        return ('{},{},{},{},{},{},{},{},{},{}'.format( self.name, self.gender, self.mobile, self.email, self.address, self.password,  self.status))