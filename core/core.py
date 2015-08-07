#!/src/bin/python3
import os.path
import urllib.request

def pywget(url):
    """
        download the given url

        Argument:
        url -- the url to be downloaded
    """
    if not isinstance(url, str):
        print("Error: url is not a string")
        return None

    filename = url[url.rfind("/")+1:]
    extension = os.path.splitext(filename)[1][1:].strip().lower()
    name_without_extension = os.path.splitext(filename)[0]

    # handle name collisions
    i = 1;
    while os.path.isfile(filename):
        filename = name_without_extension + "." + str(i) + "." + extension
        i += 1

    try:
        urllib.request.urlretrieve(url, filename)
    except:
        print("Network error")
