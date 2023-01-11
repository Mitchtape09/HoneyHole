from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_bcrypt import Bcrypt
from flask_app.models.user_model import User
from flask_app.models.spot_model import Spot
from flask_app.models.fish_model import Fish


@app.route('/fish/new')
def new_fish_form():
    if "user_id" not in session:
        return redirect('/')

    return render_template('fish_new.html')


@app.route('/trophies')
def trophies():
    if "user_id" not in session:
        return redirect('/')

    trophy_fish = Fish.get_all_trophies()
    return render_template('trophies.html', trophy_fish=trophy_fish)


# the route that pushes are information from the new page and posts to our database/ updates onto dashboard


@app.route('/fish/<int:id>/create', methods=['post'])
def create_catch(id):
    # if "user_id" not in session:
    #     return redirect('/')
    # if not Fish.validator(request.form):
    #     return redirect('/fish/new')
    catch_data = {
        **request.form,
        'spot_id': id
    }
    Fish.create(catch_data)
    return redirect('/dashboard')


@app.route('/fish/<int:id>/add_catch')
def add_fish_form(id):
    if "user_id" not in session:
        return redirect('/')

    return render_template('fish_new.html', spot_id=id)


@app.route('/spots/<int:id>/view')
def get_one_spot(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        'id': id
    }
    one_spot = Spot.get_one(data)

    return render_template('spots_one.html', one_spot=one_spot)


@app.route('/trophy/<int:id>/delete')
def delete_catch(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        'id': id
    }
    this_catch = Fish.get_one(data)
    if not this_catch.spot_id == session['user_id']:
        flash('not yours, hands off')
        return redirect('/dashboard')
    Fish.delete(data)
    return redirect('/dashboard')
