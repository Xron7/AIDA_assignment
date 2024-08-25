# gets the api key from the text file
def get_key(file="api_key.txt"):
    f = open(file, "r")
    api_key = f.read().strip()
    f.close()
    return api_key


# simplifies a sentence (removes he/his/him and who/that/which etc.)
def simplify_text(text, client):
    prompt = "Transform the following sentences by replacing all pronouns (e.g., he, she, it, they, his, her, their) and relative clauses (e.g., who, that, which) with the corresponding actual entities, ensuring that the text remains grammatically correct and clear. Focus on maintaining the original meaning while explicitly stating each entity."
    request = "Please simplify the sentence I will give you in the next message. Return ONLY the simplified sentence"
    completion = client.chat.completions.create(
        model="ft:gpt-4o-mini-2024-07-18:personal::A0BlPz97",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": request},
            {"role": "user", "content": text}
        ]
    )

    return completion.choices[0].message.content
