from flask import Flask, render_template, redirect, flash, url_for
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app =  Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()


connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

@app.route("/")
def list_pets():
    """List A Pet"""
    pets = Pet.query.all()
    return render_template("pet_list.html", pets=pets)

@app.route("/add", methods=["GET","POST"])
def add_pet():
    """Add A Pet"""
    form = AddPetForm()

    if form.validate_on_submit():
        data = {key: value for key, value in form.data.items() if key != "csrf_token"}
        new_pet = Pet(**data)
        db.session.add(new_pet)
        db.session.commit()
        flash("New Pet Added")
        return redirect(url_for('list_pets'))
    else:
        return render_template("pet_add_form.html",form=form)
    
@app.route("/<int:pet_id>", methods=["GET","POST"])
def edit_pet(pet_id):
    """Edit A Pet"""
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.notes = form.notes.data
        pet.available = form.available.data
        pet.photo_url = form.photo_url.data
        db.session.commit()
        flash("Pet Updated")
        return redirect(url_for('list_pets'))
    else:
        return render_template("pet_edit_form.html", form=form, pet=pet)