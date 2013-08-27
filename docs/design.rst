..  _design:

Design concepts
================
In building Chanjo I've had to make assumptions in designing the package. The following text will set up the premise of why Chanjo looks and behaves the way it does. I will explain my reasons and give the reader an overview of how Chanjo is architected.

Overview
------------------

.. image:: _static/overview.png
   :alt: A brief overview of the workflow

Use of adapters
------------------
I've spent a lot of time testing different possible combinations of element and coverage sources. At one point I was using a binary version of the BED-format called BigBed. This allowed for random access of coverage in a moderately compressed format. However, it turned out to be too slow for even whole exome data and I refocused to get coverage directly from the BAM alignment instead.

The point is that the Core of Chanjo was able to stay the same in spite of these major changes. I believe the architecture in Chanjo makes for a nice separation of concern. Hopefully in the future, development of new adapters will make Chanjo more flexible and/or provide performance benefits.

.. note::
    The decision to use adapters was originally inspired by the front end web framework `Ember.js <http://emberjs.com/>`_. It has a number of adapters developed by both first and third party developers to talk to "any" kind of backend server setup.

Coordinate system
------------------
The world of genomics and bioinformatics is in a bit of a pickle. This is because there currently doesn't exist a defined standard how to reference genomic positions and intervals. The need for standardization has become abundantly clear during the development of Chanjo. A lot of concepts and tasks become unnecessarily complex when you never quite know how software is implemented or database are set up.

* BEDTools, extensively used in bioinformatics, uses a 0,1-based coordinate system for genomic intervals. An analogy would be the python `range` function.

* Now go to your favorite genomics database (CCDS, Ensembl). Chances are they work with arguably the most intuitive 1,1-based coordinates.

* Most programming languages use a 0,0-based system, python included.

* Pysam?

Chanjo's strict use of 0,0-based coordinates is not to be seen as a proposal for how genomics should work. Instead I simply decided to follow the standard in the pythonic environment Chanjo is implemented in. At leasts Chanjo is consistent. 

.. note::
    Anything having dealing with coordinate systems will be clearly stated in source and documentation. 
