# -*- coding: utf-8 -*-
from chanjo.compat import itervalues


def group_by_field(results, name='field_id'):
    """Group items based on the initial field.

    Args:
        results (List[tuple]): list of fields to group
        name (Optional[str]): what to call the first field

    Returns:
        List[dict]: grouped dicts
    """
    groups = {}
    # loop over results
    for field_id, metric, value in results:
        if field_id not in groups:
            # init a new group
            groups[field_id] = {name: field_id}
        # store the metric under the correct group
        groups[field_id][metric] = value

    return itervalues(groups)


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
