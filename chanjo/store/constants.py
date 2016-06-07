# -*- coding: utf-8 -*-
COMPLETENESS_LEVELS = [10, 15, 20, 50, 100]
COMPLETENESS_COLUMNS = ["completeness_{}".format(level) for level
                        in COMPLETENESS_LEVELS]
STAT_COLUMNS = ['mean_coverage'] + COMPLETENESS_COLUMNS
