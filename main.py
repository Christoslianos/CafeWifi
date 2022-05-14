from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
from sqlalchemy import Boolean, Column, Integer


def make_bool(val: int) -> bool:
    return bool(int(val))


app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
db = SQLAlchemy(app)
Bootstrap(app)


##create form
class CafeForm(FlaskForm):
    name = StringField('Cafe name', validators=[DataRequired()])
    coffee_price = StringField('Coffee price', validators=[DataRequired()])
    seats = StringField('Number of seats', validators=[DataRequired()])
    map_url = StringField("Direction", validators=[DataRequired(), URL()])
    location = StringField("Location", validators=[DataRequired()])
    img_url = StringField("Cafe photo", validators=[DataRequired(), URL()])
    has_wifi = StringField("Has wifi", validators=[DataRequired()])
    has_toilet = StringField("Has toilet", validators=[DataRequired()])
    can_take_calls = StringField("Has phone", validators=[DataRequired()])
    has_sockets = StringField("Power availability", validators=[DataRequired()])
    submit = SubmitField('Submit')


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(default=False, server_default="false")
    has_wifi = db.Column(default=False, server_default="false")
    has_sockets = db.Column(default=False, server_default="false")
    can_take_calls = db.Column(default=False, server_default="false")
    coffee_price = db.Column(db.String(60), nullable=True)


# db.create_all()


@app.route("/")
def home():
    cafes = db.session.query(Cafe).all()
    list_of_cafes = []
    for _ in cafes:
        list_of_cafes.append(cafes)
    return render_template("index.html", cafes=list_of_cafes)


@app.route("/add", methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        name = form.name.data
        map_url = form.map_url.data
        img_url = form.img_url.data
        location = form.location.data
        seats = form.seats.data
        has_toilet = bool(form.has_toilet.data)
        has_wifi = bool(form.has_wifi.data)
        has_sockets = bool(form.has_sockets.data)
        can_take_calls = bool(form.can_take_calls.data)
        coffee_price = form.coffee_price.data

        new_cafe = Cafe(name=name,
                        map_url=map_url,
                        img_url=img_url,
                        location=location,
                        seats=seats,
                        has_wifi=has_wifi,
                        has_toilet=has_toilet,
                        has_sockets=has_sockets,
                        can_take_calls=can_take_calls,
                        coffee_price=coffee_price
                        )
        db.session.add(new_cafe)
        db.session.commit()
    return render_template('add.html', form=form)


@app.route("/delete", methods=["DELETE", "GET"])
def delete():
    cafe_id = request.args.get('id')
    cafe = db.session.query(Cafe).get(cafe_id)
    if cafe:
        db.session.delete(cafe)
        db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, port=2800)
