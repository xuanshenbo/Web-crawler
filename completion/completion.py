#!/src/bin/python3
import os.path
import re
import urllib.request

def pywget(url, first_time=True):
    """
        Download the given url

        Argument:
        url         -- the url to be downloaded
        first_time  -- to avoid recursion
                       default value True
    """
    if not isinstance(url, str):
        print("Error: url is not a string")
        return None

    filename = url[url.rfind('/')+1:]
    extension = os.path.splitext(filename)[1][1:].strip().lower()
    name_without_extension = os.path.splitext(filename)[0]

    # handle name collision
    i = 1;
    while os.path.isfile(filename):
        filename = name_without_extension + '.' + str(i) + '.' + extension
        i += 1

    try:
        urllib.request.urlretrieve(url, filename)
        if first_time:
            pywget_inside_crawler(url)
    except:
        pass

def pywget_inside_crawler(url):
    """
        Crawl the content of the file

        Argument:
        url -- the url that is to be crawled
    """

    # open and read the url
    content = ''
    try:
        request = urllib.request.urlopen(url)
        content = request.read().decode("utf-8")
    except:
        pass

    # find all contents we need which are links and srcs using regex
    match = re.findall(r'<a href="(.*?)"', content) + \
            re.findall(r'<img src="(.*?)"', content) + \
            re.findall(r'<a href = "(.*?)"', content) + \
            re.findall(r'<img src = "(.*?)"', content)

    domain_name = url[0 : url.rfind('/')]

    all_item_list = []

    # if it's an absolute link, add it to all_item_list
    # if it's a relative link, add prefix in the front and add it to the list
    if match:
        for item in match:
            if item.startswith("http://") or item.startswith("https://") or item.startswith("//"):
                if item.startswith(domain_name):
                    all_item_list.append(item)
            else:
                all_item_list.append(domain_name + "/" + item)

    # apply pywget_download_inside
    for item in all_item_list:
        pywget(item, first_time=False)
