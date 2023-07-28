from ..models import User

# 디자인 패턴에 따르면 어떤 객체안에 다른 객체의 메소드를 쓰는 방법을 쓰는게 좋다한다.

class CRUD:
    def __init__(self, data):
        self.data = data

    def create(self):
        pass


    def read(self):
        pass


    def update(self):
        pass


    def delete(self):
        pass


class CrudUser(CRUD):
    def __init__(self, data):
        super().__init__(data)


    # {userid: 'seong960603', 
    # nickname: '김성동', 
    # password: '5162!kim', 
    # passwordCheck: '5162!kim', 
    # email: '3930648@naver.com', …}

    def create(self):
        print(self.data)
        self.userid = self.data.get('userid')
        self.nickname = self.data.get('nickname')
        self.password = self.data.get('password')
        self.phone = self.data.get('phone')
        self.email = self.data.get('email')

        user = User(
            userid=self.userid,
            nickname=self.nickname,
            phone=self.phone,
            email=self.email
        )
        user.set_password(self.password)
        user.save()

        return f"{self.nickname} 유저 등록이 완료되었습니다."


    # 예를들어
    def read(self):
        print(self.data)



# 다음과 같이 아키텍처 설계를 해볼까?

# from abc import ABC, abstractmethod

# class CrudOperation(ABC):
#     def __init__(self, data):
#         self.data = data

#     @abstractmethod
#     def create(self):
#         pass

#     @abstractmethod
#     def read(self):
#         pass

#     @abstractmethod
#     def update(self):
#         pass

#     @abstractmethod
#     def delete(self):
#         pass


# class UserCrudOperation(CrudOperation):
#     def create(self):
#         # User specific creation logic
#         pass

#     def read(self):
#         # User specific read logic
#         pass

#     def update(self):
#         # User specific update logic
#         pass

#     def delete(self):
#         # User specific deletion logic
#         pass

# # Repeat the similar classes for other tables


# class CrudOperationFactory:
#     @staticmethod
#     def get_crud_operation(data, table):
#         if table == 'User':
#             return UserCrudOperation(data)
#         # elif table == 'OtherTable':
#         #     return OtherTableCrudOperation(data)
#         else:
#             raise ValueError("Invalid table.")
