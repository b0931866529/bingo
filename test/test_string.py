import unittest

from pytest import skip


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        print("Hook method for setting up the test fixture before exercising it.")
        pass

    def tearDown(self):
        print("Hook method for deconstructing the test fixture after testing it.")
        pass

    @unittest.skip("demonstrating skipping")
    def test_upper(self):
        print("test_upper")
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        print("test_isupper")
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        print("test_split")
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'worlda'])


if __name__ == '__main__':
    # unittest.main()
    with open('test_output.txt', 'w') as f:
        runner = unittest.TextTestRunner(f)  # Set the test output file
        unittest.main(testRunner=runner)
