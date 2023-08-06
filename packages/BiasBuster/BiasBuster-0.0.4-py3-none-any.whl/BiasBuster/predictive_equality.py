from sklearn.metrics import (
    confusion_matrix
)

def calculate_predictive_equality(clf, X_test_advantaged_group, 
y_test_advantaged_group,X_test_disadvantaged_group, y_test_disadvantaged_group 
):
    """
    Function calculates predictive equality
    """
    pred_adv = clf.predict(X_test_advantaged_group)
    tn, fp, fn, tp = confusion_matrix(y_test_advantaged_group, pred_adv).ravel()
    FPR_advantaged_group = fp / (fp + tn)

    pred_disadv = clf.predict(X_test_disadvantaged_group)
    tn, fp, fn, tp = confusion_matrix(y_test_disadvantaged_group, pred_disadv).ravel()
    FPR_disadvantaged_group = fp / (fp + tn)

    predictive_equality = FPR_disadvantaged_group - FPR_advantaged_group

    return predictive_equality
