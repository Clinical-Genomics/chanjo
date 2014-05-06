.. Chanjo documentation master file, created by
   sphinx-quickstart on Sun Apr 13 18:46:22 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

mascot
=======
.. raw:: html
   
   <div class="intro__wrapper">
      <div class="logo center-content">
         <img alt="Chanjo Mascot" src="_images/chanjo-logo@2x.png">
      </div>
      <div class="intro">
         <h1>Chanjo</h1>
         <div class="sub-header">Coverage analysis for clincal sequencing</div>
       </div>
     </div>
   </div>


Simple & intuitive analysis pipeline
--------------------------------------
Chanjo introduces a new coverage metric, an intuitive abstraction layer, a pipeable command line interface, and a clear path forward.

.. code-block:: console

   $ cat intervals.bed
   1  10 15 interval-1
   2  45 55 interval-2
   $ cat intervals.bed | chanjo annotate alignment.bam
   #{"sample_id": "bavewira", ...}
   1  10 15 interval-1  9.92231     0.97231
   2  45 55 interval-2  14.23123 1.0

.. raw:: html

   <a href="introduction.html" class="button--big">
      <div class="button__body">Check out the demo</div>
   </a>


Contents
---------

.. toctree::
   :maxdepth: 1

   installation
   introduction
   interface
   code
   developer
   release-notes
   FAQ


made by
--------

.. raw:: html

   <a href="http://www.robinandeer.com/" class="outro">
      <div class="intro">
         <img class="robinandeer-logo" src="_static/robinandeer-logo@2x.png" />
         <div class="sub-header title">Made by Robin Andeer</div>
      </div>
   </a>
