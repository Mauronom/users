from hex.users.domain import UsersRepo

class MemoryUsersRepo(UsersRepo):
    def __init__(self, init_users):
        self.users = init_users

    def save(self, user):
        self.users.append(user.clone())

    def find_all(self):
        res = []
        for u in self.users:
            res.append(u.clone())
        return res

    def find_by_field(self, field, value):
        res = []
        for u in self.users:
            if (getattr(u, field) == value):
                res.append(u)
        return res
    
class DjangoUsersRepo(UsersRepo):

    def save(self, user):
        from django.contrib.auth import get_user_model
        from users.models import Profile as DjangoProfile
        DjangoUser = get_user_model()
        django_user, _ = DjangoUser.objects.update_or_create(
            username=user.username,
            defaults={"email": user.email},
        )

        profile, _ = DjangoProfile.objects.update_or_create(
            user=django_user,
            defaults={
                "uuid": user.uuid,
                "dni": user.dni,
            },
        )

        return self._to_domain(django_user, profile)

    def find_all(self):
        from django.contrib.auth import get_user_model
        DjangoUser = get_user_model()
        users = DjangoUser.objects.select_related("profile").all().exclude(username='admin')
        return [self._to_domain(u, u.profile) for u in users]

    def find_by_field(self, field, value):
        from django.contrib.auth import get_user_model
        from users.models import Profile as DjangoProfile
        DjangoUser = get_user_model()
        if field == "dni":
            profiles = DjangoProfile.objects.select_related("user").filter(dni=value)
            return [
                self._to_domain(p.user, p)
                for p in profiles
            ]

        users = DjangoUser.objects.select_related("profile").filter(**{field: value})
        return [
            self._to_domain(u, u.profile)
            for u in users
        ]

    def _to_domain(self, django_user, profile):
        from hex.users.domain import User
        return User(
            uuid=str(profile.uuid),
            username=django_user.username,
            email=django_user.email,
            dni=profile.dni,
        )
