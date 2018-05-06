import json

def load_tweets(file, skip):
    with open(file, 'r') as f:
        tweets = (json.loads(line) for i, line in enumerate(f.readlines()) if i % skip == 0)
    return tweets


tweets = load_tweets("../../datasets/DMM/airlines-1465230427503.json", 1)

data = {"id": [], 'text': [], 'screen_name': [], 'created_at': [], 'len': [], 'user': [], "in_reply_to_status_id": []}

for t in tweets:

    if len(t) < 22:
        continue
    else:
        data["id"].append(t["id"])
        data['text'].append(t['text'])
        data['screen_name'].append(t['user']['screen_name'])
        data['created_at'].append(t['created_at'])
        data['len'].append(len(t["text"]))
        data['user'].append(t['user']["id"])
        data["in_reply_to_status_id"].append(t["in_reply_to_status_id_str"])

df = pd.DataFrame(data)

len(df.text[0])
grades = []

for index, row in df.iterrows():
    grades.append(len(row["text"]))

df.groupby(["in_reply_to_status_id"])
american = df['user'] == 22536055

sum(american)
zaza = df[df['text'].notnull() & (df['user'] == 22536055)]