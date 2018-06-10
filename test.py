import faceAnalise

class TestFace:
    def test_delete_old_message(self):
        assert faceAnalise.detect_faces() is not None
