marchanddesable
===============

Turn off your server when you sleep.

Install
-------

The easiest way is to just grab the file `marchanddesable.py`.

If you want to install it, `Marchanddesable` is on pypi_, so this should do the trick :

    pip install marchanddesable

.. _pypi: http://pypi.python.org/pypi/marchanddesable

Arch users, you can install `marchanddesable` from AUR.

Usage
-----
To halt the current machines 5 minutes after both 192.168.0.1 and 192.168.0.2 stop pinging, just execute this often enough (every minute in your cron, for example)::

    marchand 192.168.0.1 192.168.0.2

If you don't like cron, and think running daemon or programs in screen are better, you can use ::

    marchand 192.168.0.1 192.168.0.2

TODO
----

These features may or may not be implemented at some point :

- Play a sound to warn when the machines stopped pinging

If you want any of those, or anything else, give me a shout.

Also, I wrote this to scratch my own itch, but if you find any use to this but are annoyed but the hard-coded values and rules, tell me and I'll fix that.
