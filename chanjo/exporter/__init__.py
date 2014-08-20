# -*- coding: utf-8 -*-
"""Component for exporting intervals in the Chanjo-BED format from an
existing Chanjo database.

The component only needs the path to the Chanjo database and performs
the nessesary SQL queries and formatting to transform each interval
to the Chanjo-flavoured BED-format.
"""
from __future__ import absolute_import

from .core import export_intervals
from .producers import fetch_records
