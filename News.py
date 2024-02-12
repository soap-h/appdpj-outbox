class News():
    comment_count = 0
    count_id = 0

    def __init__(self, title, description, date_posted, file):
        News.count_id += 1
        self.__title = title
        self.__description = description
        self.__date_posted = date_posted
        self.__file = file
        self.__news_id = News.count_id
        self.__comments = []

    def get_title(self):
        return self.__title

    def get_description(self):
        return self.__description

    def get_date_posted(self):
        return self.__date_posted

    def get_nid(self):
        return self.__news_id

    def get_file(self):
        return self.__file

    def set_title(self, title):
        self.__title = title

    def set_description(self, des):
        self.__description = des

    def set_date_posted(self, dp):
        self.__date_posted = dp

    def set_nid(self, nid):
        self.__news_id = nid

    def set_file(self, file):
        self.__file = file


    def add_comment(self, comment):
        self.__comments.append(comment)

    def get_comments(self):
        return self.__comments

    def __str__(self):
        return f"{self.__title}, {self.__description}, {self.__date_posted}, {self.__comments}"



class Comment():
    def __init__(self, text):
        self.__text = text
        self.__comid = int

    def get_comid(self):
        return self.__comid

    def get_text(self):
        return self.__text

    def set_text(self, text):
        self.__text = text

