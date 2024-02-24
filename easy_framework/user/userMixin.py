class UserMixin():
    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def is_anonymous(self) -> bool:
        return False

    @property
    def is_active(self) -> bool:
        return True


class AnonymousUser():
    @property
    def is_authenticated(self) -> bool:
        return False

    @property
    def is_anonymous(self) -> bool:
        return True

    @property
    def is_active(self) -> bool:
        return False

    def getId(self) -> bool:
        return None
