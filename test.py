import os
import unittest
from core import MockIt


class TestMockIt(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.app = MockIt(os.path.abspath('.'))

    def tearDown(self):
        pass

    def test_save_data(self):
        for x in range(3):
            self.app.save_data({'key': 'value'}, str(x))

    def test_get_data(self):
        for x in range(3):
            self.app.get_data("539facbf76cb401eed386eb131aa62ef")

    def test_mock(self):
        @self.app.mock(many=True)
        def mock_func(a, b):
            return a, b

        mock_func(11, {'a': '5'})
        mock_func(12, {'b': '6'})


if __name__ == '__main__':
    unittest.main()
