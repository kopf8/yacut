from datetime import datetime

from settings import Constants

from yacut import db


class URLMap(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True)
    original = db.Column(db.String(Constants.ORIG_URL_MAX_LEN),
                         nullable=False)
    short = db.Column(db.String(Constants.SHORT_URL_MAX_LEN),
                      unique=True,
                      nullable=False)
    timestamp = db.Column(db.DateTime,
                          index=True,
                          default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=self.short
        )

    def from_dict(self, data):
        for field in Constants.API_DICT:
            if field in data:
                setattr(self, Constants.API_DICT[field], data[field])

    def __str__(self):
        return (f'Короткая ссылка: {self.short}, '
                f'Оригинальная длинная ссылка: '
                f'{self.original[Constants.ORIG_URL_STR_LEN]})')
