from app.forms import RegisterForm, LoginForm, ProfileForm
from app.models import Users, Profile, Favourite
import os
from app import app, db
from flask import request, jsonify, url_for
from werkzeug.utils import secure_filename
from datetime import datetime
from werkzeug.security import check_password_hash
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

@app.route('/api/register', methods=['POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        name = form.name.data
        email = form.email.data
        photo = form.photo.data

        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        new_user = Users(
            username=username,
            password=password,
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
        })

    return jsonify({"message": "Invalid form input"}), 400

@app.route('/api/auth/login', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = Users.query.filter_by(username=username).first()
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
        profiles = Profile.query.order_by(Profile.id.desc()).all()
        results = []
        for p in profiles:
            user = Users.query.get(p.user_id_fk)
            results.append({
                "id": p.id,
                "user_id": p.user_id_fk,
                "name": user.name,
                "photo": url_for('get_image', filename=user.photo, _external=True),
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
        return jsonify(results)

    elif request.method == 'POST':
        profile_count = Profile.query.filter_by(user_id_fk=current_user.id).count()
        if profile_count >= 3:
            return jsonify({"message": "Profile limit reached"}), 403

        form = ProfileForm()
        if form.validate_on_submit():
            new_profile = Profile(
                user_id_fk=current_user.id,
                description=form.description.data,
                parish=form.parish.data,
                biography=form.biography.data,
                sex=form.sex.data,
                race=form.race.data,
                birth_year=form.birth_year.data,
                height=form.height.data,
                fav_cuisine=form.fav_cuisine.data,
                fav_colour=form.fav_colour.data,
                fav_school_subject=form.fav_school_subject.data,
                political=form.political.data,
                religious=form.religious.data,
                family_oriented=form.family_oriented.data,
            )
            db.session.add(new_profile)
            db.session.commit()
            return jsonify({"message": "Profile added successfully"}), 201

        return jsonify({"message": "Invalid form input"}), 400
        

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
            case((Profile.fav_cuisine == base.fav_cuisine, 1), else_=0) +
            case((Profile.fav_colour == base.fav_colour, 1), else_=0) +
            case((Profile.fav_school_subject == base.fav_school_subject, 1), else_=0) +
            case((Profile.political == base.political, 1), else_=0) +
            case((Profile.religious == base.religious, 1), else_=0) +
            case((Profile.family_oriented == base.family_oriented, 1), else_=0)
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
def get_user_favourites(user_id):
    user = Users.query.get_or_404(user_id)
    favs = Favourite.query.filter_by(user_id_fk=user.id).all()
    fav_profiles = [Profile.query.get(fav.fav_user_id_fk) for fav in favs]
    if fav_profiles:
        return jsonify([{
            "id": x.id,
            "user_id": x.user_id_fk,
            "birth_year": x.birth_year,
            "sex": x.sex,
            "height": x.height,
            "race": x.race,
            "description": x.description,
            "fav_cuisine": x.fav_cuisine,
            "fav_colour": x.fav_colour,
            "parish": x.parish,
            "fav_school_subject": x.fav_school_subject,
            "political": x.political,
            "religious": x.religious,
            "family_oriented": x.family_oriented,
            "fav_count": x.fav_count
        } for x in fav_profiles])
    return jsonify({"message": "User has no favourite users"})


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
def uploaded_file(filename):
    return send_from_directory(os.path.join(os.getcwd(), 'uploads'), filename)

@app.route('/uploads/<filename>')
def get_image(filename):
    return send_from_directory('uploads', filename)


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
