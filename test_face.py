import pytest
import faceAnalise

@pytest.fixture()
def test_delete_old_message(self):
    assert (faceAnalise.detect_faces() is not None)
