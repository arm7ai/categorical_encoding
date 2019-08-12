import featuretools as ft
from category_encoders import LeaveOneOutEncoder as LeaveOneOut

from categorical_encoding.primitives import LeaveOneOutEnc


class LeaveOneOutEncoder():
    """
        Maps each categorical value to one column using LeaveOneOut encoding.

        Parameters:
        cols: [str]
            list of column names to encode.

        Functions:
        fit:
            fits encoder to data table
            returns self
        transform:
            encodes matrix and updates features accordingly
            returns encoded matrix (dataframe)
        fit_transform:
            first fits, then transforms matrix
            returns encoded matrix (dataframe)
        get_mapping:
            gets the mapping for the LeaveOneOut encoder. Only takes strings of the column name, not the index number.
            returns mapping (dict)
    """

    def __init__(self, cols=None):
        self.encoder = LeaveOneOut(cols=cols)

    def fit(self, X, y):
        self.encoder.fit(X, y)
        return self

    def transform(self, X, features):
        X_new = self.encoder.transform(X)
        feature_names = []
        for feature in features:
            for fname in feature.get_feature_names():
                feature_names.append(fname)
        X_new.columns = feature_names
        return X_new

    def fit_transform(self, X, features, y=None):
        return self.fit(X, y).transform(X, features)

    def get_mapping(self, category):
        return self.encoder.mapping[category]

    def encode_features_list(self, X, features):
        feature_list = []
        for f in features:
            if f.get_name() in self.encoder.cols:
                f = ft.Feature([f], primitive=LeaveOneOutEnc(self, f.get_name()))
            feature_list.append(f)
        return feature_list
