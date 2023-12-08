class BaseWorkDomainError(Exception):
    pass


class InvalidEntryError(BaseWorkDomainError):
    pass


class MissingEntryError(BaseWorkDomainError):
    pass


class WorkNotAvailableForCritiqueError(BaseWorkDomainError):
    pass


class CritiqueDuplicateError(BaseWorkDomainError):
    pass
