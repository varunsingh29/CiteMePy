import CiteMe
import os
import sys
import unittest

class TestMethods(unittest.TestCase):

    def test_isvalidURL1(self):
        inp = ["www.google.com","1","1"]
        with self.assertRaises(SystemExit):
            ans = CiteMe.maincite(inp)

    def test_isvalidURL2(self):
        inp = ["https://en.wikipedia.org/Marvel_Comics","1","1"]
        with self.assertRaises(SystemExit):
            ans = CiteMe.maincite(inp)

    def test_nocitations(self):
        # Wikipedia Page with No Citations - Regular Grammar 
        inp = ["https://en.wikipedia.org/wiki/Regular_grammar","1","2"]
        expect = ["Sorry ! No citations found."]
        print(CiteMe.maincite(inp))
        self.assertEqual(CiteMe.maincite(inp),expect)

    def test_query1(self):
        # Query of Type 1 - Get lines having citation X
        inp = ["https://en.wikipedia.org/wiki/Marvel_Comics","1","82"]
        expect = ["82: Marvel relaunched the CrossGen imprint, owned by Disney Publishing Worldwide, in March 2011."]
        self.assertEqual(CiteMe.maincite(inp),expect)

    def test_query1_multiple(self):
        # Query of Type 1 where X has multiple lines
        inp = ["https://en.wikipedia.org/wiki/Marvel_Comics","1","10"]
        expect = []
        expect.append("10:  The issue was a great success, with it and a second printing the following month selling, combined, nearly 900,000 copies.")
        expect.append("10:  It, too, proved a hit, with sales of nearly one million.")
        self.assertEqual(CiteMe.maincite(inp),expect)

    def test_query2(self):
        # Query of Type 2 - Get citations of a line
        inp = ["https://en.wikipedia.org/wiki/Marvel_Comics","2","Disney Kingdoms"]
        expect = ["79"]
        self.assertEqual(CiteMe.maincite(inp),expect)

    def test_query2_substring(self):
        # Query of Type 2 with only substring input
        inp = ["https://en.wikipedia.org/wiki/Marvel_Comics","2"," Marvel issued its collectable caps for "]
        expect = ["105"]
        self.assertEqual(CiteMe.maincite(inp),expect)

    def test_invalidchoice(self):
        inp = ["https://en.wikipedia.org/wiki/Marvel_Comics","5","2"]
        expect = ["Invalid Choice ! Re-enter: "]
        self.assertEqual(CiteMe.maincite(inp),expect)



if __name__ == '__main__':

    # Suppress print statements from CiteMe
    save_stdout = sys.stdout
    sys.stdout = open('Output', 'w')
    unittest.main()
    sys.stdout = save_stdout

