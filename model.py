# Import necessary libraries
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score

st.title("Modeling for Assignment")

st.write("""In this section, I will be creating two different machine learning models to predict whether or not a supplier would or would not accept assignment. The first model I will create is going to be a Random Forest classifier, as this model is robust against complex data with many predictors due to its ensemble nature. Because it consists of a collection of decision trees, it will be able to handle data with many predictors like the Medical Equipment Suppliers data with all of the encoded variables. The second model will be a Logistic Regression, since this is a binary classification problem, which is Logistic Regression's specialty.""")

encoded_suppliers = st.session_state.encoded_suppliers

X = encoded_suppliers.drop(columns = [
    "provider_id",
    "acceptsassignement",
    "participationbegindate",
    "businessname",
    "practicename",
    "practiceaddress1",
    "practiceaddress2",
    "practicecity",
    "practicestate",
    "practicezip9code",
    "telephonenumber",
    "specialitieslist",
    "supplieslist",
    "providertypelist"
])

y = encoded_suppliers["acceptsassignement"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

st.write("""To begin with, I created my feature matrix X and outcome vector y. To create X, I removed all columns except for the one-hot encodings of supplies and specialities, accepts_cba, and the longitude/latitude coordinates. The outcome vector y is the accepts_assignement column. The goal of this is to use location and available supplies/specialities to predict accepts_assignement, so these variables were used for the models.""")
st.write(X.head())

rf_model = RandomForestClassifier(n_estimators = 100, random_state = 42)
rf_model.fit(X_train, y_train)

y_pred_rf = rf_model.predict(X_test)
y_prob_rf = rf_model.predict_proba(X_test)[:, 1]

st.write("""The Random Forest Classifier was highly effective, as it was able to accurately capture all of the different one-hot encodings due to its ability to handle complex data. The model's performance on the test set in accuracy and AUROC can be seen below.""")

st.write("Random Forest Accuracy:", accuracy_score(y_test, y_pred_rf))
st.write("Random Forest AUROC:", roc_auc_score(y_test, y_prob_rf))

st.write("""The Logistic Regression was also effective, due to the binary nature of this classification problem, but it was not quite as effective as the Random Forest, with a slightly worse accuracy and much worse AUROC. This suggests that for this dataset, the complexity of its many features outweighs the impact of the classification problem's binary nature, as a model based around addressing complexity outperformed one based around handling binary classification.""")

lr_model = LogisticRegression(max_iter = 1000, random_state = 42)
lr_model.fit(X_train, y_train)

y_pred_lr = lr_model.predict(X_test)
y_prob_lr = lr_model.predict_proba(X_test)[:, 1]

st.write("Logistic Regression Accuracy:", accuracy_score(y_test, y_pred_lr))
st.write("Logistic Regression AUROC:", roc_auc_score(y_test, y_prob_lr))