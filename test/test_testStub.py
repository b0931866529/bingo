import unittest

from pytest import skip

from testStub import AccountDao, Hash, Validation
from unittest.mock import Mock


class TestValidationMethods(unittest.TestCase):
    def setUp(self):
        print("Hook method for setting up the test fixture before exercising it.")
        pass

    def tearDown(self):
        print("Hook method for deconstructing the test fixture after testing it.")
        pass

    def test_CheckAuthentication(self):
        # arrange
        accountDao = Mock()
        hash = Mock()
        target = Validation(accountDao, hash)
        id = ''
        password = ''
        excepted = False
        # Configure the mock method return value
        accountDao.GetPassword.return_value = 'ttt'

        # act
        actual = target.CheckAuthentication(id, password)
        # assert
        self.assertEqual(excepted, actual)

    @unittest.skip("demonstrating skipping")
    def test_upper(self):
        print("test_upper")
        self.assertEqual('foo'.upper(), 'FOO')

    @unittest.skip("demonstrating skipping")
    def test_isupper(self):
        print("test_isupper")
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    @unittest.skip("demonstrating skipping")
    def test_split(self):
        print("test_split")
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'worlda'])


if __name__ == '__main__':
    unittest.main()
    # with open('test_output.txt', 'w') as f:
    #     runner = unittest.TextTestRunner(f)  # Set the test output file
    #     unittest.main(testRunner=runner)
