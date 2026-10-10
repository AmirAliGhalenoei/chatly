from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone, username, email=None, password=None):
        if not phone:
            raise ValueError("Error Phone")

        if not username:
            raise ValueError("Error Username")

        user = self.model(phone=phone, username=username)
        if email:
            user.email = self.normalize_email(email)

        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, username, email=None, password=None):
        if not phone:
            raise ValueError("Error Phone")

        if not username:
            raise ValueError("Error Username")

        if not password:
            raise ValueError("Superuser must have password")

        user = self.model(phone=phone, username=username)
        if email:
            user.email = self.normalize_email(email)

        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user