class Hash40:
    def __init__(self, hash40, tag = None):
        self.hash40 = hash40
        self.length = int(hash40, 16) >> 32
        self.hash = hex(int(hash40, 16) & 0xffffffff)
        self.tag = tag

    @staticmethod
    def Create(hash, length):
        return Hash40(hex(length) + hash[2:])