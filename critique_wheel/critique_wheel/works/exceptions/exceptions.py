class BaseWorkDomainError(Exception):
    pass


class MissingEntryError(BaseWorkDomainError):
    pass


class WorkNotAvailableForCritiqueError(BaseWorkDomainError):
    pass


class CritiqueDuplicateError(BaseWorkDomainError):
    pass
