# cyoa

This is a script I wrote to help me manage my own Choose Your Own Adventure
branching.  Which choices did I forget to pen?  Which branches did I let die on
the vine?  Which choices did I write up text for, but neglect to add either any
conclusions or user choices from? This helped me keep such matters under wraps.

The formatting of the text file where all your input is stored should look
roughly like so:

-------------------------------------------------------------
##title##
 
text on a page.
more text on a page.
even more text on a page.

#link_from_that_page# one option for the reader to follow.
#other_linked_page# another option for the reader to follow

::a_resolution_if_there_were_no_options_to_follow::
-------------------------------------------------------------

And so on and so on, forever.  If you run the default cyoa.py setup against
"cyoa_dummy.txt", you should receive the following warnings as output:

Evaluating: cyoa_dummy.txt
NUMBER OF ENDINGS: 3
NUMBER OF PAGES: 6
UNFINISHED: fire_without_content
CHOICES AND ENDING CONFLICT: test_story
LINK TO NON-PAGE: void_fire
HAS NO ENDINGS: fire_without_conclusion

As opposed to "cyoa_smarty.txt", which validates and thus yields the following:
Evaluating: cyoa_smarty.txt
NUMBER OF ENDINGS: 5
NUMBER OF PAGES: 7