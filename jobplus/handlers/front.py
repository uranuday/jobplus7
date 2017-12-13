from flask import  Blueprint, render_template, flash, redirect, url_for, request, current_app


front = Blueprint('front', __name__)



@front.route('/')
def index():
    print('index')
    return render_template('index.html')







