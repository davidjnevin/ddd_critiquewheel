class MemberServiceError(Exception):
    pass


class InvalidCredentialsError(MemberServiceError):
    pass


class MemberNotFoundError(MemberServiceError):
    pass


class DuplicateEntryError(MemberServiceError):
    pass


class DuplicateUsernameError(MemberServiceError):
    pass


class InvalidEntryError(MemberServiceError):
    pass


class MissingUsernameError(MemberServiceError):
    pass


class MissingEmailError(MemberServiceError):
    pass


class MissingPasswordError(MemberServiceError):
    pass


class MissingConfirmPasswordError(MemberServiceError):
    pass


class PasswordMismatchError(MemberServiceError):
    pass


class InvalidPasswordError(MemberServiceError):
    pass


class InvalidEmailError(MemberServiceError):
    pass


class InvalidUsernameError(MemberServiceError):
    pass
