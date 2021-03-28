import webbrowser


baseURL = "https://rarbgprx.org/"
cookie = input("Enter cookie obtained from browser:")

catalogURL = baseURL + "catalog/movies/"

for i in range(5):
    catalogURLForIteration = catalogURL + i + "/"
    page = webbrowser.open()
