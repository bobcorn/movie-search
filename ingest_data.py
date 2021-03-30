# Import necessary packages
import json

from elasticsearch import Elasticsearch

# Declare client instance
es = Elasticsearch("127.0.0.1", port=9200)

# Open JSON file
file = open("./data/imdb.json", "r", encoding="utf-8")
# Retrieve content
text = file.read()
# Close JSON file
file.close()
# Clean whitespaces
text.strip()
# Split each line
lines = text.split("\n")

# Delete previously created index (if existing)
if es.indices.exists(index="movies"):
    es.indices.delete(index="movies", ignore=[400, 404])

# Create required index
es.indices.create(index="movies", ignore=400)

# Define required fields
strings = ["title", "plot", "fullplot"]
floats = ["imdb.rating", "tomatoes.viewer.rating"]
lists = ["directors", "countries", "genres"]

# Iterate on each line
for line in lines:
    if line != "":
        parsed = None

        # Parse the current line
        try:
            parsed = json.loads(line)
        except Exception as e:
            print("Error parsing: " + line + ". Exception: " + str(e))

        # Create an empty dictionary for the document
        doc = {}

        # Retrieve "title", "plot", "fullplot"
        for field in strings:
            try:
                doc[field] = parsed[field]
            except Exception as e:
                print("Error parsing: " + field + ". Exception: " + str(e))
                doc[field] = ""

        # Retrieve "year"
        try:
            doc["year"] = int(parsed["year"]["$numberInt"])
        except Exception as e:
            print("Error parsing: year. Exception: " + str(e))
            doc["year"] = 0

        # Retrieve "imdb.rating", "tomatoes.viewer.rating"
        for fields in floats:
            temp = parsed
            try:
                for field in fields.split("."):
                    temp = temp[field]
                doc[fields] = float(temp["$numberDouble"])
            except Exception as e:
                print("Error parsing: " + fields + ". Exception: " + str(e))
                doc[fields] = 0.0

        # Retrieve "directors", "countries", "genres"
        for field in lists:
            try:
                doc[field] = list(parsed[field])
            except Exception as e:
                print("Error parsing: " + field + ". Exception: " + str(e))
                doc[field] = []

        # Print retrieved data
        # print(json.dumps(doc, indent=4))

        # Index retrieved data
        try:
            es.index(index="movies", body=doc)
        except Exception as e:
            print("Error indexing: " + str(doc) + ". Exception: " + str(e))
