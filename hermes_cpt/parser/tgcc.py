"""
.. module:: hermes_cpt.parser.tgcc.py
   :copyright: Copyright "Sep 21, 2019", Institute Pierre Simon Laplace
   :license: GPL/CeCIL
   :platform: Unix
   :synopsis: TGCC CPT file parser.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.fr>


"""
import datetime as dt

from collections import OrderedDict

import hermes_cpt as hcpt



def get_consumption(cpt):
    """Yields conso blocks from a TGCC consumption (cpt) file.

    """
    return [_map_project_consumption(i) for i in _yield_cpt_of_project(cpt)]


def _map_project_consumption(cpt):
    """Maps CPT content to resource consumption by project.

    """
    # Extract data from cpt file.
    consumption = [_map_machine_consumption(i) for i in _yield_cpt_of_machine(cpt)]
    project = cpt[0].split(' ')[3]
    project_end_date = dt.datetime.strptime(cpt[-1].split(' ')[-1], "%Y-%m-%d")
    project_start_date = dt.datetime(dt.datetime.utcnow().year, 01, 01)

    obj = OrderedDict()
    obj['hpc'] = OrderedDict()
    obj['hpc']['name'] = hcpt.HPC_TGCC
    obj['project'] = OrderedDict()
    obj['project']['name'] = project
    obj['project']['end_date'] = project_end_date
    obj['project']['start_date'] = project_start_date
    obj['consumption_by_machine'] = consumption

    return obj


def _map_machine_consumption(cpt):
    """Maps CPT content to resource consumption by machine.

    """
    # Extract data from cpt file.
    allocation = [i.split(' ')[-1] for i in cpt if i.lower().startswith('allocated')][-1]
    allocation_date = dt.datetime.strptime(cpt[0].split(' ')[-1], "%Y-%m-%d")
    name = cpt[0][cpt[0].index('on'): cpt[0].index('at')][3:-1]
    consumption = [_map_user_consumption(i) for i in _yield_cpt_of_users(cpt)]

    obj = OrderedDict()
    obj["machine"] = OrderedDict()
    obj["machine"]["name"] = name
    obj["machine"]["allocation"] = float(allocation)
    obj["machine"]["allocation_date"] = allocation_date
    obj["consumption_by_sub_project"] = consumption

    return obj


def _map_user_consumption(cpt):
    """Maps CPT content to resource consumption by user.

    """
    # Extract data from cpt file.
    consumption = [(i[0], float(i[-1])) for i in cpt]
    sub_project = None if not cpt or not len(cpt[0]) == 3 else cpt[0][1]

    obj = OrderedDict()
    obj["sub_project"] = sub_project
    obj["consumption_by_user"] = [{
        'login': i,
        'hours_consumed': j
        } for i, j in consumption]

    return obj


def _yield_cpt_of_project(cpt):
    """Yields CPT content at project level.

    """
    # A CPT file contains multiple project related sub-slices derived
    # by identifying lines: Project deadline YYYY-MM-DD.
    indexes = [i for i, v in enumerate(cpt) if v.lower().startswith('project deadline')]
    for i in indexes:
        idx_from = 0 if indexes.index(i) == 0 else indexes[indexes.index(i) - 1] + 1
        yield cpt[idx_from: i + 1]


def _yield_cpt_of_machine(cpt):
    """Yields CPT content at machine level.

    """
    # A CPT file contains multiple accounting related sub-slices derived
    # by identifying lines beginning: Accounting for project.
    indexes = [i for i, v in enumerate(cpt) if v.lower().startswith('accounting for project')]
    for i in indexes:
        idx_to = len(cpt) if indexes.index(i) + 1 == len(indexes) else indexes[indexes.index(i) + 1]
        yield cpt[i: idx_to]


def _yield_cpt_of_users(cpt):
    """Yields CPT content at user level.

    """
    # A CPT file contains multiple lines of resource consumption
    # in hours per login.
    indexes = [i for i, v in enumerate(cpt) if v.lower().startswith('login')]
    for i in indexes:
        idx_to = len(cpt) if indexes.index(i) + 1 == len(indexes) else indexes[indexes.index(i) + 1]
        lines = [j.split(' ') for j in cpt[i + 1: idx_to] if j == j.lower()]
        lines = [[l for l in k if len(l)] for k in lines]

        yield lines


# Previous output - TODO remove
# for start, end in _get_indexes(cpt):
#     consumption = _get_consumption(cpt, start, end)
#     yield {
#         'machine': cpt[start].split()[5].lower(),
#         'node': cpt[start].split()[6].lower(),
#         'consumption_date': dt.datetime.strptime(
#             "{} 23:59:59".format(cpt[start].split()[-1]), "%Y-%m-%d %H:%M:%S"),
#         'consumption': consumption,
#         'project': cpt[start].split()[3].lower(),
#         'project_allocation': float(cpt[end - 3].split()[-1]),
#         'project_end_date': dt.datetime.strptime(cpt[end].split()[-1], "%Y-%m-%d"),
#         'project_start_date': dt.datetime(_YEAR, 01, 01),
#         'project_total': float(cpt[end - 4].split()[-1]),
#         'subtotals': _get_subtotals(consumption)
#     }
