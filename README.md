# WikiLinks

---------
File List
---------

The following files are required for this web app:
 - index.html
 - style.css
 - wiki.py
 - wiki.sql (not included)


------
Set-up
------

I set up an apache server to run this web app and named it moatserver.com on port 80 and ran it locally on a VirtualBox running Fedora 24.  The 'index.html' and 'style.css' files were placed in /var/www and the 'wiki.py' and 'wiki.sql' files were placed in /var/www/cgi-bin.  The httpd.conf file was edited to increase the timeout time (more on that later) and to enable the server to execute .py files


------------------------------
Design Decisions & Explanation
------------------------------

The point of this project is to determine the minimum number of links that it will take to get from one arbitrary Wikipedia page to another by following any of the links that appear on any given page.  This sort of problem lends itself to a breadth first search, as a depth first search would follow the first link on each subsequent page and most likely find itself in an infinite loop before ever reaching the target page.

This implementation tracks the 'parent' page of each child page, so as to enable a means of back-tracking and identifying each of the links taken to get from the source page to the destination page
 

------------
Optimization
------------

The run-time of this program is poor when it needs to traverse 3+ links (hence, increasing the timeout of the server).  I made several attempts to improve the speed, and did, but only nominally.  I'm fairly certain I need to make a fundamental alorithmic change to get the speed-up in processing I need, but wasn't able to come up with what that change might be.  Some of the changes I did make were database related.  Specifically, I modified some of the pragmas (journal mode, synchronous, temp store, and page size) and indexed the source_id field in the link table.  Again, this resulted in speed-ups on the order of 2 or 3x, but not the order of magnitude speed up needed to get the time down to a reasonable level.  In the wiki.py script, I made attempts at bulk SELECT calls and other similar SQL changes, but the python api for working with SQLite databases has limited functionality