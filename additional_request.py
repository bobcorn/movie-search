# Import necessary packages
from elasticsearch import Elasticsearch

es = Elasticsearch("127.0.0.1", port=9200)

# Get the list of the first 20 movies that best match the word “robots” in both the plot and fullplot, and that have
# been published after year 2000. Boost the results by multiplying the standard score with the average between
# IMDb and Rotten Tomatoes ratings.
body = {
    "query": {
        "function_score": {
            "query": {
                "bool": {
                    "must": [
                        {
                            "multi_match": {
                                "query": "robots",
                                "fields": ["plot", "fullplot"]
                            }
                        },
                        {
                            "range": {
                                "year": {
                                    "gte": 2000
                                }
                            }
                        }
                    ]
                }
            },
            "script_score": {
                "script": {
                    "source": "doc.containsKey('imdb.rating') && doc['imdb.rating'].value > 0.0 \
                    && doc.containsKey('tomatoes.viewer.rating') && doc['tomatoes.viewer.rating'].value > 0.0 \
                    ? (doc['imdb.rating'].value + doc['tomatoes.viewer.rating'].value) / 2 : 1"
                }
            }
        }
    },
    "size": 20
}

res = es.search(body=body, index="movies")

print("\nAdditional request:")
print("\tFound " + str(len(res["hits"]["hits"])) + " results:")
for index, doc in enumerate(res["hits"]["hits"]):
    print("\t\t" + str(index + 1) + ")\tScore: " + str(doc["_score"]),
          "\n\t\t\tTitle: " + doc["_source"]["title"],
          "\n\t\t\tIMDb rating: " + str(doc["_source"]["imdb.rating"]),
          "\n\t\t\tRotten Tomatoes rating: " + str(doc["_source"]["tomatoes.viewer.rating"]))
