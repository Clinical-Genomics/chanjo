# -*- coding: utf-8 -*-
import datetime

DB_NAME = 'coverage.ccds15.grch37p13.extended.sqlite3'
DATABASE_URL = "https://s3.eu-central-1.amazonaws.com/chanjo/{}".format(DB_NAME)
BED_URL = ("https://s3.eu-central-1.amazonaws.com/"
           "chanjo/ccds15.grch37p13.extended.bed.zip")
CCDS_DATE = datetime.date(2015, 5, 12)

ARCHIVE = {}
