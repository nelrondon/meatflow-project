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
    def createUser(name, user, pw):
        module = "auth_data"

        if DB.exists(module):
            userDB = DB.getOneBy(module, "user", user)
            if userDB: 
                raise UserExist("El usuario ya se encuentra registrado")

        passw = pw.encode("utf-8")
        salt = bcrypt.gensalt()
        passwHashed = bcrypt.hashpw(passw, salt)

        user = {
            "name": name,
            "user": user, 
            "password": passwHashed.decode("utf-8")}
        return DB.save(module, user)
    
    @staticmethod
    def changePassw(user, newpw):
        module = "auth_data"
        newpw = newpw.encode("utf-8")
        salt = bcrypt.gensalt()
        newpwHashed = bcrypt.hashpw(newpw, salt)


        DB.update(module, "user", user, {"password": newpwHashed.decode("utf-8")})
        return True        

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
        return userDB
    
    def logout(self):
        self.__isLogin = False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "create":
            name = input("Ingresa el nombre: ")
            user = input("Ingresa el usuario: ")
            passw = input("Ingresa la contraceña: ")
            try:
                Auth.createUser(name, user, passw)
            except Exception as e:
                print(e)