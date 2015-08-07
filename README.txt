core:
	def pywget(url)

	Done with no problems
	I had some inline comments at first but then I thought it'd be overkill as
the variable names explain things well enough. The PEP 8 Style guide for
Python Code suggests inline comments are usually unnecessary and this program
are almost all one-line code.

completion:
	def pywget(url, first_time=True)
	def pywget_inside_crawler(url)

	Done with no problems
	Same with core, I don't have many comments in the pywget() function but in
the pywget_inside_crawler() function I do believe my comments explained things
well.
	I made a default argument first_time and set it with a default true. The
idea is that if it's the first time it goes into the function, crawl the page,
otherwise do not. So basically it avoids recursion as this part only requires
a depth of 1 crawlling.


challenge:
	def pywget(url, depth)
	def initialise(url, depth)
	def pywget_inside_crawler(url, depth, start_dir, start_file, root_dir_name)
	def pywget_recursive(url, depth, start_dir, start_file, root_dir_name)
	def handle_collision(file_or_dir, current_name, first_half, second_half)
	def add_item_to_list(given_list, prefix)

	Done and I think there are no problems.

	Style comment:
	I thought it might be a good idea to split the programs into few functions
so each of them does their own job which makes the code more readable. It
seems like I had a little too many arguments but they actually they have to be
there and it's better than using global variables as it's safer.
	Unlike for core and completion, I had some inline comments in the
initialise() function as those variables need more explaination to tell what
they are for.

	Functionality comment:
	The program follows the assignment description. That is to avoid potential
cycles, there is a depth argument that the value is determained by the user.
Also, unlike in the completion part all the files are saved in a same
directory which is messy, this program creats the following local directory
structure when downloading:

	homepages.ecs.vuw.ac.nz/
		~ian/
			nwen241/
				index.html

	The above is well expalined in the assignment description and that is how
I followed. However there is something that the assignment description did not
cover. For example, if we follow the description and run the program with a
depth of 2, it is supposed to be like this:

	homepages.ecs.vuw.ac.nz/
		~ian/
			nwen241/
				felids.html
				felines.html
				images/
					...
				index.html
				index.1.html
				index.2.html

because we need to handle the name collisions. However in the sample output
there are no index.1.html or index.2.html. I asked this question on forum also
in person with tutors but have not got a clear answer to that. So I had to
guess the intention here and what I thought is that because index.html was the
very first url we gave to the program and we do not want cycle happen here. So
what I did was recording the very first url we gave to the program, if we have
found a same url we simply ignore it(i.e. do not download it). So now my
program outputs the same result as the sample output. And I hope what I did
is the assignment's intention.

	However my program still handles file name collisions, that is the same
with the core and completion part. In addition to that my program also handles
directory name collisions. For example if there is already a
homepages.ecs.vuw.ac.nz/ directory, if you run the program again it will
create a homepage.ecs.vuw.ac.nz.1/ directory.
