from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime
from pymongo import MongoClient

# Set headers
headers = requests.utils.default_headers()
headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.137 Safari/537.36'})

def trimmer(txt):
    rev = txt.split()
    rev[len(rev) - 1] = ""
    txt = ""
    txt = ' '.join([str(v) for v in rev])
    return txt.strip()


def findBookInfo(db, txt):
    t = txt.split("\n")
    all_info = []
    flag = False
    i = 0
    while i < len(t):

        if "GUTINDEX.2002" in t[i]:
            i = 170
            continue

        if "TITLE and AUTHOR" in t[i]:
            flag = True
            i += 1
            continue

        if t[i].strip() == "":
            i += 1
            continue
        else:
            j = i + 1
            other_lang = False
            while t[j].strip() != "":
                if "Language" in t[j]:
                    other_lang = True
                j += 1
            if (other_lang):
                i = j + 1
                if i == len(t):
                    continue

        if t[i].strip() == "" and t[i - 1].strip() == "":
            i += 1
            continue

        if "Posting Dates for the below" in t[i]:
            i += 1
            continue

        if ("[" in t[i]) or ("]" in t[i]):
            if (("[" in t[i]) and ("]" in t[i])):
                pass
            else:
                i += 1
                continue

        if (flag):
            temp = t[i]
            if ", by" in temp:
                info = temp.split(", by")
                book = info[0].strip()
                if book[len(book) - 1] == ",":
                    book = book[:-1]
                try:
                    author = trimmer(info[1])
                except:
                    i += 1
                    continue
                derived = []
                j = i + 1
                other_lang = False
                while t[j].strip() != "":
                    if "Language" in t[j]:
                        other_lang = True
                    j += 1
                if not other_lang:
                    derived.append(book)
                    derived.append(author)
                    all_info.append(derived)
                    i = j

            elif "by" in t[i]:
                info = temp.split("by")
                derived = []
                book = info[0].strip()

                try:
                    if book[len(book) - 1] == ",":
                        book = book[:-1]
                except:
                    i += 1
                    continue
                derived.append(book)
                derived.append(trimmer(info[1]))
                all_info.append(derived)
                j = i + 1
                while t[j].strip() != "":
                    j += 1
                i = j

            else:
                derived = []
                if t[i + 1].strip() == "":
                    if (i + 1) == (len(t) - 1):
                        i += 1
                        continue
                    book = trimmer(t[i])
                    if book[len(book) - 1] == ",":
                        book = book[:-1]
                    derived.append(book)
                    derived.append("Unknown")
                    all_info.append(derived)

                elif "by" in t[i + 1]:
                    book = trimmer(t[i])
                    val = t[i + 1].split("by")
                    book += val[0].strip()
                    if book[len(book) - 1] == ",":
                        book = book[:-1]
                    derived.append(book)
                    derived.append(val[1])
                    all_info.append(derived)
                    j = i + 2
                    while t[j].strip() != "":
                        j += 1
                    i = j + 1
                    continue
                    # i += 1
                else:
                    if ("[" in t[i + 1]) or ("]" in t[i + 1]):
                        j = i + 1
                        while t[j].strip() != "":
                            j += 1
                        i = j + 1
                        continue

                    book = trimmer(t[i])
                    if book[len(book) - 1] == ",":
                        book = book[:-1]

                    j = i + 1
                    info = []
                    found_author = False
                    while t[j].strip() != "":
                        if "by" in t[j]:
                            info = t[j].split("by")
                            found_author = True
                        else:
                            if not found_author:
                                book += t[j]
                            else:
                                book += info[0]
                        j += 1

                    if book[len(book) - 1] == ",":
                        book = book[:-1]
                    derived.append(book)

                    if not info:
                        derived.append("Unknown")
                    else:
                        derived.append(info[1].strip())
                    all_info.append(derived)
                    # book += t[i+1]
                    i = j
        i += 1
    for i in range(len(all_info)):
        # print(all_info[i][0].strip() ," | " , all_info[i][1])
        db.books.insert_one({"title": all_info[i][0], "author": all_info[i][1]})


client = MongoClient("mongodb+srv://admin:U9gyl4m0gWCzPeEO@cluster0.36gi7.mongodb.net/book_db?retryWrites=true&w=majority")
db = client['book_db']
i = 1998
while i < 2021:
    url = "http://www.gutenberg.org/dirs/GUTINDEX." + str(i)
    print("URL", url)
    if i != 1998:
        time.sleep(100)   #  min delay
    start_time = datetime.now().time()
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    findBookInfo(db, soup.prettify())
    end_time = datetime.now().time()
    c1 = db['process_log']
    c1.insert_one({"year": i, "start_time": str(start_time), "end_time": str(end_time)})
    i += 1
