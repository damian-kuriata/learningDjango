import pytest
from django.conf import settings
from django.core.exceptions import ValidationError

from catalog import models

def test_file_size_validator_file_too_big():
    class TestObject:
        def __init__(self):
            self.size = settings.MAX_UPLOAD_SIZE + 1
    obj = TestObject()
    with pytest.raises(ValidationError) as err:
        models.file_size_validator(obj)
    print(dir(err))
    assert 'ValidationError(["File too big, the maximum file size is' in err.value

