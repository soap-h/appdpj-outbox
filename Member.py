class Member:
    count_id = 0

    def __init__(self, firstname, lastname, email, phone, password):
        Member.count_id += 1
        self.__member_id = Member.count_id
        self.__first_name = firstname
        self.__last_name = lastname
        self.__email = email
        self.__phone = phone
        self.__password = password

    def get_member_id(self):
        return self.__member_id

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_email(self):
        return self.__email

    def get_phone(self):
        return self.__phone

    def get_password(self):
        return self.__password

    def set_member_id(self, member_id):
        self.__member_id = member_id

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_email(self, email):
        self.__email = email

    def set_phone(self, phone):
        self.__phone = phone

    def set_password(self, password):
        self.__password = password

# can you see this
