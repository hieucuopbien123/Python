import json
with open("vocab") as f:
        vocab = json.loads(f.read())
list_dict=dict.items(vocab)
list_ham_spam=list(vocab.values())
ham=[]
spam=[]
for x in list_ham_spam:
        ham.append(x[0])
        spam.append(x[1])

print(sorted(range(len(ham)), key=lambda x: ham[x])[-5:])
print(sorted(range(len(spam)), key=lambda x: spam[x])[-5:])
print(vocab)