===================
Developer's Guide
===================
The developer guide is directed to fellow coders. You should read this if:

- you want to contribute to the development of Chanjo
- develop a Chanjo plugin that hooks into one of the entry points


Contributing
----------------
Currently the best resource on this topic is available at GitHub, in the `CONTRIBUTING.md`_ file.



Installation/dev environment
-----------------------------
Check out the `installation guide`_ to learn how you can set up a Vagrant environment which is ready to start development in no time!



Develop a plugin
---------------------
Chanjo exposes a couple of plugin interfaces using setuptools entry points.

When publishing a new Chanjo plugin you should register with the corresponding entry point in your ``setup.py`` script. It might look something like this:

.. code-block:: python

  setup(
    name='Chanjo-PluginName',
    ...
    entry_points={
      'chanjo.subcommands.3': [
        'plugin_name = chanjo_plugin.cli:main',
      ],
    },
    ...
  )

The setup above would register a new subcommand to the command line interface as ``chanjo plugin``.

When you write a Chanjo plugin name it something like "Chanjo-MyPlugin" to make it easy to find using ``pip search``.

.. note::
  It's absolutly OK for plugins to to depend on Chanjo itself or any Chanjo dependencies.



New subcommand
---------------
Setuptools entry point: ``chanjo.subcommands.3``

You can write a plugin that will show up as an additional subcommand when you type ``chanjo`` on the command line.

The implementation should use the Click command line framework. As long as you stick to Click, you can do pretty much whatever you want. Let's your imagination run free! The only requirement is that it should tie into some form of Chanjo functionality like generating a report from a populated SQL database.


License
--------
.. include:: ../LICENSE


.. _CONTRIBUTING.md: https://github.com/robinandeer/chanjo/blob/master/CONTRIBUTING.md
.. _installation guide: installation.html
