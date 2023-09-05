from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField

from wtforms import StringField, SubmitField, TextAreaField, EmailField, PasswordField, HiddenField
from wtforms.validators import DataRequired, URL, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired

class RecipePrompt(FlaskForm):
    recipe_prompt = StringField("Ingredients to Include (Enter seperated by a comma)", validators=[DataRequired()])
    items_exclude = StringField("Ingredients to Exclude (Enter seperated by a comma)", validators=[DataRequired()])
    submit = SubmitField("Generate Recipe")

class Recipe(FlaskForm):
    title = StringField("Recipe Title", validators=[DataRequired()])
    description = TextAreaField("Recipe Description", validators=[DataRequired()])
    ingredients = TextAreaField("Ingredients", validators=[DataRequired()])
    instructions = TextAreaField("Instructions", validators=[DataRequired()])
    img_url = StringField("Upload File", validators=[DataRequired()])
    save = SubmitField("Save Recipe")

class NewRecipe(FlaskForm):
    recipe_id = HiddenField("Recipe ID")
    title = StringField("Recipe Title", validators=[DataRequired()])
    description = TextAreaField("Recipe Description", validators=[DataRequired()])
    ingredients = CKEditorField("Ingredients", validators=[DataRequired()])
    instructions = CKEditorField("Instructions", validators=[DataRequired()])
    # uploaded_img = FileField("Upload File", validators=[
    #     FileRequired(),
    #     FileAllowed(['jpg', 'png', 'jpeg', 'heic'], 'Images Only!')
    # ])
    save = SubmitField("Generate Recipe Images")

    def set_submit_label(self, is_edit):
        if is_edit:
            self.save.label.text = "Save Changes"
        else:
            self.save.label.text = "Generate Recipe Images"

class NewUser(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired()])
    username = StringField("User Name", validators=[DataRequired()])
    email = EmailField("Email Address", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min= 8)])
    submit = SubmitField("Register")

class UserLogin(FlaskForm):
    email = EmailField("Email Address", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")