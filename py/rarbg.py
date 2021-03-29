"""
Expected response from rarbg
<p class="title">
	<b>The Bridge (2021)</b> » 1h04m » IMDB: 4.2/10 »
	<a href="/catalog/movies/Drama/">Drama</a>  »
	<a id="catalog-post-info-357783-link" onclick="gecibi('tt13873530','#catalog-post-info-357783','movies');return false;" href="#">More...</a>
</p>
"""

import requests, bs4, re


def findRegExp(regExp, string):
    list_of_finds = re.findall(regExp, string)
    if len(list_of_finds) == 0:
        return ""
    first_tuple = list_of_finds[0]
    return "".join(first_tuple)


REGEXP_IMDB_RATING = "(?<=IMDB:.)(\d*)(\.*)(\d*)(?=\/)"
REGEXP_IMDB_RATING_FULL = "(?<=IMDB:.)(\d*)(\.*)(\d*)(/*)(\d*)(?=)"
REGEXP_IMDB_ID = "(?<=\(\')(tt)(\d*)(?=\'.)"

baseURL = "https://rarbgprx.org/"
catalogURL = baseURL + "catalog/movies/"
torrentCatalogURL = baseURL + "torrents.php?imdb="
imdbBaseUrl = "https://www.imdb.com/title/"

cookie = input("Enter cookie obtained from browser: ")
cookie_dict = dict(cookies_are=cookie)
threshold = float(input("Enter threshold: ") or 7.5)
pagesToCheck = int(input("Number of pages to check: ") or 5)

for pageNo in range(pagesToCheck):
    catalogURLForIteration = catalogURL + str(pageNo) + "/"
    page = requests.get(catalogURLForIteration, cookies=cookie_dict)
    catalogPage = bs4.BeautifulSoup(page.text)

    for p_title in catalogPage.find_all("p", "title"):
        tag_text = p_title.text
        imdb_rating = findRegExp(REGEXP_IMDB_RATING, tag_text)

        if imdb_rating == "":
            continue

        rating = float(imdb_rating)
        if (rating > threshold):
            film_title = ""
            for title in p_title.b:
                film_title = title
                break

            tt_ID = ""
            genre = list()
            for tt_ID_tag in p_title.find_all("a"):
                tt_ID_tag_attrs = tt_ID_tag.attrs
                if "onclick" in tt_ID_tag_attrs:
                    tt_ID_found = findRegExp(REGEXP_IMDB_ID, tt_ID_tag_attrs["onclick"])
                    if tt_ID_found != "":
                        tt_ID = tt_ID_found
                else:
                    genre.append(tt_ID_tag.text)

            print(film_title + " " + imdb_rating + " (" + ", ".join(
                genre) + ") " + torrentCatalogURL + tt_ID + " " + imdbBaseUrl + tt_ID)
