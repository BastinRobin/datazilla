
from datazilla.model.stats import PushLogStatsModel, PerformanceTestStatsModel
from datazilla.model.base import PushLogModel

def get_not_referenced(project, startdate, enddate, branches=None):
    """Return a list of test runs by in pushlogs not in Datazilla"""

    branches = branches or get_all_branches()

    ptm = PerformanceTestStatsModel(project)
    tr_set = ptm.get_distinct_test_run_revisions()
    ptm.disconnect()

    plm = PushLogStatsModel()
    pl_dict = plm.get_pushlog_dict(startdate, enddate, branches)
    plm.disconnect()

    # gather matching and non-matching sets
    branch_wo_match = {}
    branch_w_match = {}
    for pl, data in pl_dict.iteritems():
        rev_list = data["revisions"]

        if not len(tr_set.intersection(set(rev_list))):
            bucket = branch_wo_match
        else:
            bucket = branch_w_match

        br_list = bucket.setdefault(data["branch_name"], {})
        pushlog_list = br_list.setdefault("pushlogs", [])
        pushlog_list.append({
            "push_id": pl,
            "revisions": rev_list,
            })

    return {
        "with_matching_test_run": branch_w_match,
        "without_matching_test_run": branch_wo_match,
        }


def get_all_branches():
    """Return a list of all the branch names our pushlogs know about"""
    plm = PushLogModel()
    branches = [x["name"] for x in plm.get_all_branches()]
    plm.disconnect()
    return branches


def get_db_size():
    """Return the database size, on disk in MB"""
    plm = PushLogStatsModel()
    size = plm.get_db_size()
    plm.disconnect()
    return size
