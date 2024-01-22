class Voucher:
    def __init__(self, voucher_id, name, discount):
        self.__id = voucher_id
        self.__name = name
        self.__discount = discount

    def get_voucher_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_discount(self):
        return self.__discount

    def set_voucher_id(self, voucher_id):
        self.__id = voucher_id

    def set_name(self, name):
        self.__name = name

    def set_discount(self, discount):
        self.__discount = discount
