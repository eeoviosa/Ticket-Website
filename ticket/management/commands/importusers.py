from django.core.management.base import BaseCommand
from csv import reader
from django.contrib.auth.models import User

class Command(BaseCommand):
    help= 'imports user from directories csv file'

    def add_arguments(self, parser):
        parser.add_argument('file_directory', type = str)

    def handle(self, *args, **kwargs):

        with open(kwargs['file_directory'], 'r') as csv_file:
            read = reader(csv_file)
            _ = next(read)
            __ = next(read)

            for user in read:
                firstname = user[2]
                lastname = user[1]
                email = user[13]
                lis = email.split('@')
                username = lis[0]
                id = user[0]
                password = "Txwe$" + str(id)
                if User.objects.filter(username=username).exists():
                     self.stdout.write('Username "%s" already exists' %username)
                else:
                    user = User(username=username)
                    user.first_name = firstname
                    user.set_password(password)
                    user.last_name = lastname
                    user.email = email
                    user.save()
                    user = User.objects.get(username = username)
                    user.student.sid = id
                    user.save()
                    self.stdout.write("User Created Succesfully")



