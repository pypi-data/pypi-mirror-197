from sklearn.metrics import (
    roc_auc_score
)

def calculate_abroca(clf, X_test_advantaged_group, 
y_test_advantaged_group,X_test_disadvantaged_group, y_test_disadvantaged_group 
):
    """
    Function calculates abroca
    """
    pred_adv = clf.predict(X_test_advantaged_group)
    auc_advantaged_group = roc_auc_score(y_test_advantaged_group, pred_adv)

    pred_disadv = clf.predict(X_test_disadvantaged_group)
    auc_disadvantaged_group = roc_auc_score(y_test_disadvantaged_group, pred_disadv)

    abroca = auc_advantaged_group - auc_disadvantaged_group

    return abroca
