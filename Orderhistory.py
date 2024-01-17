class OrderHistory:
    count_id = 0
    def __init__(self, name, email, products, date, number, payment_amt):
        OrderHistory.count_id += 1
        self.__orderid = OrderHistory.count_id
        self.__name = name
        self.__email = email
        self.__products = products
        self.__date = date
        self.__number = number
        self.__payment_amt = payment_amt

    def get_order_id(self):
        return self.__orderid

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_products(self):
        return self.__products

    def get_date(self):
        return self.__date

    def get_number(self):
        return self.__number

    def get_payment_amt(self):
        return self.__payment_amt

    def set_order_id(self, id):
        self.__orderid = id

    def set_name(self, name):
        self.__name = name

    def set_email(self, email):
        self.__email = email

    def set_products(self, products):
        self.__products = products

    def set_date(self, date):
        self.__date = date

    def set_payment_amt(self, payment_amt):
        self.__payment_amt = payment_amt