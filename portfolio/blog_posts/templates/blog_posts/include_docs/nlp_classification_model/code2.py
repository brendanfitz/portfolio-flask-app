documents = df.story.values
vectorizer = TfidfVectorizer(stop_words="english")
doc_vectors = vectorizer.fit_transform(documents).toarray()
y_true = df.loc[:, 'success']

model = GaussianNB().fit(doc_vectors, y_true)

y_pred = model.predict(doc_vectors)
"Accuracy Score:{:-10.2%}".format(accuracy_score(y_true, y_pred))
