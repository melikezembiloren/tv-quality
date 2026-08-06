class DomainError(Exception):
    """Tüm domain hatalarının temel sınıfı."""
    pass


class InvalidTvStateError(DomainError):
    """Bir TV, mevcut durumunda izin verilmeyen bir işleme tabi tutulmaya çalışıldığında fırlatılır."""
    pass

class InvalidDefectStateError(DomainError):
    """Bir Defect, mevcut durumunda izin verilmeyen bir işleme tabi tutulmaya çalışıldığında fırlatılır."""
    pass
