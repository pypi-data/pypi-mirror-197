from sklearn.metrics import (
    recall_score
)

def calculate_equal_opportunity(clf, X_test_advantaged_group, 
y_test_advantaged_group,X_test_disadvantaged_group, y_test_disadvantaged_group 
):
    """
    Function calculates equal opportunity
    """
    pred_adv = clf.predict(X_test_advantaged_group)
    recall_advantaged_group = recall_score(y_test_advantaged_group, pred_adv)
    
    pred_disadv = clf.predict(X_test_disadvantaged_group)
    recall_disadvantaged_group = recall_score(y_test_disadvantaged_group, pred_disadv)

    equal_opportunity = recall_disadvantaged_group - recall_advantaged_group

    return equal_opportunity