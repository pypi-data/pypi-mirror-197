from sklearn.metrics import (
    precision_score
)

def calculate_predictive_parity(clf, X_test_advantaged_group, 
y_test_advantaged_group,X_test_disadvantaged_group, y_test_disadvantaged_group 
):
    """
    Function calculates predictive parity
    """
    pred_adv = clf.predict(X_test_advantaged_group)
    predicison_advantaged_group = precision_score(y_test_advantaged_group, pred_adv)

    pred_disadv = clf.predict(X_test_disadvantaged_group)
    predicison_disadvantaged_group = precision_score(y_test_disadvantaged_group, pred_disadv)

    predictive_parity = predicison_advantaged_group - predicison_disadvantaged_group

    return predictive_parity
