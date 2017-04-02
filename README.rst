Eleanor Rigby Robot
===================

.. contents:: The code powering `@eleanorrigbot`_.

What is this?
-------------

See the `tracking issue`_ in my About repository.

    Eleanor Rigbot, searching for tweets

    That will fit in the scheme of this rhyme

    What will it find?

Running the bot
---------------

You can install and launch the application using::

    python setup.py install
    launch_rigbot.py

or ``cf push`` it to `Cloud Foundry`_ using the manifest file (note that you
will need to explicitly deactivate the health check, see `the CF docs`_).

The following environment variables must be set to authenticate with the Twitter
API:

- ``TWITTER_API_KEY``
- ``TWITTER_API_SECRET``
- ``TWITTER_ACCESS_TOKEN``
- ``TWITTER_ACCESS_TOKEN_SECRET``

See `the Tweepy Authentication tutorial`_ for more information.

For additional configuration, you can pass arguments to the launch script::

    usage: launch_rigbot.py [-h] [--verbose]
                            [--location SW_LON SW_LAT NE_LON NE_LAT] [--version]

    optional arguments:
      -h, --help            show this help message and exit
      --verbose, -v         set the logging level to DEBUG for more output
      --location SW_LON SW_LAT NE_LON NE_LAT, -l SW_LON SW_LAT NE_LON NE_LAT
                            specify a location to filter (defaults to Liverpool)
      --version             show program's version number and exit

Development
-----------

To install for development, install the package and all of its requirements
with::

    pip install -r requirements.txt
    python setup.py develop

You can run the tests with::

    python setup.py test

Matching other phrases
----------------------

If you would like to match a different phrase, you can use the ``PhraseMatcher``
to create an alternate matcher. For example:

.. code-block:: python

    # https://www.flickr.com/places/info/12591829
    napoli = [13.8509, 40.5360, 14.6697, 41.0201]

    # "when the moon hits your eye like a big pizza pie"
    that_is_amore = PhraseMatcher((3, 3, 3, 3), (None, 'a', None, 'a'))

    start_listening(napoli, that_is_amore)

.. _@eleanorrigbot: https://twitter.com/eleanorrigbot
.. _Cloud Foundry: https://www.cloudfoundry.org/
.. _the CF docs: https://docs.cloudfoundry.org/devguide/deploy-apps/manifest.html#no-route
.. _the Tweepy Authentication tutorial: http://tweepy.readthedocs.io/en/v3.5.0/auth_tutorial.html
.. _tracking issue: https://github.com/textbook/about/issues/12
