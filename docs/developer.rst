===================
Developer's Guide
===================
The developer guide is directed to fellow coders. You should read this if:

- you want to contribute to the development of Chanjo
- develop a Chanjo plugin or converter adapter


Contributing
----------------
Currently the best resource on this topic is available at GitHub, in the `CONTRIBUTING.md`_ file.


Develop a plugin
---------------------
Chanjo exposes a couple of plugin interfaces using setuptools entry points.

When publishing a new Chanjo plugin you should register with the corresponding entry point in your ``setup.py`` script. It might look something like this:

.. code-block:: python

  setup(
    name='Chanjo-EnsemblConverter',
    ...
    entry_points={
      'chanjo.converters': [
        'ensembl = chanjo_converter.core:ensembl_to_bed',
      ],
    },
    ...
  )

The setup above with register a new converter adapter as "ensembl" that will point to the function "ensembl_to_bed".

When you write a Chanjo plugin name it something like "Chanjo-MyPlugin" to make it easy to find using ``pip search``.

.. note::
  Remember that it's absolutly OK for plugins to to depend on Chanjo itself or any Chanjo dependencies.


Converter adapters
~~~~~~~~~~~~~~~~~~~
Setuptools entry point: ``chanjo.converters``

The first type of Chanjo plugin is converter adapters. When you install Chanjo, you get the first adapter (ccds) for free as the default option. This adapter maps the CCDS database format to the extended Chanjo BED format. Read more under interface_.

To give you an idea of why this is useful, imagine that you work with exons defined in Ensembl. Considering the ubiquity of this database it's likely that there are many teams working with the same dataset.

This is an ideal point to consider writing a new adapter for ``chanjo convert``. It should essentially be a single function that accepts a stream of lines from whatever files is used as input.

To get a better understanding of what an actual implementation should look like, take a look at the `reference implementation`_ of the default "ccds" adapter.


New subcommand
~~~~~~~~~~~~~~~
Setuptools entry point: ``chanjo.subcommands``

The second type of entry point let's you write a plugin that will show up as an additional subcommand when you type in ``chanjo`` on the command line.

This type of plugin doesn't have any particular limitations as to what they can accomplish. They only requirement is that it should tie into some form of Chanjo functionality like generating a report from a populated SQL database.

When writing a new subcommand for Chanjo you can study any of the built in modules that are all built as if they really were external plugins. Consider for example the `annotator module`_. It consists of a "core" submodule that implements the main pipeline to data defined in BED format. This function works like a black box and you are free to define any I/O that suits you.

A second submodule "cli" contains the actual subcommand implemented using the Click command line framework. As long as you stick to Click, you can do pretty much whatever you want.


License
--------
.. include:: ../LICENSE


.. _CONTRIBUTING.md: https://github.com/robinandeer/chanjo/blob/master/CONTRIBUTING.md
.. _interface: interface.html#convert
.. _reference implementation: https://github.com/robinandeer/chanjo/tree/master/chanjo/converter
.. _annotator module: https://github.com/robinandeer/chanjo/tree/master/chanjo/annotator
