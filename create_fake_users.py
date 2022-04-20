import datetime
import random
from app import db, User


def random_name():
    letters_count = 7
    alphabet = "qwertyuiopasdfghjklzxcvbnm"
    result = ""
    for _ in range(letters_count):
        index = random.randint(0, len(alphabet) - 1)
        result += alphabet[index]
    result += str(random.randint(1000, 9999))
    return result


def create_fake_users(n):
    for i in range(n):
        user = User(date=datetime.date.today(),
                    name=random_name(),
                    count=random.randint(1, 50),
                    distance=random.randint(0, 100) * 1.5
                    )
        db.session.add(user)
    db.session.commit()
    print(f'{n} случайных данных добавлено.')


if __name__ == '__main__':
    create_fake_users(100)
