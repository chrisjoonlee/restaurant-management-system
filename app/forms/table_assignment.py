from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField


class TableAssignmentForm(FlaskForm):
    tables = SelectField("Tables", coerce=int)
    servers = SelectField("Servers", coerce=int)
    assign = SubmitField("Assign")
