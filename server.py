from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Engine, UserAccount

Base.metadata.create_all(Engine)

DBsession = sessionmaker(bind=Engine)
session = DBsession()

app = Flask(__name__)


app.run(
    secret_key='super',
    debug=True,
    host='0.0.0.0',
    port=8080,
    use_reloader=True
)