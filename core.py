# coding=utf-8

import os
import json
import time
import hashlib


class MockIt:
    """
    Как использовать:
        from mockitto import MockIt
        mock_db = MockIt(os.path.abspath("."))
        декоратор - @mock_db.mock
    """

    def __init__(self, path, active=True, file_name=None):
        """
        :param active: включен ли по умолчанию декоратор
        """

        self.path = path
        self.active = active
        if not file_name:
            self.file_name = os.path.join(
                self.path, "%s.json" % time.strftime('%d_%m_%Y'))
        else:
            self.file_name = file_name

    def get_data(self, data_id):
        """
        :param data_id:
        :return:
        """

        try:
            with open(self.file_name, 'r') as f:
                data = f.read().encode('utf-8')
            records = json.loads(data).get(data_id)
        except Exception as err:
            # TODO:
            records = dict()
        return records

    def save_data(self, data, data_id):
        """
        :param data:
        :param data_id:
        :return:
        """

        new_data = dict()

        try:
            if os.path.isfile(self.file_name):
                with open(self.file_name, "r") as f:
                    new_data = json.loads(f.read())
        except ValueError:
            pass

        new_data[data_id] = data

        with open(self.file_name, "w") as f:
            f.write(json.dumps(new_data))

    def mock(self, many=False):
        """
        :param many: множество вариантов ответа
        :return:
        """

        def decorator(func):
            def wrapper(*args, **kwargs):

                if many:
                    hash_data = json.dumps(kwargs)
                    hash_str = str('_'.join(hash_data)) + '_' + func.__name__
                    data_id = hashlib.md5(hash_str.encode('utf-8')).hexdigest()
                else:
                    data_id = func.__name__

                records = self.get_data(data_id)

                if self.active:
                    if not records:
                        data = func(*args, **kwargs)
                        self.save_data(data, data_id)
                    else:
                        return records

                return func(*args, **kwargs)

            return wrapper

        return decorator
