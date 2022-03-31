from datetime import datetime
def activeness(reviewer_activeness):
    rev_act=dict()
    for key in reviewer_activeness:
        start_date = datetime.strptime(reviewer_activeness[key].split(".")[0], '%Y-%m-%d %H:%M:%S')
        end_date = datetime.now()
        num_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
        rev_act[key] = num_months
    rev_act = dict(sorted(rev_act.items(), key=lambda item: item[1],reverse=True))
    return rev_act