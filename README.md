CiteMePy  - Python Script
===================
Given a wikipedia article as a URL, this script performs two tasks.

__Task 1:__ Get all lines with citations **X** ( where X is a number)

__Task 2:__ Get all the citations of a particular line.

Implemented using Python3, Requests, beautifulsoup4 and some magic sauce

----------

### __Installation__

Check out a copy of the CiteMePy repository or download the `CiteMe.py` file and execute it.
```
$ git clone https://github.com/varunsingh29/CiteMePy.git
$ cd CiteMePy
$ python3 CiteMe.py
```
#### __External Dependencies__

Requirements: Python 3.4.3+, Requests, beautifulsoup4

```
pip install requests
pip install beautifulsoup4
apt-get install python-lxml

```
It’s essential that you install lxml, since Python's in-built HTML parser isn't very good

---------

### __Running__
On executing, the script will request for a wikipedia URL, for example

`Enter URL:` https://en.wikipedia.org/wiki/Marvel_Comics

```
This can take a moment... Go grab a snickers!!
Choose type of query
[1]: Get lines with citation X
[2]: Get citations of a line
[3]: Exit
```

If Choice is 1
```
1
Enter citation number: 21
```
It outputs **all** the strings with that citation number. Here, 3 lines had citation [21]

>String(s)
>21: Goodman began using the globe logo of the Atlas News Company, the newsstand-distribution company he owned, on comics cover-dated November 1951 even though another company, Kable News, continued to distribute his comics through the August 1952 issues.

>21: In 1968, while selling 50 million comic books a year, company founder Goodman revised the constraining distribution arrangement with Independent News he had reached under duress during the Atlas years, allowing him now to release as many titles as demand warranted.

>21:  In 1969, Goodman finally ended his distribution deal with Independent by signing with Curtis Circulation Company.



If Choice is 2
```
2
Enter string: With few books issued under the imprint, Marvel and Disney Books Group relaunched Marvel Press in 2011 with the Marvel Origin Storybooks line.
```

>Citation(s)

>112

---------

### __Tests__

The script UnitTests.py uses `unittest` — Unit testing framework from Python's Standard Library

#### __Running Tests__
`$ python3 UnitTests.py`

```
Ran 8 tests in 24.512s
OK
```
The output of all testcases can be found in file 'Output'

----------
### **Pros**
- Python, hence supported on all platforms.
- For a given URL, processes all citations at once, so querying is in constant time.
- Accounts for cases with multiple citations, and text with no citations at all, can process UTF-8 characters.

### **Issues**

- Will not identify some lines that have texts such as __Oct. 19__ (notice the dot space character), __U.S.__ , __etc.__ (the word etcetera itself) and others since the fundamental assumption is that new sentence starts with a `. ` or a newline, so there is no way of telling if it is a new line or such abbreviations, and hence the output for a given citation number may sometimes have a partial sentence. Although, such cases are extremely less in numbers.

-----

__Bonus__ (For the love of xkcd)

![](perl_problems.jpg "Me after this project")





















