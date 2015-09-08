# -*- coding: utf-8 -*-
import logging

from .models import Sample

logger = logging.getLogger(__name__)


def filter_samples(query, group_id=None, sample_ids=None):
    """Filter a query to a subset of samples.

    Will return an unaltered query if none of the optional parameters
    are set. `group_id` takes precedence over `sample_ids`.

    Args:
        query (Query): SQLAlchemy query object
        group_id (Optional[str]): sample group identifier
        sample_ids (Optional[List[str]]): sample ids

    Returns:
        Query: filtered query object
    """
    if group_id:
        logger.debug('filter based on group')
        return query.filter(Sample.group_id == group_id)
    elif sample_ids:
        logger.debug('filter based on list of samples')
        return query.filter(Sample.sample_id.in_(sample_ids))
    else:
        return query


def group_by_field(results):
    """Group items based on the initial field.

    Assumes a sorted list of results.

    Args:
        results (List[tuple]): list of fields to group

    Yields:
        str, dict: next group of results along with the group id
    """
    results = iter(results)
    current_group_id, metric, value = next(results)
    group = {metric: value}
    for group_id, metric, value in results:
        if current_group_id != group_id:
            yield current_group_id, group
            # reset the group
            current_group_id = group_id
            group = {}
        # store the metric under the correct group
        group[metric] = value
    yield current_group_id, group


def predict_gender(x_coverage, y_coverage):
    """Make a simple yet accurate prediction of a samples gender.

    The calculation is based on the average coverage across the X and Y
    chromosomes. Note that an extrapolation from a subsection of bases is
    usually quite sufficient.

    Args:
        x_coverage (float): estimated average coverage on X chromosome
        y_coverage (float): estimated average coverage on Y chromosome

    Returns:
        str: prediction, ['male', 'female', 'unknown']
    """
    # algoritm doesn't work if coverage is missing for X chromosome
    if x_coverage == 0:
        return 'unknown'
    # this is the entire prediction, it's usually very obvious
    elif (y_coverage > 0) and (x_coverage / y_coverage < 10):
        return 'male'
    else:
        # the few reads mapping to the Y chromosomes are artifacts
        return 'female'
