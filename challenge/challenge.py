#!/src/bin/python3
import os
import re
import urllib.request

def pywget(url, depth):
    """
        Check input type
        Then call initialise()

        Arguments:
        url   -- the url that is to be crawled
        depth -- the total number of recursions
    """
    if not isinstance(url, str) or not isinstance(depth, int):
        print("Error: Please check types.")
        print("url should be a string")
        print("depth should be an int")
        return None

    initialise(url, depth)

def initialise(url, depth):
    """
        Initialise all the values that is going to be used in the program
        Create files by the given url and download the given url
        Then call pywget_inside_crawler() function

        Arguments:
        url   -- the url that is to be downloaded
        depth -- the total number of recursions
    """
    dir_string = url[url.find('/')+2 : url.rfind('/')+1]                        # the directory name that is going to be created format of .../.../.../
    dir_string_list = dir_string.split('/')
    root_dir_name = dir_string_list[0]                                          # the root directory's name. useful to check collisions
    filename = url[url.rfind('/')+1:]

    root_dir_name = handle_collision("dir", root_dir_name, root_dir_name, '')   # handle directory name collisions

    start_dir = os.getcwd()                                                     # the location of this py file
    start_file = os.path.splitext(filename)[0]                                  # the first file that is downloaded. useful to avoid cycles

    dir_string_list[0] = root_dir_name
    dir_string = '/'.join(dir_string_list)                                      # change the directory names if collision happened

    os.makedirs(dir_string, exist_ok=True)
    os.chdir(dir_string)

    urllib.request.urlretrieve(url, filename)
    pywget_inside_crawler(url, depth, start_dir, start_file, root_dir_name)     # start crawlling and recursion

def pywget_inside_crawler(url, depth, start_dir, start_file, root_dir_name):
    """
        Crawl the given url find all <a href> and <img src> tags
        Get the information inside the tags and apply pywget_recursive() function on each of them

        Arguments:
        url                -- the url that is to be crawler
        depth              -- total number of recursions
        start_dir          -- the directory of the this py file
        start_file         -- the first file that was downloaded, store it to avoid cycles
        root_dir_name      -- the root derectory to for downloading files
    """
    depth -= 1

    content = ''
    try:
        request = urllib.request.urlopen(url)
        content = request.read().decode("utf-8")
    except:
        pass

    # all the information that's inside <a href> and <img src> tags
    match = re.findall(r'<a href="(.*?)"', content) + \
            re.findall(r'<a href = "(.*?)"', content) + \
            re.findall(r'<img src="(.*?)"', content) + \
            re.findall(r'<img src = "(.*?)"', content)

    prefix = url[0 : url.rfind('/')]                                           # a prefix of the link. useful to check if a link is under the same domain

    all_item_list = add_item_to_list(match, prefix)                            # add information to a list

    for item in all_item_list:
        pywget_recursive(item, depth, start_dir, start_file, root_dir_name)    # recursively download the information

def pywget_recursive(url, depth, start_dir, start_file, root_dir_name):
    """
        Recursively create directories and download files by the given url

        Arguments:
        url                -- the url that is to be crawler
        depth              -- total number of recursions
        start_dir          -- the directory of the this py file
        start_file         -- the first file that was downloaded, store it to avoid cycles
        root_dir_name      -- the root derectory to for downloading files
    """
    dir_string = url[url.find('/')+2 : url.rfind('/')+1]                       # the directory name that is going to be created
    dir_string_list = dir_string.split('/')
    dir_string_list[0] = root_dir_name
    dir_string = '/'.join(dir_string_list)                                     # change the directory name if collision happened

    filename = url[url.rfind('/')+1:]

    filename_without_extension = os.path.splitext(filename)[0]
    filename_extension = os.path.splitext(filename)[1][1:].strip().lower()
    filename = handle_collision("file", filename, filename_without_extension, filename_extension)

    os.chdir(start_dir)
    os.makedirs(dir_string, exist_ok=True)
    os.chdir(dir_string)

    if filename_without_extension != start_file:                               # do not download if it's the same file with the start file
        urllib.request.urlretrieve(url, filename)
    if depth > 0:
        pywget_inside_crawler(url, depth, start_dir, start_file, root_dir_name)

def handle_collision(file_or_dir, current_name, first_half, second_half):
    """
        To handle file name or directory name collisions
        That is if there is an existing filename, add .1 etc. between the filename and extension
        if there is an existing directory name, add .1 etc. after the directory name

        Arguments:
        file_or_dir   -- the type of the item that is to be handled
        current_name  -- the current name of the item
        first_half    -- the .1 etc. will be added after first_half
        second_half   -- the .1 etc. will be added before second_half

        Return:
        A new name that is going to be used. Must be a string.
    """
    if file_or_dir == "file":
        i = 1
        while os.path.isfile(current_name):
            current_name = first_half + '.' + str(i) + second_half
            i += 1
        return current_name
    elif file_or_dir == "dir":
        i = 1
        while os.path.isdir(current_name):
            current_name = first_half + '.' + str(i) + second_half
            i += 1
        return current_name
    return None

def add_item_to_list(given_list, prefix):
    """
        Add information inside <a href> and <img src> to the given list
        If it is an absolute link, check if it's under the same domain, if so add it to the list otherwise ignore
        If it is a relative link, add prefix in the front and add it to the list

        Arguments:
        given_list  -- a list that stores information inside <a href> and <img src> files
        prefix      -- pretty much the domain name but not exactly
                       for example if the domain name is homepage.ecs.ac.nz/root, the prefix will be
                       http://homepage.ecs.ac.nz/root

        Return:
        a list that contains all information inside <a href> and <img src>
        all items are in the format of absolute links
        Must be a list type
    """
    new_list = []
    if given_list:
        for item in given_list:
            item.lstrip()
            if item.startswith("http://") or item.startswith("https://") or item.startswith("//"):
                if item.startswith(prefix):
                    new_list.append(item)
            else:
                new_list.append(prefix + '/' + item)
    return new_list
