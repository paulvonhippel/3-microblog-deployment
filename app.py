from flask import Flask, render_template, request
import datetime
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def create_app(): # This is called an app factory!
    app = Flask(__name__)

    client = MongoClient(os.getenv("MONGODB_URI"))
    app.db = client.microblog
    entries = []

    @app.route("/", methods=["GET","POST"])
    def home():
        print([e for e in app.db.entries.find({})])
        # Invoking fin() with an empty dictionary {} means "fidnd everything"
        if request.method == "POST":
            entry_content = request.form.get("content") # returns something like a dictionary
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            entries.append((entry_content, formatted_date))
            app.db.entries.insert_one({"content": entry_content, "date": formatted_date})
            
        entries_with_date = [
            (
            entry[0], 
            entry[1], 
            datetime.datetime.strptime(entry[1], "%Y-%m-%d").strftime("%b %d")
            )
            for entry in entries
        ]
        print(entries_with_date)
        return render_template("home.html", entries=entries_with_date)
    
    return app

