import requests, bs4, re


def findRegExp(regExp, string):
    list_of_finds = re.findall(regExp, string)
    if len(list_of_finds) == 0:
        return ""
    first_tuple = list_of_finds[0]
    return "".join(first_tuple)

baseURL = "https://rarbgprx.org/"
cookie = input("Enter cookie obtained from browser: ")
cookie_dict = dict(cookies_are=cookie)
threshold=float(input("Enter threshold: ") or 7.5)
pages=int(input("Number of pages to check: ") or 5)

catalogURL = baseURL + "catalog/movies/"
torrentCatalogURL = baseURL + "torrents.php?imdb="

for i in range(pages):
    catalogURLForIteration = catalogURL + str(i) + "/"
    page = requests.get(catalogURLForIteration, cookies=cookie_dict)
    catalogPage = bs4.BeautifulSoup(page.text)

    for p_title in catalogPage.find_all("p", "title"):
        tag_text = p_title.text
        imdb_rating = findRegExp("(?<=IMDB:.)(\d*)(\.*)(\d*)(?=\/)", tag_text)

        if imdb_rating != "":
            rating = float(imdb_rating)
            if(rating > threshold):
                film_title = ""
                for title in p_title.b:
                    film_title = title
                    break

                tt_ID = ""
                genre = list()
                for tt_ID_tag in p_title.find_all("a"):
                    tt_ID_tag_attrs = tt_ID_tag.attrs
                    if "onclick" in tt_ID_tag_attrs:
                        tt_ID_found = findRegExp("(?<=\(\')(tt)(\d*)(?=\'.)", tt_ID_tag_attrs["onclick"])
                        if tt_ID_found != "":
                            tt_ID = tt_ID_found
                    else:
                        genre.append(tt_ID_tag.text)



                print(film_title + " " + imdb_rating + " (" + ", ".join(genre) + ") " +torrentCatalogURL + tt_ID)



        #print(a)
        # for title in a.select("b"):
        #     title.b.unwrap()
        #     print(title)


