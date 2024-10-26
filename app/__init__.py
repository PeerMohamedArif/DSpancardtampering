from flask import Flask
from config import Config
import mysql.connector

app=Flask(__name__)

if app.config.get("ENV", "production") == "production":
    app.config.from_object("config.DevelopmentConfig")
elif app.config["ENV"]=="testing":
    app.config.from_object("config.TestingConfig")
else:
    app.config.from_object("config.ProductionConfig")

def get_db_connection():
    return mysql.connector.connect(
        host=app.config["DB_HOST"],
        user=app.config["DB_USERNAME"],
        password=app.config["DB_PASSWORD"],
        database=app.config["DB_NAME"]
    )
from app import views

