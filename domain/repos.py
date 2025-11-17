from abc import abstractmethod

class UsersRepo:
    
    @abstractmethod
    def save(self, user):...
        
    @abstractmethod
    def find_all(self):...
    
    @abstractmethod
    def find_by_field(self, field, value):...
    