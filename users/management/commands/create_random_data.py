import random
import string
from django.core.management.base import BaseCommand
from faker import Faker
from users.models import User
from organizations.models import Organization

fake = Faker('ru_RU')  # Используем локаль для русскоязычных данных

class Command(BaseCommand):
    help = 'Создает случайные организации и пользователей'

    def add_arguments(self, parser):
        parser.add_argument(
            '--organizations',
            type=int,
            default=10,
            help='Количество создаваемых организаций (по умолчанию 10)'
        )
        parser.add_argument(
            '--users',
            type=int,
            default=50,
            help='Количество создаваемых пользователей (по умолчанию 50)'
        )

    def handle(self, *args, **options):
        org_count = options['organizations']
        user_count = options['users']

        self.stdout.write(self.style.WARNING(f'Создание {org_count} организаций...'))
        organizations = []
        for _ in range(org_count):
            org = Organization.objects.create(
                name=fake.company(),
                description=fake.text(max_nb_chars=200)
            )
            organizations.append(org)
        self.stdout.write(self.style.SUCCESS(f'Создано {org_count} организаций.'))

        self.stdout.write(self.style.WARNING(f'Создание {user_count} пользователей...'))
        users = []
        for _ in range(user_count):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.unique.email()
            phone = fake.unique.phone_number()
            password = self.generate_random_password()

            user = User.objects.create(
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                is_active=True,
                is_staff=False
            )
            user.set_password(password)  # Рекомендуется использовать хешированные пароли
            user.save()
            users.append((user, password))  # Сохраняем пароль для вывода

        # Назначаем пользователям организации
        for user, _ in users:
            orgs = random.sample(organizations, random.randint(0, 3))  # От 0 до 3 организаций
            user.organizations.set(orgs)
            user.save()

        self.stdout.write(self.style.SUCCESS(f'Создано {user_count} пользователей.'))

        # Выводим созданных пользователей и их пароли
        self.stdout.write(self.style.SUCCESS('Сгенерированные пользователи:'))
        for user, password in users:
            org_names = ', '.join([org.name for org in user.organizations.all()]) or 'Нет организаций'
            self.stdout.write(f'Email: {user.email}, Пароль: {password}, Организации: {org_names}')

    def generate_random_password(self, length=12):
        """Генерирует случайный пароль."""
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        return password
