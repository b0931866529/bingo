from typeguard import typechecked
from abc import ABC, abstractmethod


class IAccountDao(ABC):
    @abstractmethod
    def GetPassword(self, id: str) -> str:
        pass


class AccountDao(IAccountDao):
    @typechecked
    def GetPassword(self, id: str) -> str:
        return 'pass'


class IHash(ABC):
    @abstractmethod
    def GetHashResult(self, passwordByDao: str) -> str:
        pass


class Hash:
    @typechecked
    def GetHashResult(self, passwordByDao: str) -> str:
        return 'hash'


class Validation:
    def __init__(self, accountDao: IAccountDao, hash: IHash):
        self.__accountDao = accountDao
        self.__hash = hash

    @typechecked
    def CheckAuthentication(self, id: str,  password: str) -> bool:
        # 取得資料中，id對應的密碼
        passwordByDao = self.__accountDao.GetPassword(id)

        # 針對傳入的password，進行hash運算
        hashResult = self.__hash.GetHashResult(password)

        # 比對hash後的密碼，與資料中的密碼是否吻合
        return passwordByDao == hashResult


if __name__ == '__main__':
    accountDao = AccountDao()
    hash = Hash()
    target = Validation(accountDao, hash)
    id = ''
    password = ''
    actual = target.CheckAuthentication(id, password)
    print("")
