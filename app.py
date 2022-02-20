# Use Flask to render a template, redirecting to another url and creating a url
from flask import Flask, render_template, redirect, url_for
# use PyMongo to interact with Mongo database
from flask_pymongo import PyMongo
# use scraping code, we will convert from Jupyter notebook to Python
import scraping

# Set up Flask and create a new instance called app
app = Flask(__name__, template_folder = "templates")

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Set-up app routes
# Set-up home page
@app.route("/")
def index():
   # Use PyMongo to fine "mars" collection in our database; assign that path to mars variable for later
   mars = mongo.db.mars.find_one()
   # Tells flask to return html template using an index.html file; mars = mars tells Python to use "mars" collection in MongoDB
   return render_template("index.html", mars=mars)

# Set-up scraping route
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   # Create variable to hold newly scraped data (references scrape_all function in scraping.py file from jupyter notebook); update database
   mars_data = scraping.scrape_all()
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)

# Tell Flask to run
if __name__ == "__main__":
   app.run()