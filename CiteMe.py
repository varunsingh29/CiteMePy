import requests
from bs4 import BeautifulSoup

input = raw_input("Enter URL: ")

try:
    r = requests.get(input)
except HTTPError:
    print("Oops ! An HTTP error occured")
except URLRequired:
    print("Oops ! Seems like that is not a valid URL")
except :
    print("Grats !! You broke it. Something went wrong")

# Check through regex that URL is a valid Wikipedia URL

def ins_element(key,val,inp):
    inp.setdefault(key, []).append(val)

# Citation is at the end of line
def cite_at_end(cur_tag):
    line = ""
    for sibling in cur_tag.previous_siblings:
        if re.search(re.compile(r"[^\.]+\. [^\.]*"),sibling.string):
            s1 = re.search(re.compile(r"\. ([^\.]*)$"),sibling.string)
            line = s1.group(1) + line
            break
        elif re.search(re.compile(r"[^\.]+\.$"),sibling.string) and line != "":
            break
        else:
            line = sibling.string + line
    # clean citation from text
    re.sub(r"\[[0-9]+]","",line)

    return line

def cite_others(cur_tag):
    line = ""
    for sibling in cur_tag.next_siblings:
        if(re.search(re.compile(r"[^\.]+\. [^\.]+"),sibling.string)):
            s1 = re.search(re.compile(r"\. ([^\.]+)"),sibling.string)
            line = line + s1.group(1)
        else:
            line = line + sibling.string

    return line


# Finding all reference strings
soup = BeautifulSoup(r.content, "lxml")
r_data = soup.find_all("span", class_ = "mw-cite-backlink")
bk_link = []
for item in r_data:
    tag = item.find("a")
    bk_link.append(tag['href'].lstrip('#'))

ref_list = {}
for item in bk_link:
    tag = item.find("sup", {"id", item})
    key_tag = tag.find("a")
    temp = str(key_tag.string)
    key = temp[1:-1]
    

