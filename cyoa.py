# cyoa.py
# 
# A simple little script for taking a "flat file" of Choose Your Own Adventure fare and validating it.
# Every page either needs to have a conclusion or a link to other pages where the story continues.
# Every "select this option to continue!" choice needs to have a page fleshing out that choice.
# This script just lets you know when those parameters aren't being met, so you don't have loose ends around.
#
# This is how the formatting should look in your flat text file.  Just repeat this indefinitely:
#
# --------begin formatting quoting--------
# ##title##
# 
# text on a page.
# more text on a page.
# even more text on a page.
#
# #link_from_that_page# one option for the reader to follow.
# #other_linked_page# another option for the reader to follow
#
# ::a_resolution_if_there_were_no_options_to_follow::
# --------end formatting quoting--------
#
# Every entry needs at least one option for the reader to follow or a resolution (e.g., The End) for that branch
# of adventure-choosing.
#
# This script does some rudimentary checking, like "let's make sure no two pages have been assigned the same name"
# and the like, because that way lies madness.

import re, sys, os

# Broadly, how these dicts flesh themselves out:
#
# pages
#   title -> text
# endings
#   title -> ending
# options
#   title -> (option, option_text)

STORY_FILE = "cyoa_dummy.txt"   # replace with your own text file.  included so the dummy story file can be used to test validate.
if (len(sys.argv)>1):
	STORY_FILE = sys.argv[1]

VERBOSE = False
pages = {}
endings = {}
options = {}

# regular expressions get cached here
title_regex = re.compile('^##(.*?)##$')         # ##title##
link_regex = re.compile('^#([^#]+)#\s+(.*?)$')  # #link# Text of the link you are pursuing.
ending_regex = re.compile('^::(.*?)::$')        # ::end of this particular journey::

# MAIN PROGRAM BEGINS
# no use continuing if the file doesn't exist
if (not os.path.exists(STORY_FILE)):
	print("Cannot find file of the name %s for evaluating.  Aborting task." % STORY_FILE)
	exit(0)

story_fh = open(STORY_FILE)
print("Evaluating: %s" % STORY_FILE)
title = ""
text = ""
for line in story_fh:
	# let's see if we're onto a new "page" with a new title yet
    title_match = title_regex.match(line)
    if (title_match):
        if (title):
            pages[title] = text.strip() # save text from last title page
        title = title_match.group(1)
        if (VERBOSE): print("TITLE: {:s}".format(title))
        if (title in pages):
            print("PAGE ALREADY EXISTS: {:s}".format(title))
        text = ""                       # found a title - zero out text of this new page

	# let's see if this is a link, directing the user to another page with various choices
    link_match = link_regex.match(line)
    if (link_match):
        link_page = link_match.group(1)
        link_text = link_match.group(2)
        if (VERBOSE): print("on page '{:s}' link to page '{:s}' with '{:s}'".format(title, link_page, link_text))
        if (not title in options):
            options[title] = []
        options[title].append((link_page, link_text))       # add this link to this page's roster of options to follow

	# let's see if this is a ending, effectively concluding this branch of the story
    ending_match = ending_regex.match(line)
    if (ending_match):
        ending = ending_match.group(1)
        if (VERBOSE): print("ending for '{:s}' is '{:s}'".format(title, ending))
        endings[title] = ending
    
	# no special declarations = this must be more text for the user to read.  Keep trucking accordingly.
    if (not title_match and not link_match and not ending_match):
        text = text + line              # no match - must be part of the actual text here

# salt away whatever we'd parsed but not yet saved at file's end
if (title):
	pages[title] = text.strip()
		
# text parsed!  time to print analytics of what all was in that file and what shortcomings it might still have.
print("NUMBER OF ENDINGS: {:d}".format(len(endings)))
print("NUMBER OF PAGES: {:d}".format(len(pages)))

# show pages with placeholder tags in the file but no content just yet
for page in pages:
    if (not pages[page]):
        print("UNFINISHED: {:s}".format(page))
        endings[page] = "[unfinished]"			# dummy ending, so it won't show up in "no endings" below

# show pages with links to follow that don't go anywhere, not even to placeholder pages
for page in options:
    if (page in endings):
        print("CHOICES AND ENDING CONFLICT: {:s}".format(page))
    else:
	    endings[page] = "[no ending needed]"		# dummy ending, so it won't show up in "no endings" below
    options_arr = options[page]
    for (title, text) in options_arr:
        if (not title in pages):
            print("LINK TO NON-PAGE: {:s}".format(title))

# show pages with text but just no "this is how this branch concluded, the end" fluorish
for page in pages:
    if (not page in endings):
        print("HAS NO ENDINGS: {:s}".format(page))

