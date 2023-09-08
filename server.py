from flask import Flask, render_template, redirect, url_for, request, jsonify, abort, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from dotenv import load_dotenv
from datetime import date
from functools import wraps
from bs4 import BeautifulSoup

import os
import ast

from chat_gpt import chatGPT
from forms import RecipePrompt, NewUser, UserLogin, NewRecipe
from image_processing import download_image, upload_file

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipe-db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)
ckeditor = CKEditor(app)
RECIPE_AI = chatGPT()

# db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        admin_email = os.environ.get("ADMIN_EMAIL")
        if current_user.email != admin_email:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

    recipes = db.relationship("Recipe", backref='user')
    # comments = db.relationship("Comment", backref='user')

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text, nullable=True)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=True)
    date_posted = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # comments = db.relationship("Comment", backref='recipe')

# class Comment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.String(250), nullable=False)
#     date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     author_username = db.Column(db.Integer, db.ForeignKey('user.username'), nullable=False)
#     recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

with app.app_context():
    db.create_all()

@app.template_filter('string_to_list')
def string_to_list(list_as_string):
    return eval(list_as_string)

@app.template_filter('custom_split')
def custom_split(data):
    str_data = data
    if data.startswith('['):
        list_data = ast.literal_eval(str_data)
    else:
        list_data = data
    return list_data

@app.template_filter('is_list_check')
def is_list_check(data):
    if type(data) == str:
        return False
    else:
        return True

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
 
@app.route("/")
def home():
    return render_template('index.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    new_user = NewUser()
    if new_user.validate_on_submit():
        if User.query.filter_by(email=new_user.email.data).first():
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))
        new_user_name = request.form.get('name')
        new_user_email = request.form.get('email')
        new_user_username = request.form.get('username')
        new_user_password = generate_password_hash(request.form.get('password'), method='pbkdf2:sha256', salt_length=8)
        new_user = User(email = new_user_email, username = new_user_username, password = new_user_password, name = new_user_name)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("main_feed"))
    else:
        return render_template("register.html", form = new_user, current_user=current_user)

@app.route('/login', methods=["GET", "POST"])
def login():
    login_form = UserLogin()
    if login_form.validate_on_submit():
        if not User.query.filter_by(email=login_form.email.data).first():
            flash("No user associated with that email, try registering!")
            return redirect(url_for('login'))
        email = request.form.get("email")
        user = User.query.filter_by(email = email).first()
        if user:
            password = request.form.get('password')
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('main_feed'))
            else:
                flash("Incorrect Password, try again!")
                return render_template("login.html", form = login_form)
    else:
        return render_template("login.html", form = login_form, current_user=current_user)
    

@app.route("/main_feed")
@login_required
def main_feed():
    all_recipes = Recipe.query.all()
    return render_template("main_feed.html", all_recipes=reversed(all_recipes))

@app.route("/recipe-gen", methods=["POST", "GET"])
@login_required
def ai_generation():
    new_recipe_prompt = RecipePrompt()
    if new_recipe_prompt.validate_on_submit():
        include = new_recipe_prompt.recipe_prompt.data
        exclude = new_recipe_prompt.items_exclude.data
        recipe = RECIPE_AI.recipe_generation(include, exclude)
        soup = BeautifulSoup(recipe, 'html.parser')
        title_element = soup.find('h2')
        title = title_element.text if title_element else "No title found"
        description = str(soup.find('p')) if soup.find('p') else "No description found"

        ingredients_list = soup.find('ul')
        ingredients = [str(ingredient) for ingredient in ingredients_list.find_all('li')] if ingredients_list else []

        instructions_list = soup.find('ol')
        instructions = [str(instruction) for instruction in instructions_list.find_all('li')] if instructions_list else []
        image_urls = RECIPE_AI.image_generation(title, description, ingredients)
        return render_template('display_recipe.html', recipe = recipe, recipe_title = title, recipe_desc = description, instructions = instructions, ingredients = ingredients, images = image_urls)
    
    return render_template('recipe_generation.html', prompt_form = new_recipe_prompt)

@app.route("/new-recipe", methods=["GET", "POST"])
@login_required
def new_recipe():
    new_recipe_form = NewRecipe()
    is_edit = False
    new_recipe_form.set_submit_label(is_edit)
    if new_recipe_form.validate_on_submit():
        title = request.form.get("title")
        description = request.form.get("description")
        ingredients = request.form.get("ingredients")
        instructions = request.form.get("instructions")
        image_urls = RECIPE_AI.image_generation(title, description, ingredients)
        return render_template('display_recipe.html', recipe_title = title, recipe_desc = description, ingredients = ingredients, instructions = instructions, images = image_urls)
        
        # This code allows to download an uploaded image #
        # f = new_recipe_form.uploaded_img.data
        # filename = secure_filename(f.filename)
        # save_point = os.path.join(
        #     app.instance_path, 'photos', filename
        # )
        # f.save(save_point)
        # return redirect(url_for('main_feed'))

    return render_template('new_recipe.html', new_recipe_form = new_recipe_form, is_edit = is_edit)

@app.route("/edit-recipe/<recipe_id>", methods=["GET", "POST"])
@login_required
def edit_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    is_edit = True
    edit_recipe_form = NewRecipe(recipe_id = recipe_id, title=recipe.title, description=recipe.description, ingredients=recipe.ingredients, instructions=recipe.instructions)
    edit_recipe_form.set_submit_label(is_edit)
    if edit_recipe_form.validate_on_submit():
        recipe.title = edit_recipe_form.title.data
        recipe.description = edit_recipe_form.description.data
        recipe.ingredients = edit_recipe_form.ingredients.data
        recipe.instructions = edit_recipe_form.instructions.data    
        db.session.commit()
        return redirect(url_for("main_feed"))
    return render_template ("new_recipe.html", new_recipe_form = edit_recipe_form, is_edit = True, current_user=current_user)

@app.route("/delete-recipe/<recipe_id>", methods=["GET", "POST"])
@login_required
def delete_recipe(recipe_id):
    recipe_to_delete = Recipe.query.filter_by(id=recipe_id).first()
    db.session.delete(recipe_to_delete)
    db.session.commit()
    return redirect(url_for('main_feed'))

@app.route("/save-recipe", methods=["POST"])
@login_required
def save_recipe():
    if request.method == "POST":
        recipe_title = request.form.get('title')
        recipe_desc = request.form.get("description")
        ingredients = request.form.get("ingredients")
        instructions = request.form.get("instructions")
        recipe_id = request.form.get("recipe_id")
        if recipe_id:
            existing_recipe = Recipe.query.get(recipe_id)
            
            if existing_recipe:
                if not existing_recipe.img_url:
                    recipe_image = request.form.get("recipe_image")
                    file_name = download_image(recipe_image, recipe_title)
                    file_url = upload_file(file_name)
                else:
                    file_url = existing_recipe.img_url

                existing_recipe.title = recipe_title
                existing_recipe.description = recipe_desc
                existing_recipe.ingredients = ingredients
                existing_recipe.instructions = instructions
                existing_recipe.img_url = file_url

                db.session.commit()
        else:
            recipe_image = request.form.get("recipe_image")
            file_name = download_image(recipe_image, recipe_title)
            file_url = upload_file(file_name)

            new_recipe = Recipe(
                title=recipe_title,
                description=recipe_desc,
                ingredients=ingredients,
                instructions=instructions,
                img_url=file_url,
                date_posted=date.today().strftime("%B %d, %Y"),
                user_id=current_user.id        
            )
            db.session.add(new_recipe)
            db.session.commit()
        
        return redirect(url_for("main_feed"))

@app.route("/regen_images", methods=["POST"])
@admin_only
def regen_images():
    try:
        data = request.get_json()
        title = data['title']
        description = data['description']
        prompt = f"{title}. {description}. {data['ingredients']}"
        image_urls = RECIPE_AI.image_generation(prompt)
        return jsonify(images=image_urls)
    except Exception as e:
        app.logger.error(f"Error in regen_images route: {e}")
        return jsonify(error=str(e)), 400
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 8080, debug=True)