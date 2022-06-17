import os
import json
from dateutil import parser
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, session, redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost/fakebook'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['SECRET_KEY'] = 'YMyqz0uWN0'
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.config["MAX_IMAGE_FILESIZE"] = 0.5 * 1024 * 1024

db = SQLAlchemy(app)

# Routes
@app.route('/')
def index():
    try:
        if session['logged_in']:
            current_user = CurrentUser.instance(session)
            user = current_user.user
            posts = current_user.get_timeline_posts()
            return render_template('dashboard.html', user=user, posts=posts)
    except:
        return render_template('index.html')

@app.route('/get_posts')
def get_posts():
    try:
        if session['logged_in']:
            current_user = CurrentUser.instance(session)
            user = current_user.user
            posts = current_user.get_timeline_posts()
            return render_template('get_posts.html', user=user, posts=posts)
    except:
        return render_template('index.html')

@app.route('/login', methods=['GET'])
def login():
    try:
        if session['logged_in']:
            return redirect('/')
    except:
        return render_template('login.html')

@app.route('/login', methods=['POST'])
def loginUser():
    try:
        email = request.form['loginemail']
        password = request.form['loginpass']

        user_true = User.query.filter_by(email_address=email, password=password).first()
        if user_true:
            session['user_name'] = email
            session['user_id'] = user_true.id
            session['logged_in'] = True
            return json.dumps({
                'message' : 'success'
            })
        else:
            return json.dumps({
                'message' : 'invalid login'
            })

    except Exception as e:
        return json.dumps({
            'message' : str(e)
        })

@app.route('/register', methods=['GET'])
def register():
    try:
        if session['logged_in']:
            return redirect('/')
    except:
        return render_template('register.html')

@app.route('/register', methods=['POST'])
def registerUser():
    try:
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password1 = request.form['password1']
        gender = request.form['gender']
        dob = request.form['dob']
        pic = request.files['picture']

        user_exists = User.query.filter_by(email_address=email).first()
        if user_exists:
            return json.dumps({
                'message' : 'Email already exists'
            })

        filename = pic.filename
        if '.' not in filename:
            return json.dumps({
                'message' : 'File extension not allowed'
            })

        ext = filename.rsplit(".", 1)[1]
        if ext.upper() not in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
            return json.dumps({
                'message' : 'File extension not allowed'
            })

        user = User(first_name=fname, last_name=lname, email_address=email, password=password1,  gender=gender, dob=dob, profile_picture='temp')
        db.session.add(user)
        db.session.commit()

        file_name = f'{user.id}-{user.first_name}.{(pic.filename).split(".")[-1]}' 

        path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)

        pic.save(path)

        user.profile_picture = file_name
        db.session.commit()

        return json.dumps({
            'message' : 'success'
        })
    except Exception as e:
        return json.dumps({
            'message' : str(e)
        })

@app.route('/post', methods=['POST'])
def newpost():
    try:
        post_text = request.form['post_text']
        user = User.query.filter_by(id=session['user_id']).first()
        photo = request.files['photo']
        if photo:
            post_type = 'special'
            post_factory = PostFactory.get_post(post_type, post_text, user, photo)
            (post, photo) = post_factory.get_post()
            db.session.add(post)
            db.session.commit()
            db.session.add(photo)
            db.session.commit()
        else:
            post_type = 'normal'
            post_factory = PostFactory.get_post(post_type, post_text, user, photo)
            post = post_factory.get_post()
            db.session.add(post)
            db.session.commit()
        
        return json.dumps({
            'message' : 'success'
        })
    except Exception as e:
        print(e)
        return json.dumps({
            'message' : str(e)
        })

@app.route('/logout')
def logout():
    try:
        if session['logged_in']:
            current_user = CurrentUser.instance(session)
            current_user.remove()
            session.pop('logged_in', None)
            session.pop('user_id', None)
            session.pop('user_name', None)
            return redirect('/')
    except:
        return redirect('/')

@app.route('/profile')
def profile():
    try:
        if session['logged_in']:
            user_id = request.args.get('id', default=0)
            user = User.query.filter_by(id=user_id).first()
            if user:
                dateobj = parser.parse(str(user.dob))
                dob = datetime.strftime(dateobj, '%d %b, %Y')
                dateobj = parser.parse(str(user.created_at))
                joined_date = datetime.strftime(dateobj, '%d %b, %Y')
                return render_template('profile.html', user=user, dob=dob, joined_date=joined_date)
            else:
                return render_template('profile.html', user=user)
    except:
        return redirect('/')

@app.route('/requests')
def requests():
    try:
        if session['logged_in']:
            current_user = CurrentUser.instance(session)
            user = current_user.user
            sent_requests = current_user.get_sent_requests()
            recd_requests = current_user.get_received_requests()
            return render_template('requests.html', sent=sent_requests, receive=recd_requests, user=user)
    except Exception as e:
        print(e)
        return redirect('/')

@app.route('/posts')
def posts():
    try:
        if session['logged_in']:
            current_user = CurrentUser.instance(session)
            user = current_user.user
            posts = current_user.get_own_posts()
            return render_template('posts.html', posts=posts, user=user)
    except:
        return redirect('/')

@app.route('/new_friends')
def new_friends():
    try:
        if session['logged_in']:
            current_user = CurrentUser.instance(session)
            user = current_user.user
            users_found = current_user.get_new_friends()            
            return render_template('explore.html', users_found=users_found, user=user)
    except Exception as e:
        print(e)
        return redirect('/')

@app.route('/friends')
def friends():
    try:
        if session['logged_in']:
            current_user = CurrentUser.instance(session)
            user = current_user.user
            friends = current_user.get_friends()
            return render_template('friends.html', friends=friends, user=user)
    except:
        return redirect('/')

@app.route('/sent_request', methods=['POST'])
def sent_frequest():
    try:
        user_id = session['user_id']
        friend_id = request.form.get("friend_id","")
        #To send request using Facade Pattern
        network_manager.send_request(user_id, friend_id)

        return json.dumps({
            'message' : 'success'
        })
    except Exception as e:
        return json.dumps({
            'message' : str(e)
        })

@app.route('/cancel_request', methods=['POST'])
def cancel_request():
    try:
        user_id = session['user_id']
        request_id = request.form.get("request_id","")
        #To cancel request using Facade Pattern
        network_manager.cancel_request(user_id, request_id)

        return json.dumps({
            'message' : 'success'
        })
    except Exception as e:
        return json.dumps({
            'message' : str(e)
        })

@app.route('/remove_request', methods=['POST'])
def remove_request():
    try:
        user_id = session['user_id']
        request_id = request.form.get("request_id","")
        #To remove request using Facade Pattern
        network_manager.remove_request(user_id, request_id)

        return json.dumps({
            'message' : 'success'
        })
    except Exception as e:
        return json.dumps({
            'message' : str(e)
        })

@app.route('/delete_post', methods=['POST'])
def delete_post():
    try:
        post_id = request.form.get("post_id","")
        post = Post.query.filter_by(id=post_id).first()
        db.session.delete(post)
        db.session.commit()
        return json.dumps({
            'message' : 'success'
        })
    except Exception as e:
        return json.dumps({
            'message' : str(e)
        })

@app.route('/accept_request', methods=['POST'])
def accept_request():
    try:
        user_id = session['user_id']
        request_id = request.form.get("request_id","")
        #To accept request using Facade Pattern
        network_manager.accept_request(user_id, request_id)
        return json.dumps({
            'message' : 'success'
        })
    except Exception as e:
        return json.dumps({
            'message' : str(e)
        })

@app.route('/remove_friend', methods=['POST'])
def remove_friend():
    try:
        user_id = session['user_id']
        friend_id = request.form.get("friend_id","")

        my_friend = Friend.query.filter_by(user_id=user_id, friend_id=friend_id).first()
        db.session.delete(my_friend)
        db.session.commit()

        his_friend = Friend.query.filter_by(user_id=friend_id,friend_id=user_id).first()
        db.session.delete(his_friend)
        db.session.commit()
        return json.dumps({
            'message' : 'success'
        })
    except Exception as e:
        return json.dumps({
            'message' : str(e)
        })


@app.route('/like_post', methods=['POST'])
def like_post():
    try:
        user_id = session['user_id']
        post_id = request.form.get("post_id","")
        #Like command
        action.execute('like', user_id, post_id)
        return json.dumps({
            'message' : 'success'
        })
    except Exception as e:
        return json.dumps({
            'message' : str(e)
        })

@app.route('/unlike_post', methods=['POST'])
def unlike_post():
    try:
        user_id = session['user_id']
        post_id = request.form.get("post_id","")
        #Unlike command
        action.execute('unlike', user_id, post_id)
        return json.dumps({
            'message' : 'success'
        })
    except Exception as e:
        return json.dumps({
            'message' : str(e)
        })

if __name__ == '__main__':
    from models import *

    #Create tables in db
    db.create_all()

    #Singletom Class
    from singleton.singleton import CurrentUser

    #Abstract Factory Class
    from abstract_factory.post_abstract_factory import PostFactory

    ##Command Pattern
    from command.command import PostClass, LikePostCommand, UnlikePostCommand, Action
    #Receiver
    post_class = PostClass()

    #Commands
    like_command = LikePostCommand(post_class)
    unlike_command = UnlikePostCommand(post_class)

    #Invoker
    action = Action()
    action.register('like', like_command)
    action.register('unlike', unlike_command)

    ##Facade Pattern
    from facade.facade import Facade

    network_manager = Facade()

    app.run(host='0.0.0.0', debug=True)