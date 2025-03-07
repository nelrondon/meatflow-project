import bcrypt, sys
from handledb import DB

class UserNotFound(Exception):
    pass
class AuthFail(Exception):
    pass
class UserExist(Exception):
    pass

class Auth:
    @staticmethod
    def createUser(user, pw):
        module = "auth_data"

        if DB.exists(module):
            userDB = DB.getOneBy(module, "user", user)
            if userDB: 
                raise UserExist("El usuario ya se encuentra registrado")

        passw = pw.encode("utf-8")
        salt = bcrypt.gensalt()
        passwHashed = bcrypt.hashpw(passw, salt)

        user = {"user": user, "password": passwHashed.decode("utf-8")}
        return DB.save(module, user)

class AuthUser:
    def __init__(self, user):
        self.user = user
        self.__isLogin = False

    @property
    def isLogin(self):
        return self.__isLogin
    
    def login(self, pw):
        passw = pw.encode("utf-8")
        module = "auth_data"
        userDB = DB.getOneBy(module, "user", self.user)
        if not userDB:
            self.__isLogin = False
            raise UserNotFound("No se ha encontrado el usuario")
        else:
            passwHashed = userDB["password"].encode("utf-8")
            self.__isLogin = bcrypt.checkpw(passw, passwHashed)

        if not self.__isLogin: raise AuthFail("Contraceña o usuario no coincide")
        return self.__isLogin
    
    def logout(self):
        self.__isLogin = False

if len(sys.argv) > 1:
    if sys.argv[1] == "create":
        user = input("Ingresa el usuario: ")
        passw = input("Ingresa la contraceña: ")
        Auth.createUser(user, passw)