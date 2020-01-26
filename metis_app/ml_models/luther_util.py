
def my_tokenizer(doc):
    if doc.find(' / ') == -1:
        return doc.split(' ')
    else:
        return doc.split(' / ')
