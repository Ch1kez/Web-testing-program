from django.db import models


class Mail(models.Model):
    tmail = models.CharField(max_length=255)

    def __str__(self):
        return self.tmail


class Target(models.Model):
    tname = models.CharField(max_length=255)
    madr = models.CharField(max_length=255)
    dadr = models.CharField(max_length=255)
    rem = models.CharField(max_length=255)

    def __str__(self):
        return self.tname


# На будущее:
# class Tester(models.Model):
#     tester_name = models.CharField(max_length=255)
#
#     def __str__(self):
#         return self.tester_name


class Test(models.Model):
    id = models.IntegerField(primary_key=True)
    test_name = models.CharField(max_length=255)
    test_text = models.TextField()  # Может потребоваться изменить тип поля
    test_grp = models.CharField(max_length=255)

    # tester = models.ForeignKey(Tester, on_delete=models.CASCADE)

    def __str__(self):
        return self.test_name


class Tuser(models.Model):
    target = models.CharField(max_length=255)
    ulogin = models.CharField(max_length=255)
    upass = models.CharField(max_length=255)
    uorg = models.CharField(max_length=255)

    def __str__(self):
        return self.target


class WebsiteTable(models.Model):
    url = models.URLField()
    # Добавьте другие поля по необходимости
