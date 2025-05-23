from app.forms import RegisterForm, LoginForm, ProfileForm
from app.models import Users, Profile, Favourite
import os
from app import app, db
from flask import request, jsonify, url_for
from flask import send_from_directory, render_template
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy import case, func, literal
import jwt
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
            current_user = Users.query.get(data['id'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return app.send_static_file(os.path.join('assets', filename))



@app.route('/api/register', methods=['POST'])
def register():
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()
    name = request.form.get('name').strip()
    email = request.form.get('email').strip()
    photo = request.files.get('photo')

    print("== Incoming registration ==")
    print("Username:", username)
    print("Raw password:", password)

    if not all([username, password, name, email, photo]):
        return jsonify({"message": "Missing required fields"}), 400

    existing_user = Users.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "Username already exists"}), 409

    filename = secure_filename(photo.filename)
    photo.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    new_user = Users(
        username=username,
        password=password,  # Store raw password
        name=name,
        email=email,
        photo=filename,
        date_joined=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User Successfully added",
        "username": new_user.username,
        "name": new_user.name,
        "email": new_user.email
    }), 201



@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')


    print(f"Incoming username: {username}")
    print(f"Incoming raw password: {password}")

    user = Users.query.filter_by(username=username).first()

    print(f"Found user in DB: {user}")
    if user:
        print(f"Stored hashed password: {user.password}")
        print(f"Password check result: {check_password_hash(user.password, password)}")


    if user and check_password_hash(user.password, password):
        token = jwt.encode({'id': user.id}, app.config['JWT_SECRET_KEY'], algorithm="HS256")
        return jsonify({
            "message": "Login successful",
            "token": token,
            "username": user.username,
            "id": user.id
        }), 200

    return jsonify({"message": "Invalid credentials"}), 401


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    return jsonify({"message": "Logout successful"}), 200

@app.route('/api/profiles', methods=['GET', 'POST'])
@token_required
def profiles(current_user):
    if request.method == 'GET':
        try:
            profiles = Profile.query.order_by(Profile.id.desc()).all()
            results = []

            for p in profiles:
                user = Users.query.get(p.user_id_fk)
                if not user:
                    print(f"Skipping profile {p.id}, user {p.user_id_fk} not found")
                    continue

                # Fallback image if user's image is missing or file not found
                filename = user.photo if user.photo else 'default-user.png'
                photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                photo_url = (
                    url_for('get_image', filename=filename, _external=True)
                    if os.path.exists(photo_path)
                    else url_for('get_image', filename='default-user.png', _external=True)
                )

                results.append({
                    "id": p.id,
                    "user_id": p.user_id_fk,
                    "name": user.name,
                    "photo": photo_url,
                    "description": p.description,
                    "parish": p.parish,
                    "biography": p.biography,
                    "sex": p.sex,
                    "race": p.race,
                    "birth_year": p.birth_year,
                    "height": p.height,
                    "fav_cuisine": p.fav_cuisine,
                    "fav_colour": p.fav_colour,
                    "fav_school_subject": p.fav_school_subject,
                    "political": p.political,
                    "religious": p.religious,
                    "family_oriented": p.family_oriented,
                    "fav_count": p.fav_count
                })

            return jsonify(results), 200

        except Exception as e:
            print("GET /api/profiles error:", e)
            return jsonify({"error": "Internal Server Error"}), 500

    elif request.method == 'POST':
        try:
            profile_count = Profile.query.filter_by(user_id_fk=current_user.id).count()
            if profile_count >= 3:
                return jsonify({"message": "Profile limit reached"}), 403

            data = request.get_json()
            required_fields = [
                'description', 'parish', 'biography', 'sex', 'race',
                'birth_year', 'height', 'fav_cuisine',
                'fav_colour', 'fav_school_subject'
            ]

            if not all(field in data for field in required_fields):
                return jsonify({"message": "Missing required fields"}), 400

            new_profile = Profile(
                user_id_fk=current_user.id,
                description=data['description'],
                parish=data['parish'],
                biography=data['biography'],
                sex=data['sex'],
                race=data['race'],
                birth_year=int(data['birth_year']),
                height=float(data['height']),
                fav_cuisine=data['fav_cuisine'],
                fav_colour=data['fav_colour'],
                fav_school_subject=data['fav_school_subject'],
                political=data.get('political', False),
                religious=data.get('religious', False),
                family_oriented=data.get('family_oriented', False),
            )

            db.session.add(new_profile)
            db.session.commit()
            return jsonify({"message": "Profile added successfully"}), 201

        except Exception as e:
            print("POST /api/profiles error:", e)
            return jsonify({"error": "Internal Server Error"}), 500
        

@app.route('/api/profiles/<profile_id>', methods=['GET'])#done
def get_profile(profile_id):
    profile = Profile.query.get_or_404(profile_id)
    user = Users.query.get(profile.user_id_fk)
    if profile and user:
        return jsonify({
            "id": profile.id,
            "user_id": profile.user_id_fk,
            "name": user.name,
            "email": user.email,
            "photo": user.photo,
            "description": profile.description,
            "parish": profile.parish,
            "biography": profile.biography,
            "sex": profile.sex,
            "race": profile.race,
            "birth_year": profile.birth_year,
            "height": profile.height,
            "fav_cuisine": profile.fav_cuisine,
            "fav_colour": profile.fav_colour,
            "fav_school_subject": profile.fav_school_subject,
            "political": profile.political,
            "religious": profile.religious,
            "family_oriented": profile.family_oriented,
            "fav_count": profile.fav_count
        })

    return jsonify({"message": "Profile doesn't exist."}), 400


@app.route('/api/profiles/<int:user_id>/favourite', methods=['POST'])
@token_required
def favourite_user(current_user, user_id):
    profile = Profile.query.get(user_id)
    if profile.user_id_fk == current_user.id:
        return jsonify({"message": "You cannot favourite yourself."}), 400
    
    if Favourite.query.filter_by(user_id_fk=current_user.id, fav_user_id_fk=user_id).first():
        return jsonify({"message": "User already favourited."}), 409

    fav = Favourite(user_id_fk=current_user.id, fav_user_id_fk=user_id)
    db.session.add(fav)
    profile.fav_count += 1  
    db.session.commit()  
    return jsonify({"message": "User added to favourites."})

@app.route('/api/profiles/<profile_id>/is-favourited', methods=['GET'])
@token_required
def is_favourited(current_user, profile_id):
    fav = Favourite.query.filter_by(user_id_fk=current_user.id, fav_user_id_fk=profile_id).first()
    return jsonify({"isFavourited": bool(fav)})

@app.route('/api/profiles/matches/<profile_id>', methods=['GET'])
@token_required
def get_profile_matches(current_user, profile_id):
    try:
        base = Profile.query.get_or_404(profile_id)

        match_score = (
            case((Profile.fav_cuisine == literal(base.fav_cuisine), 1), else_=0) +
            case((Profile.fav_colour == literal(base.fav_colour), 1), else_=0) +
            case((Profile.fav_school_subject == literal(base.fav_school_subject), 1), else_=0) +
            case((Profile.political == literal(base.political), 1), else_=0) +
            case((Profile.religious == literal(base.religious), 1), else_=0) +
            case((Profile.family_oriented == literal(base.family_oriented), 1), else_=0)
        )

        matches = (
            db.session.query(Profile, match_score.label("match_count"))
            .filter(
                func.abs(Profile.birth_year - base.birth_year) <= 5,
                func.abs(Profile.height - base.height).between(3, 10),
                match_score >= 3
            )
            .all()
        )

        result = []
        for match, match_count in matches:
            result.append({
                "id": match.id,
                "user_id": match.user_id_fk,
                "birth_year": match.birth_year,
                "sex": match.sex,
                "height": match.height,
                "fav_cuisine": match.fav_cuisine,
                "fav_colour": match.fav_colour,
                "parish": match.parish,
                "fav_school_subject": match.fav_school_subject,
                "political": match.political,
                "religious": match.religious,
                "family_oriented": match.family_oriented,
                "fav_count": match.fav_count,
                "match_count": match_count
            })

        return jsonify(result if result else {"message": "No matches found"}), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    

@app.route('/api/search', methods=['GET'])#done
def search_profiles():
    form = SearchForm()
    if form.validate_on_submit():
        name = form.name.data
        birth_year = form.birth_year.data
        sex = form.sex.data
        race = form.race.data

        query = db.session.query(Profile).join(Users, Profile.user_id_fk == Users.id)

        if name:
            query = query.filter(Users.name.ilike(f"%{name}%"))
        if birth_year:
            query = query.filter(Profile.birth_year == birth_year)
        if sex:
            query = query.filter(Profile.sex == sex)
        if race:
            query = query.filter(Profile.race.ilike(f"%{race}%"))

        results = query.all()

        return jsonify([{
            "id": p.id,
            "user_id": p.user_id_fk,
            "name": Users.query.get(p.user_id_fk).name,
            "birth_year": p.birth_year,
            "sex": p.sex,
            "race": p.race
        } for p in results])
    
    return form_errors(form)


@app.route('/api/users/<int:user_id>', methods=['GET'])#done
def get_user(user_id):
    user = Users.query.get_or_404(user_id)
    if user:
        return jsonify({
            "id": user.id,
            "username": user.username,
            "name": user.name,
            "email": user.email,
            "photo": user.photo,
            "date_joined": user.date_joined
        })
    return jsonify({"message": "User doesnt exist"})

@app.route('/api/users/<int:user_id>/favourites', methods=['GET'])
@token_required
def get_user_favourites(current_user, user_id):
    if current_user.id != user_id:
        return jsonify({"message": "Unauthorized"}), 403

    user = Users.query.get_or_404(user_id)
    favs = Favourite.query.filter_by(user_id_fk=user.id).all()
    results = []

    for fav in favs:
        profile = Profile.query.get(fav.fav_user_id_fk)
        if not profile:
            continue

        fav_user = Users.query.get(profile.user_id_fk)
        if not fav_user:
            continue

        filename = fav_user.photo or 'default-user.png'
        photo_url = url_for('get_image', filename=filename, _external=True)

        results.append({
            "id": profile.id,
            "user_id": profile.user_id_fk,
            "name": fav_user.name,
            "photo": photo_url,
            "description": profile.description,
            "parish": profile.parish,
            "race": profile.race,
            "birth_year": profile.birth_year,
            "sex": profile.sex,
            "height": profile.height,
            "fav_cuisine": profile.fav_cuisine,
            "fav_colour": profile.fav_colour,
            "fav_school_subject": profile.fav_school_subject,
            "political": profile.political,
            "religious": profile.religious,
            "family_oriented": profile.family_oriented,
            "fav_count": profile.fav_count
        })

    if results:
        return jsonify(results), 200
    return jsonify({"message": "User has no favourite users"}), 404


@app.route('/api/users/favourites/<int:N>', methods=['GET'])
def top_favourited_users(N):
    try:
        # Join Profile and Users, order by fav_count descending
        results = (
            db.session.query(Profile, Users)
            .join(Users, Profile.user_id_fk == Users.id)
            .order_by(Profile.fav_count.desc())
            .limit(N)
            .all()
        )
        profiles = []
        for profile, user in results:
            profiles.append({
                "id": profile.id,
                "user_id": profile.user_id_fk,
                "name": user.name,
                "email": user.email,
                "photo": user.photo,
                "description": profile.description,
                "parish": profile.parish,
                "biography": profile.biography,
                "sex": profile.sex,
                "race": profile.race,
                "birth_year": profile.birth_year,
                "height": profile.height,
                "fav_cuisine": profile.fav_cuisine,
                "fav_colour": profile.fav_colour,
                "fav_school_subject": profile.fav_school_subject,
                "political": profile.political,
                "religious": profile.religious,
                "family_oriented": profile.family_oriented,
                "fav_count": profile.fav_count
            })

        return jsonify(profiles), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/uploads/<filename>')
def get_image(filename):
    try:
        safe_name = secure_filename(filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_name)

        print("Trying to serve image from:", file_path)
        print("UPLOAD_FOLDER config:", app.config["UPLOAD_FOLDER"])
        print("Directory exists?", os.path.isdir(app.config["UPLOAD_FOLDER"]))
        print("Files in directory:", os.listdir(app.config["UPLOAD_FOLDER"]) if os.path.isdir(app.config["UPLOAD_FOLDER"]) else "Missing")

        if not os.path.exists(file_path):
            print(f"Image not found: {safe_name}")
            return jsonify({"error": "File not found"}), 404

        return send_from_directory(app.config['UPLOAD_FOLDER'], safe_name)
    except Exception as e:
        print("Image loading error:", e)
        return jsonify({"error": "Server error"}), 500


###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
