import json
import logging as logging
from dataclasses import dataclass
from re import split

POST_PATH = "posts.json"
# допустимые расширения для загружаемого файла
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
logging.basicConfig(filename="log.log", level=logging.INFO)

class MyException(Exception):
    pass


@dataclass
class PostsManager:
    """
    класс для работы с постами
    """
    file_json: str
    data_json: list = None

    def __post_init__(self):
        """
        загружает данные из JSON
        :return:
        """
        try:
            with open(self.file_json, encoding='utf-8') as file:
                self.data_json = json.load(file)
        except FileNotFoundError:
            raise MyException("Файл json не найден!")
        except json.JSONDecodeError:
            raise MyException("Проблемы с json файлом!")

    def get_post(self, s):
        """
        ищет посты по критерию
        :param s:
        :return:
        """
        posts = []
        hash_tags = split(',| ', s)
        for post in self.data_json:
            for hash_tag in hash_tags:
                if hash_tag.lower() in post["content"].lower():
                    posts.append(post)
        return posts

    def add_post(self, data):
        """
        добавляет посты в файл json
        :param data:
        :return:
        """
        self.data_json.append(data)
        try:
            with open(self.file_json, "w", encoding='utf-8') as file:
                json.dump(self.data_json, file, ensure_ascii=False)
                logging.info("Дынные в JSON добавлены")
        except json.JSONDecodeError:
            raise MyException('Не удалось сохранить json файл')


try:
    posts = PostsManager(POST_PATH)
except MyException as exc:
    logging.error(exc)


def allowed_extension(filename):
    """
    проверяет соответствует ли загружаемый файл необходимым параметрам
    :param filename:
    :return:
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
