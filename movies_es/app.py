from elasticsearch import Elasticsearch
from flask import Flask, render_template, request

app = Flask(__name__)
es = Elasticsearch("127.0.0.1", port=9200)


@app.route("/")
def home():
    return render_template("search.html")


@app.route("/search/results", methods=["GET", "POST"])
def search_request():
    search_term = request.form["input"]
    if request.form["search"] == "imdb-search":
        search_mode = "imdb-boost"
        query = {
            "function_score": {
                "query": {
                    "multi_match": {
                        "query": search_term,
                        "fields": ["title", "fullplot"]
                    }
                },
                "script_score": {
                    "script": {
                        "source": "doc.containsKey('imdb.rating') && doc['imdb.rating'].value > 0.0 ? doc['imdb.rating'].value : 1"
                    }
                }
            }
        }
    elif request.form["search"] == "tomatoes-search":
        search_mode = "tomatoes-boost"
        query = {
            "function_score": {
                "query": {
                    "multi_match": {
                        "query": search_term,
                        "fields": ["title", "fullplot"]
                    }
                },
                "script_score": {
                    "script": {
                        "source": "doc.containsKey('tomatoes.viewer.rating') && doc['tomatoes.viewer.rating'].value > 0.0 ? doc['tomatoes.viewer.rating'].value : 1"
                    }
                }
            }
        }
    else:
        search_mode = "no-boost"
        query = {
            "multi_match": {
                "query": search_term,
                "fields": ["title", "fullplot"]
            }
        }

    highlight = {
        "fields": {
            "fullplot": {}
        },
        "pre_tags": ["<b>"],
        "post_tags": ["</b>"],
        "fragment_size": 5000
    }

    res = es.search(
        index="movies",
        size=20,
        body={"query": query, "highlight": highlight},
    )
    return render_template("results.html", res=res, search_mode=search_mode)


if __name__ == "__main__":
    app.secret_key = "mysecret"
    app.run(host="0.0.0.0", port=5000)
