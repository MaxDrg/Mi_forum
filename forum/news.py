from posixpath import split

class News():
    def __init__(self, title, info, pre_info, hashtags, date, image) -> None:
        self.title = title
        self.info = info
        self.pre_info = pre_info
        self.hashtags = split(hashtags)
        self.date = date
        self.image = image