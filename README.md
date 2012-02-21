refuge.blog
-----------

Here is the current couchapp running the blog in the website http://refuge.io.

You can use the script `publish.py` in the _scripts folder to send post.
To use it, you will need to install couchdbkit first.


All posts should be in one folder and are using the doc on fs definition
from couchapp: 
                                                                  

    /posts
        /onepost
            title
            body
            _attachments/


the body should be written in markdown. _attachments could contains any
attachments needed for a post.
