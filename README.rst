Eleanor Rigby Robot
===================

The code powering `@eleanorrigbot`_.

What are you?
-------------

See the `tracking issue`_ in my About repository.

    Eleanor Rigbot, searching for tweets

    That will fit in the scheme of this rhyme

    What will it find?

How to run the bot
------------------

You can install and launch the application using::

    python setup.py install
    launch_rigbot.py

or ``cf push`` it to `Cloud Foundry`_ using the manifest file (note that you
will need to explicitly deactivate the health check, see `the CF docs`_).

For additional configuration, you can pass arguments to the launch script::

    usage: launch_rigbot.py [-h] [--verbose]
                            [--location SW_LON SW_LAT NE_LON NE_LAT] [--version]

    optional arguments:
      -h, --help            show this help message and exit
      --verbose, -v         set the logging level to DEBUG for more output
      --location SW_LON SW_LAT NE_LON NE_LAT, -l SW_LON SW_LAT NE_LON NE_LAT
                            specify a location to filter (defaults to Liverpool)
      --version             show program's version number and exit

Configuration
-------------

The following environment variables must be set to authenticate with the Twitter
API:

- ``TWITTER_API_KEY``
- ``TWITTER_API_SECRET``
- ``TWITTER_ACCESS_TOKEN``
- ``TWITTER_ACCESS_TOKEN_SECRET``

See `the Tweepy Authentication tutorial`_ for more information.

Development
-----------

To install for development, install the package and all of its requirements
with::

    pip install -r requirements.txt
    python setup.py develop

You can run the tests with::

    python setup.py test

.. _@eleanorrigbot: https://twitter.com/eleanorrigbot
.. _Cloud Foundry: https://www.cloudfoundry.org/
.. _the CF docs: https://docs.cloudfoundry.org/devguide/deploy-apps/manifest.html#no-route
.. _the Tweepy Authentication tutorial: http://tweepy.readthedocs.io/en/v3.5.0/auth_tutorial.html
.. _tracking issue: https://github.com/textbook/about/issues/12
