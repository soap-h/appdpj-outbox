class Supplier:
    count_id = 0
    def __init__(self, company_name, company_email, company_phone, company_address, password):
        Supplier.count_id += 1
        self.__supplier_id = Supplier.count_id
        self.__company_name = company_name
        self.__company_email = company_email
        self.__company_phone = company_phone
        self.__company_address = company_address
        self.__password = password

    def as_dict(self):
        return {'Supplier ID': self.__supplier_id, 'Company name': self.__company_name, 'Company email': self.__company_email,
                'Company Phone': self.__company_phone, 'Company Address': self.__company_address, 'Password': self.__password}
    def get_supplier_id(self):
        return self.__supplier_id

    def get_company_name(self):
        return self.__company_name

    def get_company_email(self):
        return self.__company_email

    def get_company_phone(self):
        return self.__company_phone

    def get_company_address(self):
        return self.__company_address

    def get_password(self):
        return self.__password


    def set_supplier_id(self, supplier_id):
        self.__supplier_id = supplier_id

    def set_company_name(self, company_name):
        self.__company_name = company_name

    def set_company_email(self, company_email):
        self.__company_email = company_email

    def set_company_phone(self, company_phone):
        self.__company_phone = company_phone

    def set_company_address(self, company_address):
        self.__company_address = company_address

    def set_password(self, password):
        self.__password = password