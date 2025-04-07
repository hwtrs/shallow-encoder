import re

def extract_text_from_docs(doc):
    docs = re.findall(r"<DOC>.*?</DOC>", doc, re.DOTALL)
    formatted_docs = []

    for i, doc in enumerate(docs):
        text_matches = re.findall(r"<TEXT>.*?</TEXT>", doc, re.DOTALL)
        text_content = " ".join(re.findall(r"<P>\s*(.*?)\s*</P>", " ".join(text_matches), re.DOTALL))

        formatted_doc = f"<DOC>\n <DOCNO> {i} </DOCNO>\n {text_content}\n </DOC>\n"
        formatted_docs.append(formatted_doc)

    return "\n".join(formatted_docs)

// Un-hardcode this later
with open("latimes.xml", "r", encoding="utf-8") as file:
    document = file.read()

output = extract_text_from_docs(document)

// Un-hardcode this later
with open("smalltimes_output.xml", "w", encoding="utf-8") as file:
    file.write(output)

print("Extraction complete")
