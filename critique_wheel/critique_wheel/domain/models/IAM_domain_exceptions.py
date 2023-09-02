class BaseIAMError(Exception):
    pass


class MissingEntryError(BaseIAMError):
    pass


class NonMatchingPasswordsError(BaseIAMError):
    pass


class WeakPasswordError(BaseIAMError):
    pass


class DuplicateUsernameError(BaseIAMError):
    pass


class IncorrectCredentialsError(BaseIAMError):
    pass


class DuplicateEmailError(BaseIAMError):
    pass


class AdminOnlyError(BaseIAMError):
    pass


class WorkAlreadyExistsError(BaseIAMError):
    pass


class CritiqueAlreadyExistsError(BaseIAMError):
    pass
