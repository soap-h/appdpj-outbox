class Product:
    count_id = 0

    def __init__(self, name, price, category, remarks, drinks):
        Product.count_id += 1
        self.__product_id = Product.count_id
        self.__name = name
        self.__price = price
        self.__category = category
        self.__remarks = remarks
        self.__drinks = drinks

    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_category(self):
        return self.__category

    def get_remarks(self):
        return self.__remarks

    def get_drinks(self):
        return self.__drinks

    def set_name(self, name):
        self.__name = name

    def set_price(self, price):
        self.__price = price

    def set_category(self, category):
        self.__category = category

    def set_remarks(self, remarks):
        self.__remarks = remarks

    def set_drinks(self, drinks):
        self.__drinks = drinks

