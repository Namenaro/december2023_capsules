
class IdGenedator:
    def __init__(self, prefix=None):
        self.prefix = prefix
        self.i =- 1

    def get_id(self):
        self.i +=1

        if self.prefix is None:
            return self.i
        return self.prefix + str(self.i)
