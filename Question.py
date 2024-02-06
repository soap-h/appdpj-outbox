class Question:
    count_id = 0

    def __init__(self, email, title, question, date_posted, overall, feedback,reply):
        Question.count_id += 1  # Increment the class-level count_id
        self.__email = email
        self.__title = title
        self.__question = question
        self.__date_posted = date_posted
        self.__question_id = Question.count_id

        #######################
        self.__overall = overall
        self.__feedback = feedback
        self.__reply = reply
        #######################

    def as_dict(self):
        return {'Question ID': self.__question_id, 'Email': self.__email, 'Title': self.__title,
                'Question': self.__question, 'Date posted': self.__date_posted,
                'Overall rating': self.__overall, 'Written feedback': self.__feedback}

    def get_question_id(self):
        return self.__question_id

    def get_email(self):
        return self.__email

    def get_date_posted(self):
        return self.__date_posted

    def get_title(self):
        return self.__title

    def get_question(self):
        return self.__question

    #######################
    def get_overall(self):
        return self.__overall

    def get_feedback(self):
        return self.__feedback

     def get_reply(self):
        return self.__reply

    #######################

    def set_question_id(self, question_id):
        self.__question_id = question_id

    def set_email(self, email):
        self.__email = email

    def set_title(self, title):
        self.__title = title

    def set_question(self, question):
        self.__question = question

    #######################
    def set_overall(self, overall):
        self.__overall = overall

    def set_feedback(self, feedback):
        self.__feedback = feedback

    def set_reply(self, reply):
    self.__reply = reply
    #######################

    def __str__(self):
        return f"{self.__question_id}, {self.__title}, {self.__question}, {self.__date_posted}, {type(self.__date_posted)}, {self.__overall}, {type(self.__overall)}"
