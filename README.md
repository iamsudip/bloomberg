bloomberg hack
==============

Project requirement
-------------------

Build a crawler to store all the plain article text from www.bloomberg.com in mongodb


How to run
----------

To start the daemon ::

    $ python bloomhack.py start

this will start inserting the articles to the database(Assuming the mongodb database is running).
It will log the data inserted to the database in a file named bloomhack.log.

To stop the daemon ::

    $ python bloomhack.py stop


Press [ctrl]+c to stop the process.


Example run
-----------

    $ python bloomhack.py start
    PID: 3418 Daemon started successfully
    $

    $ python bloomhack.py stop
    Daemon killed succesfully
    $

