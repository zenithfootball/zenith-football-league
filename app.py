from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'zenith_secret_key'

# Hardcoded admin login
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'zenith123'

teams = {
    "A": {"name": "Team A", "color": "red", "logo": "a.png", "players": ["Alex", "Aron"]},
    "B": {"name": "Team B", "color": "blue", "logo": "b.png", "players": ["Ben", "Bryce"]},
    "C": {"name": "Team C", "color": "green", "logo": "c.png", "players": ["Carl", "Coby"]},
    "D": {"name": "Team D", "color": "orange", "logo": "d.png", "players": ["Dan", "Drew"]},
    "E": {"name": "Team E", "color": "purple", "logo": "e.png", "players": ["Eli", "Ezra"]},
    "F": {"name": "Team F", "color": "black", "logo": "f.png", "players": ["Finn", "Fred"]}
}

matches = [
    {"home": "A", "away": "B", "home_score": None, "away_score": None},
    {"home": "C", "away": "D", "home_score": None, "away_score": None},
    {"home": "E", "away": "F", "home_score": None, "away_score": None},
]

@app.route("/")
def index():
    return render_template("index.html", teams=teams)

@app.route("/schedule")
def schedule():
    return render_template("schedule.html", matches=matches)

@app.route("/team/<code>")
def team(code):
    team_info = teams.get(code.upper(), None)
    if not team_info:
        return "Team not found", 404
    return render_template("team.html", team=team_info, code=code)

@app.route("/table")
def table():
    standings = {team: {"points": 0, "played": 0} for team in teams}
    for match in matches:
        if match["home_score"] is not None and match["away_score"] is not None:
            standings[match["home"]]["played"] += 1
            standings[match["away"]]["played"] += 1
            if match["home_score"] > match["away_score"]:
                standings[match["home"]]["points"] += 3
            elif match["home_score"] < match["away_score"]:
                standings[match["away"]]["points"] += 3
            else:
                standings[match["home"]]["points"] += 1
                standings[match["away"]]["points"] += 1
    return render_template("table.html", standings=standings, teams=teams)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("edit_scores"))
        else:
            return render_template("admin.html", error="Invalid login")
    return render_template("admin.html")

@app.route("/edit", methods=["GET", "POST"])
def edit_scores():
    if not session.get("admin"):
        return redirect(url_for("admin"))
    if request.method == "POST":
        idx = int(request.form["match_index"])
        matches[idx]["home_score"] = int(request.form["home_score"])
        matches[idx]["away_score"] = int(request.form["away_score"])
        return redirect(url_for("edit_scores"))
    return render_template("edit.html", matches=matches)

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("index"))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
