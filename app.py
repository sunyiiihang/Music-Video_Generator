from flask import Flask, request, render_template
import datetime
import sqlite3
import os
import replicate

os.environ["REPLICATE_API_TOKEN"] = "r8_blgZ1xDcWB5CWFPpVdZdY7rTXVfeooh49nicN"

app = Flask(__name__)

name_flag = 0
name = ""

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/main", methods=["GET", "POST"])
def main():
    global name_flag, name
    if name_flag == 0:
        name = request.form.get("name")
        name_flag = 1
        conn = sqlite3.connect("log.db")
        c = conn.cursor()
        timestamp = datetime.datetime.now()
        c.execute("INSERT INTO employee (name, timestamp) VALUES (?, ?)", (name, timestamp))
        conn.commit()
        c.close()
        conn.close()
    return render_template("main.html", name=name)

@app.route("/music", methods=["GET", "POST"])
def music():
    return render_template("music.html")

@app.route("/music_generator", methods=["POST"])
def music_generator():
    q = request.form.get("q")
    r= replicate.run(
        "meta/musicgen:7be0f12c54a8d033a0fbd14418c9af98962da9a86f5ff7811f9b3423a1f0b7d7",
        input={
            "prompt": q,
            "duration": 5
        }
    )
    return render_template("music_generator.html")

@app.route("/video", methods=["GET", "POST"])
def video():
    return render_template("video.html")

@app.route("/video_generator", methods=["POST"])
def video_generator():
    q = request.form.get("q")
    r = replicate.run(
        "anotherjesse/zeroscope-v2-xl:9f747673945c62801b13b84701c783929c0ee784e4748ec062204894dda1a351",
        input={
            "prompt": q,
            "num_frames": 20
        }
    )
    return render_template("video_generator.html")

@app.route("/end", methods=["GET", "POST"])
def end():
    return render_template("end.html")

if __name__ == "__main__":
    app.run()
