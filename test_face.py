import pytest
from botocore.exceptions import NoRegionError

import faceAnalise

def test_delete_old_message(self):
    with pytest.raises(NoRegionError):
        faceAnalise.detect_faces()
