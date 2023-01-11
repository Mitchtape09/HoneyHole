from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_bcrypt import Bcrypt
from flask_app.models.user_model import User
from flask_app.models.spot_model import Spot
from flask_app.models.fish_model import Fish

# our new spots linked page


@app.route('/go/fishing')
def go_fishing():
    return render_template('index copy.html')


@app.route('/spots/desc')
def spots_Desc_page():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    logged_user = User.get_by_id(data)
    all_spots = Spot.spots_Desc()
    context = {
        'logged_user': logged_user,
        'all_spots': all_spots
    }
    return render_template('welcome.html', **context)


@app.route('/spots/asc')
def spots_Asc_page():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    logged_user = User.get_by_id(data)
    all_spots = Spot.spots_Asc()
    context = {
        'logged_user': logged_user,
        'all_spots': all_spots
    }
    return render_template('welcome.html', **context)


@app.route('/spots/new')
def new_spot_form():
    if "user_id" not in session:
        return redirect('/')

    return render_template('spots_new.html')

# the route that pushes are information from the new page and posts to our database/ updates onto dashboard


@app.route('/spots/create', methods=['post'])
def create_spot():
    if "user_id" not in session:
        return redirect('/')
    if not Spot.validator(request.form):
        return redirect('/spots/new')
    spot_data = {
        **request.form,
        'user_id': session['user_id']
    }
    Spot.create(spot_data)
    return redirect('/dashboard')

# route to view any one sasquatch siting if you are the session user


# @app.route('/spots/<int:id>/view')
# def get_one_spot(id):
#     if "user_id" not in session:
#         return redirect('/')
#     data = {
#         'id': id
#     }
#     one_spot = Spot.get_one(data)
#     return render_template('spots_one.html', one_spot=one_spot)


@app.route('/spots/<int:id>/edit')
def edit_spot_form(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        'id': id
    }
    one_spot = Spot.get_one(data)
    return render_template('spots_edit.html', one_spot=one_spot)

# route to update from the changes made in the edit form and updated in our database/dashboard


@app.route('/spots/<int:id>/update', methods=['post'])
def update_spot(id):
    if "user_id" not in session:
        return redirect('/')
    if not Spot.validator(request.form):
        return redirect(f"/spots/{id}/edit")
    update_data = {
        **request.form,
        'id': id
    }
    this_spot = Spot.get_one(update_data)
    if not this_spot.user_id == session['user_id']:
        flash('not yours, hands off')
        return redirect('/dashboard')
    Spot.update(update_data)
    return redirect('/dashboard')

# route to completely remove any information on a single spot from database/dashboard


@app.route('/spots/<int:id>/delete')
def delete_spot(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        'id': id
    }
    this_spot = Spot.get_one(data)
    if not this_spot.user_id == session['user_id']:
        flash('not yours, hands off')
        return redirect('/dashboard')
    Spot.delete(data)
    return redirect('/dashboard')
