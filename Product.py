class Product:
    products = []
    count_id = 0

    def __init__(self, name, price, category, remarks, drinks, image):
        Product.count_id += 1
        self.__product_id = Product.count_id
        self.__name = name
        self.__price = price
        self.__category = category
        self.__remarks = remarks
        self.__drinks = drinks
        self.__image = image

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

    def get_image(self):
        return self.__image

    def set_product_id(self, id):
        self.__product_id = id

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

    def set_image(self, image):
        self.__image = image


def filter_by_category(cls, category_id):
    return [product for product in cls.products if product.get_category() == category_id]