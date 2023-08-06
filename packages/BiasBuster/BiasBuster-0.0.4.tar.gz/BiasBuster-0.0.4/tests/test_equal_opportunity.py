import unittest
import pickle
from BiasBuster import equal_opportunity
import os
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

CLF_FILENAME = os.path.join(os.path.dirname(__file__), 'Decisiontreemodel_3months.pkl')
A_FILENAME = os.path.join(os.path.dirname(__file__), 'X_test_abi.pkl')
B_FILENAME = os.path.join(os.path.dirname(__file__), 'X_test_kein_abi.pkl')
C_FILENAME = os.path.join(os.path.dirname(__file__), 'y_test_abi.pkl')
D_FILENAME = os.path.join(os.path.dirname(__file__), 'y_test_kein_abi.pkl')


class TestCalculateEO(unittest.TestCase):
    def setUp(self):
        infile = open(CLF_FILENAME, 'rb')
        self.clf = pickle.load(infile)
        infile.close()
        
        infile = open(A_FILENAME, 'rb')
        self.X_test_abi = pickle.load(infile)
        infile.close()

        infile = open(B_FILENAME, 'rb')
        self.X_test_kein_abi = pickle.load(infile)
        infile.close()

        infile = open(C_FILENAME, 'rb')
        self.y_test_abi = pickle.load(infile)
        infile.close()

        infile = open(D_FILENAME, 'rb')
        self.y_test_kein_abi = pickle.load(infile)
        infile.close()

    def test_calculate_abroca(self):
        self.assertEqual(equal_opportunity.calculate_equal_opportunity(self.clf, self.X_test_abi, self.y_test_abi, self.X_test_kein_abi, self.y_test_kein_abi),0.003677900887379515)

if __name__ == '__main__':
    unittest.main()