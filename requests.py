# Import necessary packages
from elasticsearch import Elasticsearch

es = Elasticsearch("127.0.0.1", port=9200)

# 1. Get the list of the first 10 movies that have been published between 1939 and 1945 and
# best matches the word "war" in the plot.
body_1 = {
    "query": {
        "bool": {
            "must": [
                {
                    "range": {
                        "year": {
                            "gte": 1939,
                            "lte": 1945
                        }
                    }
                },
                {
                    "match": {
                        "plot": "war"
                    }
                }
            ]
        }
    },
    "size": 10
}

res_1 = es.search(body=body_1, index="movies")

print("\nRequest 1:")
print("\tFound " + str(len(res_1["hits"]["hits"])) + " results:")
for index, doc in enumerate(res_1["hits"]["hits"]):
    print("\t\t" + str(index + 1) + ")\tScore: " + str(doc["_score"]),
          "\n\t\t\tTitle: " + doc["_source"]["title"],
          "\n\t\t\tYear: " + str(doc["_source"]["year"]),
          "\n\t\t\tPlot: " + doc["_source"]["plot"])

# 2. Get the list of the first 20 movies that have an average IMDb rating higher than 6.0 and
# best matches “Iron Man” in the full plot.
body_2 = {
    "query": {
        "bool": {
            "must": [
                {"range": {"imdb.rating": {"gt": 6.0}}},
                {"match": {"fullplot": "Iron Man"}}
            ]
        }
    },
    "size": 20
}

res_2 = es.search(body=body_2, index="movies")

print("\nRequest 2:")
print("\tFound " + str(len(res_2["hits"]["hits"])) + " results:")
for index, doc in enumerate(res_2["hits"]["hits"]):
    print("\t\t" + str(index + 1) + ")\tScore: " + str(doc["_score"]),
          "\n\t\t\tTitle: " + doc["_source"]["title"],
          "\n\t\t\tIMDb rating: " + str(doc["_source"]["imdb.rating"]),
          "\n\t\t\tFull plot: " + doc["_source"]["fullplot"])

# 3. Get the list of the first 20 movies that have an average IMDb rating higher than 6.0 and
# best matches “Iron Man” in the full plot.
body_3_imdb = {
    "query": {
        "function_score": {
            "query": {
                "match": {"title": "matrix"}
            },
            "script_score": {
                "script": {
                    "source": "doc.containsKey('imdb.rating') && doc['imdb.rating'].value > 0.0 \
                    ? doc['imdb.rating'].value : 1"
                }
            }
        }
    }
}

res_3_imdb = es.search(body=body_3_imdb, index="movies")

print("\nRequest 3 (IMDb):")
print("\tFound " + str(len(res_3_imdb["hits"]["hits"])) + " results:")
for index, doc in enumerate(res_3_imdb["hits"]["hits"]):
    print("\t\t" + str(index + 1) + ")\tScore: " + str(doc["_score"]),
          "\n\t\t\tTitle: " + doc["_source"]["title"],
          "\n\t\t\tIMDb rating: " + str(doc["_source"]["imdb.rating"]))

body_3_tomatoes = {
    "query": {
        "function_score": {
            "query": {
                "match": {"title": "matrix"}
            },
            "script_score": {
                "script": {
                    "source": "doc.containsKey('tomatoes.viewer.rating') && doc['tomatoes.viewer.rating'].value > 0.0 \
                    ? doc['tomatoes.viewer.rating'].value : 1"
                }
            }
        }
    }
}

res_3_tomatoes = es.search(body=body_3_tomatoes, index="movies")

print("\nRequest 3 (Rotten Tomatoes):")
print("\tFound " + str(len(res_3_tomatoes["hits"]["hits"])) + " results:")
for index, doc in enumerate(res_3_tomatoes["hits"]["hits"]):
    print("\t\t" + str(index + 1) + ")\tScore: " + str(doc["_score"]),
          "\n\t\t\tTitle: " + doc["_source"]["title"],
          "\n\t\t\tRotten Tomatoes rating: " + str(doc["_source"]["tomatoes.viewer.rating"]))
