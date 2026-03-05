from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

# DB Section
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Xoffset = db.Column(db.Float, nullable=False)
    Yoffset = db.Column(db.Float, nullable=False)
    DSKI = db.Column(db.Float, nullable=False)
    AMB = db.Column(db.Float, nullable=False)
    TOP = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Data {self.id}>\n'

# DSKI Section
@app.route('/dski', methods=['GET', 'POST'])
def dskiengine():
    if request.method == 'POST':
        xoffset = request.form.get('xoffset')
        yoffset = request.form.get('yoffset')
        dski = request.form.get('dski')
        new_data = Data(Xoffset=xoffset, Yoffset=yoffset, DSKI=dski)
        db.session.add(new_data)
        db.session.commit()
        flash('Data has been added!', 'success')
        return redirect(url_for('dskiengine'))
    return render_template('dski.html')

# AMB Section
@app.route('/amb', methods=['GET', 'POST'])
def amb():
    if request.method == 'POST':
        amb = request.form.get('amb')
        new_data = Data(AMB=amb)
        db.session.add(new_data)
        db.session.commit()
        flash('Data has been added!', 'success')
        return redirect(url_for('amb'))
    return render_template('amb.html')

# TOP Section
@app.route('/top', methods=['GET', 'POST'])
def top():
    if request.method == 'POST':
        top = request.form.get('top')
        new_data = Data(TOP=top)
        db.session.add(new_data)
        db.session.commit()
        flash('Data has been added!', 'success')
        return redirect(url_for('top'))
    return render_template('top.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)