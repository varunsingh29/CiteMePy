import requests
import re
from collections import defaultdict
from bs4 import BeautifulSoup

inp = input("Enter URL: ")

try:
    r = requests.get(inp)
except HTTPError:
    print("Oops ! An HTTP error occured")
except URLRequired:
    print("Oops ! Seems like that is not a valid URL")
except :
    print("Grats !! You broke it. Something went wrong")

# Check through regex that URL is a valid Wikipedia URL

# Citation is at the end of line
def cite_at_end(cur_tag):
    line = ""
    list_string = []
    for sibling in cur_tag.previous_siblings:
        if sibling.string is None :
            for temp in sibling.stripped_strings:
                list_string.append(temp)
        else:
            list_string.append(sibling.string)

    for item in list_string:
        # If first sentence is in first line
        s1 = re.search(re.compile(r"\.([^\.]+(\.[0-9]+)*[^\.]+\.)$"),item)
        if s1 and not line:
            line = s1.group(1)
            break
        # If full stop is at end of another line.
        elif re.search(re.compile(r".*\.$"),item) and line:
            break
        # If first sentence is in line of {text . text}
        elif re.search(re.compile(r"\.([^\.]+(\.[0-9]+)*[^\.]+)$"),item):
            s1 = re.search(re.compile(r"\.([^\.]+(\.[0-9]+)*[^\.]+)$"),item)
            line = s1.group(1) + line
            break
        else:
            line = item + line

    # clean citation from text
    line = re.sub(r"\[[0-9]+]+","",line)
        
    return line

def cite_others(cur_tag):
    line = ""
    list_string_prev = []
    list_string_next = []
    for sibling in cur_tag.previous_siblings:
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
        if re.search(re.compile(r"\.([^\.]+(\.[0-9]+)*[^\.]+)$"),item):
            s1 = re.search(re.compile(r"\.([^\.]+(\.[0-9]+)*[^\.]+)$"),item)
            line = line + s1.group(1)
            break
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

    # clean citation from text
    line = re.sub(r"\[[0-9]+]+","",line)
    
    return line


soup = BeautifulSoup(r.content, "lxml")
r_data = soup.find_all("span", class_ = "mw-cite-backlink")
bk_link = []
for item in r_data:
    tag = item.find("a")
    bk_link.append(tag['href'].lstrip('#'))

ref_list = []
for item in bk_link:
    tag = soup.find("sup", {"id":item})
    key_tag = tag.find("a")
    temp = str(key_tag.string)
    #print(temp)
    key = temp[1:-1]
    
    # Check if multiple citations at end if yes roll to upper tag
    if tag.previous_sibling:
        while re.search(re.compile(r"\[[0-9]+]"),\
                tag.previous_sibling.string):
            tag = tag.previous_sibling

    if re.search(re.compile(r"[^\.]*\.$"),tag.previous_sibling.string):
        line = cite_at_end(tag)
        ref_list.append((key,line))
    else:
        line = cite_others(tag)
        ref_list.append((key,line))
    #print(line)
    
    # Create Dictionary whose value is list of strings
    ref = defaultdict(list)
    for k,v in ref_list:
        ref[k].append(v)

for k,v in sorted(ref.items()):
    print(k, v)
