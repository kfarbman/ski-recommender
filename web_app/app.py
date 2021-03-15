import pandas as pd
from flask import Flask, jsonify, render_template, request

from recsys import SkiRunRecommender

app = Flask(__name__)

recsys = SkiRunRecommender()


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("home.html")


@app.route("/trails", methods=["GET", "POST"])
def trails():
    """
    Load data for trail recommendations
    """
    df_trails = recsys.load_resort_data()
    return render_template("index.html", df=df_trails)


@app.route("/mountains", methods=["GET", "POST"])
def mountains():
    """
    Load data for mountain recommendations
    """
    df_mountains = recsys.load_resort_data()
    return render_template("mtn_index.html", df=df_mountains)


@app.route("/recommendations", methods=["GET", "POST"])
def recommendations():
    """
    Get and post trail recommendations to web page
    """
    dict_run_requests = {
        "green": ["Green"],
        "blue": ["Green", "Blue"],
        "black": ["Green", "Blue", "Black"],
        "double-black": ["Green", "Blue", "Black", "Double Black"],
    }

    # Default recommendations: runs of all difficulty
    color_lst = dict_run_requests["double-black"]

    # Filter based on max run difficulty requested
    if request.form.get("green"):
        color_lst = dict_run_requests["green"]
    if request.form.get("blue"):
        color_lst = dict_run_requests["blue"]
    if request.form.get("black"):
        color_lst = dict_run_requests["black"]
    if request.form.get("bb"):
        color_lst = dict_run_requests["double-black"]

    # Checkbox functionality
    resort = request.form["resort"]
    if resort == "":
        return "You must select a trail from your favorite resort."
    trail = request.form["trail"]
    if trail != "":
        index = int(trail)
        dest_resort = request.form["dest_resort"]
        num_recs = int(request.form["num_recs"])
        rec_df = recsys.trail_recommendations(
            index, num_recs, dest_resort, color=color_lst
        )
        if dest_resort == "":
            resort_links = recsys.links[resort]
        else:
            resort_links = recsys.links[dest_resort]
        return render_template(
            "recommendations.html", rec_df=rec_df, resort_links=resort_links
        )
    return "You must select a trail."


@app.route("/mtn_recommendations", methods=["GET", "POST"])
def mtn_recommendations():
    """
    Get and post mountain recommendations to web page
    """
    resort = request.form["resort"]
    if resort == "":
        return "You must select a trail from your favorite resort."
    trail = request.form["trail"]
    if trail != "":
        index = int(trail)
        num_recs = int(request.form["num_recs"])

        # Calculate mountain recommendations
        row, recs = recsys.mountain_recommendations(index, num_recs)

        df_mountains = recsys.load_resort_data()

        # Filter DataFrame for mountains in recs
        results_df = df_mountains[df_mountains["Resort"].isin(recs)]

        # Sort mountain recommendations based on cosine similarity
        results_df = results_df.set_index("Resort").loc[recs].reset_index()

        # Get features of original row used for recommendations
        row = row[recsys.MODEL_FEATURES]

        # Create DataFrame of recommendations
        results_df = results_df[recsys.MODEL_FEATURES]
        results_df.drop_duplicates("Resort", keep="first", inplace=True)

        # Remove trail columns before posting to web page
        results_df.drop(
            ["Trail Name", "Difficulty", "Groomed", "Slope Length (ft)"],
            axis=1,
            inplace=True,
        )

        return render_template(
            "mtn_recommendations.html",
            row=row,
            results_df=results_df,
            links=recsys.links,
        )
    return "You must select a trail."


@app.route("/get_trails")
def get_trails():
    resort = request.args.get("resort")
    if resort:
        df = recsys.load_resort_data()

        # Filter trails by resort
        sub_df = df[df["Resort"] == resort]

        # Sort trails by name
        sub_df.sort_values(by="Trail Name", inplace=True)

        # Create index column
        sub_df["index"] = sub_df.index.astype("str")

        # Subset sub_df
        sub_df = sub_df[["index", "Trail Name", "Difficulty"]]

        # Rename columns
        sub_df.rename(
            columns={"index": "id", "Trail Name": "name", "Difficulty": "color"},
            inplace=True,
        )

        # Convert DataFrame to list of dictionaries
        data = sub_df.to_dict("records")

    return jsonify(data)


@app.route("/trail_map/<resort>")
def trail_map(resort):
    resort_image = recsys.links[resort][0]
    return render_template("trail_map.html", resort_image=resort_image)


if __name__ == "__main__":

    # Set cache to dictionary; remove cached template limit
    app.jinja_env.cache = {}

    app.run(host="0.0.0.0", port=8080, debug=True, threaded=True)
