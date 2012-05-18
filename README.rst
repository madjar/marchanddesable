marchanddesable
===============

Turn off your server when you sleep.

What it does
------------

Give it some IPs, and it will call halt five minutes after the given computers have stopped pinging. Except if we are
in the middle of the day or if we are disconnected from the internet (because we don't want the computer to stop just
because the network went off).

Install
-------

The easiest way is to just grab the file `marchanddesable.py`.

If you want to install it, `Marchanddesable` is on pypi_, so this should do the trick :

    pip install marchanddesable

.. _pypi: http://pypi.python.org/pypi/marchanddesable

Arch users, you can install `marchanddesable` from AUR.

Usage
-----
To halt the current machines 5 minutes after both 192.168.0.1 and 192.168.0.2 stop pinging,
put this in your crontab. It will also log to the given file and rotate every night::

    * * * * *       /home/madjar/marchanddesable.py 192.168.0.2 192.168.0.10 -f /var/log/marchanddesable.log

If you don't like cron, and think running daemon or programs in screen are better, you can use ::

    marchand -l 192.168.0.1 192.168.0.2

TODO
----

These features may or may not be implemented at some point :

- Play a sound to warn when the machines stopped pinging
- A way to tell it not to halt the computer tonight without having to disable it
- A way to change the rules without having to modify the script

If you want any of those, or anything else, give me a shout.
