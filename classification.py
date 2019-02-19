#ID: 220201072
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix


#Determiner,Pronoun_Male,Pronoun_Female,Technical_Word,Relationship_And_Personal_Life,Preposition,Common_Word_Count,Gender

#male 1
#female 0

#importing dataset
scaler = MinMaxScaler()
df= pd.read_csv("gender.csv")
print df['Determiner']
#feature scaling
df[['Determiner','Pronoun_Male','Pronoun_Female','Technical_Word','Relationship_And_Personal_Life','Preposition','Common_Word_Count']]=scaler.fit_transform(df[['Determiner','Pronoun_Male','Pronoun_Female','Technical_Word','Relationship_And_Personal_Life','Preposition','Common_Word_Count']])


#feature matrix
X= df[['Determiner','Pronoun_Male','Pronoun_Female','Technical_Word','Relationship_And_Personal_Life','Preposition','Common_Word_Count']].values

y= df['Gender'].values

"""

#Create Training and Test Sets

X_train, X_test, y_train, y_test= train_test_split(X,y, test_size=.25, random_state=0 ,shuffle=True)

#Building Model
logreg = LogisticRegression()
logreg.fit(X_train, y_train)

print('Accuracy of Logistic regression classifier on training set out of 100%: {:.2f}'    .format(logreg.score(X_train, y_train)*100))
print('Accuracy of Logistic regression classifier on test set out of 100%: {:.2f}'    .format(logreg.score(X_test, y_test)*100))

#predicting a test set result
y_predict= logreg.predict(X_test)

#making a confusion matrix
cm= confusion_matrix(y_test,y_predict ,labels=[0,1])
print "Confusion Matrix:\n"
print cm


#Applying 10-fold cross validation
accurecies= cross_val_score(estimator=logreg, X= X_train, y= y_train, cv=10)
print
print "Cross validation Score List out of 100%:"
print accurecies*100
print
print "Average cross validation Score out of 100%:"
print accurecies.mean()*100
print
print "Varience of accurecies:"
print accurecies.std()



"""



