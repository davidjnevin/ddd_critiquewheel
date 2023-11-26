class BaseIAMDomainError(Exception):
    pass


class MissingEntryError(BaseIAMDomainError):
    pass


class NonMatchingPasswordsError(BaseIAMDomainError):
    pass


class WeakPasswordError(BaseIAMDomainError):
    pass


class DuplicateUsernameError(BaseIAMDomainError):
    pass


class IncorrectCredentialsError(BaseIAMDomainError):
    pass


class DuplicateEmailError(BaseIAMDomainError):
    pass


class AdminOnlyError(BaseIAMDomainError):
    pass


class WorkAlreadyExistsError(BaseIAMDomainError):
    pass


class CritiqueAlreadyExistsError(BaseIAMDomainError):
    pass
