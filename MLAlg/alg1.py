from sklearn.feature_selection import SelectKBest, f_classif, chi2

def classify(X, y):
    '''X: data; y: target'''
    kbest = SelectKBest(score_func=f_classif, k=4)
    fit = kbest.fit(X,y)
    features = fit.transform(X)

    return (features, fit.get_support(indices=True))