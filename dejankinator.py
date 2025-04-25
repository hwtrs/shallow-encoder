# Usage: python3 dejankinator.py {arg1: input-file name} {arg2: output-file name}
# Example: python3 dejankinator.py latimes latimes_parsed.txt
#   This properly converts the latimes compendium into the proper format to be
#   used in the JASSJr search scripts

import re
import sys


def extract_text_from_docs(doc):
    docs = re.findall(r"<DOC>.*?</DOC>", doc, re.DOTALL)
    formatted_docs = []

    for i, doc in enumerate(docs):
        text_matches = re.findall(r"<TEXT>.*?</TEXT>", doc, re.DOTALL)
        text_content = " ".join(re.findall(r"<P>\s*(.*?)\s*</P>", " ".join(text_matches), re.DOTALL))

        formatted_doc = f"<DOC>\n <DOCNO> {i} </DOCNO>\n {text_content}\n </DOC>\n"
        formatted_docs.append(formatted_doc)

    return "\n".join(formatted_docs)

with open(sys.argv[1], "r", encoding="utf-8") as file:
    document = file.read()

#output = extract_text_from_docs(document)
output = "hello"


with open(sys.argv[2], "w", encoding="utf-8") as file:
    file.write(output)


print("Extraction complete")
