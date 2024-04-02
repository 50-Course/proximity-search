from django.core.exceptions import ObjectDoesNotExist

class ObjectDoesNotExistException(ObjectDoesNotExist):
    """
    Wrapper around django's `ObjectDoesNotExist`
    """
