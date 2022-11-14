import unittest
import generatefixtures
import os
import os.path as path
import csv
import random
import sys
import pandas as pd

DIR = path.abspath(path.dirname(__file__))
FILES = {
    'clothing.csv': ('Blouses', 'Shirts', 'Tanks', 'Cardigans', 'Pants', 'Capris', '"Gingham" Shorts',),
    'accessories.csv': ('Watches', 'Wallets', 'Purses', 'Satchels',),
    'household_cleaners.csv': ('Kitchen Cleaner', 'Bathroom Cleaner',),
}
  
class test_generatefixtures(unittest.TestCase):
    def test_parse_cmd_line_none(self):
        sys.argv = ['generatefixtures.py']
        self.assertEqual(generatefixtures.parse_cmd_line(), [])

    def test_parse_cmd_line_single(self):
        sys.argv = ['generatefixtures.py', 'testarg']
        self.assertEqual(generatefixtures.parse_cmd_line(), ['testarg'])
    
    def test_parse_cmd_line_multiple(self):
        sys.argv = ['generatefixtures.py', 'testarg1', 'testarg2', 'testarg3']
        self.assertEqual(generatefixtures.parse_cmd_line(), ['testarg1', 'testarg2', 'testarg3'])

    def test_parse_cmd_line_multiple_redirect(self):
        sys.argv = ['generatefixtures.py', 'testarg1', 'testarg2', 'testarg3', '>', 'testargs4']
        self.assertEqual(generatefixtures.parse_cmd_line(), ['testarg1', 'testarg2', 'testarg3', 'testargs4'])

    def test_read_files_to_data_frame_empty(self): 
        df = pd.DataFrame()
        files = []
        self.assertTrue(generatefixtures.read_files_to_data_frame(files).equals(df))
    
    def test_read_files_to_data_frame_single_valid(self): 
        for fn, categories in FILES.items():
            with open(path.join(DIR, 'fixtures', fn), 'w', encoding='utf-8') as fh:
                generatefixtures.write_file(
                    csv.writer(fh, doublequote=False, escapechar='\\', quoting=csv.QUOTE_ALL),
                    random.randint(100, 1000),
                    categories
                )
        df = pd.DataFrame()
        files = ['.\\fixtures\\accessories.csv']
        df = pd.read_csv(files[0], index_col=None)
        df['filename'] = pd.Series([os.path.basename(files[0]) for x in range(len(df.index))])
        self.assertTrue(generatefixtures.read_files_to_data_frame(files).equals(df))

    def test_read_files_to_data_frame_multiple_valid(self): 
        for fn, categories in FILES.items():
            with open(path.join(DIR, 'fixtures', fn), 'w', encoding='utf-8') as fh:
                generatefixtures.write_file(
                    csv.writer(fh, doublequote=False, escapechar='\\', quoting=csv.QUOTE_ALL),
                    random.randint(100, 1000),
                    categories
                )
        df = pd.DataFrame()
        files = ['.\\fixtures\\accessories.csv', '.\\fixtures\\clothing.csv', '.\\fixtures\\household_cleaners.csv']
        df = pd.read_csv(files[0], index_col=None)
        df['filename'] = pd.Series([os.path.basename(files[0]) for x in range(len(df.index))])
        df2 = pd.read_csv(files[1], index_col=None)
        df2['filename'] = pd.Series([os.path.basename(files[1]) for x in range(len(df2.index))])
        df = pd.concat([df, df2])
        df2 = pd.read_csv(files[2], index_col=None)
        df2['filename'] = pd.Series([os.path.basename(files[2]) for x in range(len(df2.index))])
        df = pd.concat([df, df2])
        self.assertTrue(generatefixtures.read_files_to_data_frame(files).equals(df))

    def test_read_files_to_data_frame_all_invalid_non_existent(self): 
        df = pd.DataFrame()
        files = ['abc.csv', '123.csv', 'xyz.txt']
        self.assertTrue(generatefixtures.read_files_to_data_frame(files).equals(df))

    def test_read_files_to_data_frame_some_invalid(self): 
        for fn, categories in FILES.items():
            with open(path.join(DIR, 'fixtures', fn), 'w', encoding='utf-8') as fh:
                generatefixtures.write_file(
                    csv.writer(fh, doublequote=False, escapechar='\\', quoting=csv.QUOTE_ALL),
                    random.randint(100, 1000),
                    categories
                )
        f = open('test.csv', mode='w')
        df = pd.DataFrame()
        files = ['abc.csv', '.\\fixtures\\clothing.csv', '123.txt', 'generatefixtures.py', 'test.csv']
        df = pd.read_csv(files[1], index_col=None)
        df['filename'] = pd.Series([os.path.basename(files[1]) for x in range(len(df.index))])
        self.assertTrue(generatefixtures.read_files_to_data_frame(files).equals(df))
        f.close()
        os.remove('test.csv')
  
if __name__ == '__main__':
    unittest.main()