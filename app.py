from flask import Flask,render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqlite3

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///post.db'

db =SQLAlchemy(app)


super = ('login4.db')

super = sqlite3.connect(super, check_same_thread=False)
su = super.cursor()
su.execute("CREATE TABLE IF NOT EXISTS login_table (id INTEGER PRIMARY KEY,first_name TEXT,mobile TEXT,"
           "email TEXT,login_pass TEXT,re_pass TEXT)")
super.commit()

class BlogPost(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(30),nullable = False)
    content = db.Column(db.Text(80),nullable = False)
    author = db.Column(db.String(20), nullable=False,default = 'N/A')


    def __repr__(self):
        return 'Blog post' + str(id)


data = [
    {
        'title':'Corona cases in India',
        'content': 'The count of corona case in india has increased and now its 1,25,455 ',
        'author':'Shubham narke'
    },
    {
        'title':'Corona cases in Japan',
        'content': 'The count of corona case in india has increased and now its 1,25,455 '
    }
]

@app.route('/')
@app.route('/front')
def login():
    return render_template('front.html')

@app.route('/login_val',methods=['POST'])
def login_vaidation():
    email = request.form.get('email')
    password = request.form.get('pass')
    su.execute("SELECT * FROM login_table WHERE email LIKE '{}' AND login_pass LIKE '{}'".format(email, password))
    result = su.fetchall()
    print(result)
    if len(result)>0:
        return redirect('/home')
    else:
        return redirect('/')




@app.route('/new')
def new():
    return render_template('new.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register_user',methods = ['POST'])
def register_user():
    full_name = request.form.get('full')
    email = request.form.get('email')
    phone = request.form.get('phone')
    pass_word = request.form.get('pass')
    re_pass = request.form.get('re_pass')
    su.execute('INSERT INTO login_table(first_name,mobile,email,login_pass,re_pass) VALUES (?,?,?,?,?)',(full_name,phone,email,pass_word,re_pass))
    super.commit()
    return 'hello'


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/home')
    else:
        data = BlogPost.query.all()

        return render_template('index.html', posts=data)


@app.route('/home/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/home')


@app.route('/home/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/home')
    else:
        return render_template('edit.html',post=post)




if __name__ == "__main__":
    app.run(debug=True)