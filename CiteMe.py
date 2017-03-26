import requests
import re
from collections import defaultdict
from bs4 import BeautifulSoup

# If citation is immediately after full stop
def cite_at_end(cur_tag):
    line = ""
    list_string = []
    
    '''
    Traverse through all previous_siblings and store
    the text in a list named list_string. Only through
    previous_siblings because citation is at the end of line
    '''
    for sibling in cur_tag.previous_siblings:
        # If tag has multiple strings, it returns None
        if sibling.string is None :
            for temp in sibling.stripped_strings:
                list_string.append(temp)
        else:
            list_string.append(sibling.string)

    '''
    For each string, check if a full stop is encountered through
    following cases. If yes, extract the string and break.
    If no, continue.
    '''
    for item in list_string:
        # If full stop is in first line itself
        s1 = re.search(re.compile(r"\.([^\.]+(\.[0-9]+)*[^\.]+\.)$"),item)
        if s1 and not line:
            line = s1.group(1)
            break
        # If full stop is at end of another line.
        elif re.search(re.compile(r".*\.$"),item) and line:
            break
        # If first sentence is in line of the format {text . text}
        elif re.search(re.compile(r"[^0-9]+\.([^\.]+(\.[0-9]+)*[^\.]+)$"),item):
            s1 = re.search(re.compile(r"[^0-9]+\.([^\.]+(\.[0-9]+)*[^\.]+)$"),item)
            line = s1.group(1) + line
            break
        else:
            line = item + line

    # clean citation from text
    line = re.sub(r"\[[0-9]+]+","",line)
        
    return line



# If citation is in the middle of a sentence
def cite_others(cur_tag):
    line = ""
    list_string_prev = []
    list_string_next = []

    '''
    Traverse through all previous and next siblings and store
    the strings in seperate lists named list_string_prev and
    list_string_next respectively.
    '''
    for sibling in cur_tag.previous_siblings:
        # If multiple string is present, .string returns None
        if sibling.string is None:
            for temp in sibling.stripped_strings:
                list_string_prev.append(line)
        else:
            list_string_prev.append(sibling.string)

    for sibling in cur_tag.next_siblings:
        if sibling.string is None:
            for temp in sibling.stipped_strings:
                list_string_next.append(line)
        else:
            list_string_next.append(sibling.string)

    for item in list_string_prev:
        # If string is of format {text . text}
        if re.search(re.compile(r"[^0-9]+\.([^\.]+(\.[0-9]+)*[^\.]+)$"),item):
            s1 = re.search(re.compile(r"[^0-9]+\.([^\.]+(\.[0-9]+)*[^\.]+)$"),item)
            line = line + s1.group(1)
            break
        # If full stop is at the end of line. Break !! Nothing to extract
        elif re.search(re.compile(r".*\.$"),item):
            break
        else:
            line = item + line

    for item in list_string_next:
        if re.search(re.compile(r"[^\.]+\. [^\.]+"),item):
            s1 = re.search(re.compile(r"^([^\.]+\.)"),item)
            line = line + s1.group(1)
            break
        elif re.search(re.compile(r"(.+\.)(\[[0-9]+])*"),item):
            s1 = re.search(re.compile(r"(.+\.)(\[[0-9]+])*"),item)
            line = line + s1.group(1)
            break
        elif re.search(re.compile(r"^\."),item):
            break
        else:
            line = line + item

    # Clean citation from text
    line = re.sub(r"\[[0-9]+]+","",line)
    
    return line

##############


# Main 
inp = input("Enter URL: ")
if  not re.match(re.compile(r"https://en.wikipedia.org/wiki/.+"),inp):
    print("Oops ! Seems like you entered an invalid URL")
    exit()

# Download webpage using requests
try:
    r = requests.get(inp)
except HTTPError:
    print("Oops ! An HTTP error occured")
    exit()
except ConnectionError:
    print("Oops ! Connection Error")
    exit()
except :
    print("Grats !! You broke it. Something went wrong")
    exit()

print("This can take a moment... Go grab a snickers!!")

# Parse webpage using BS
soup = BeautifulSoup(r.content, "lxml")

'''
Picks up all cite_backlinks from <References> section and inserts
them in a list named 'bk_link'. Since a number can have multiple
citations, so find result set -> tag and iterate through every
anchor tag to find name of backlinks
'''
r_data = soup.find_all("span", class_ = "mw-cite-backlink")
bk_link = []
for item in r_data:
    tag = item.find_all("a")
    for iter in tag:
        bk_link.append(iter['href'].lstrip('#'))

'''
For every item in bk_link, find the tag associated with it and
store the citation number in 'key' and then navigate either 
side depending on the position of citation encountered.
'''
ref_list = []
for item in bk_link:
    tag = soup.find("sup", {"id":item})
    key_tag = tag.find("a")
    temp = str(key_tag.string)

    # Strip sqaure brackets from [num] and store as key
    key = temp[1:-1]
    
    '''
    If multiple citations are present iterate to the tag 
    with left most citation, to check which of the following
    cases shall apply
    '''
    if tag.previous_sibling:
        while re.search(re.compile(r"\[[0-9]+]"),\
                tag.previous_sibling.string):
            tag = tag.previous_sibling

    # If citation is present immediately after fullstop.
    if re.search(re.compile(r"[^\.]*\.$"),tag.previous_sibling.string):
        line = cite_at_end(tag)
        ref_list.append((key,line))
    # If citation is present in between of the sentence.
    else:
        line = cite_others(tag)
        ref_list.append((key,line))
    
    '''
    Create a dictionary named 'ref' whose value is a list of strings
    to account for keys having multple citations. Key will be citation
    number and value is all the lines with citation X.
    Create a inverse map for type 2 queries.
    '''
    ref = defaultdict(list)
    for k,v in ref_list:
        ref[k].append(v)

    inv_ref = defaultdict(list)
    for k,v in ref_list:
        inv_ref[v].append(k)

# Print the entire reference dictionary
for k,v in sorted(inv_ref.items()):
    print(k, v)

usr_msg = '''Choose type of query \n[1]: Get lines with citation X\
        \n[2]: Get citations of a line \n[3]: Exit\n'''

choice = True
while choice:
    try:
        ch = input(usr_msg)
    except KeyboardInterrupt:
        exit()

    # Get lines with citation X
    if ch == '1':
        X = input("Enter citation number: ")
        if X in ref:
            print("String(s)")
            for item in ref[X]:
                print(X + ": " + item)
        else:
            print("Sorry ! No citations found.")
    # Get citations of a line
    elif ch == '2':
        search = input("Enter string: ")
        if search in inv_ref:
            print("Citation(s)")
            for item in inv_ref[search]:
                print(item)
        else:
            print("Sorry ! No citations found.")
    elif ch == '3':
        choice = False
    else:
        print("Invalid Choice ! Re-enter: ")

