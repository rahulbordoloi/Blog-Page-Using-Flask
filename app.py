from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'       # tell our flask app where our database is gonna be stored, 'SQLALCHEMY_DATABASE_URI' - path to where our database is stored
db = SQLAlchemy(app)                                               # /// - relative path to app.py, //// - absolute path

# Model View Controller - Structure for WebD => structure the data in our DB
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)            # This field cannot be NULL
    content = db.Column(db.Text, nullable = False)
    author = db.Column(db.String(20), nullable = False, default = 'N/A')
    date_posted = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
    
    def __repr__(self):                                            # print out whenever we create a new blogpost
        return 'Blog Post ' + str(self.id)


@app.route('/')                                                    # url of the website
def index():
    return render_template('index.html')                           # raw tag , or render the html file as a template

@app.route('/posts', methods = ['GET', 'POST'])
def posts():

    if request.method =='POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)    # new post object
        db.session.add(new_post)
        db.session.commit()                                        # to get the features from being in the current state to permanent state
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()    # getting data from the database
        return render_template('posts.html', posts = all_posts)    # getting, sending variables from our flask app to our frontend using templates using jinga control flow statement

#@app.route('/home/<string:name>')                                 # variable type and name  
@app.route('/home/users/<string:name>/posts/<int:id>')             # dynamic URLs
def hello(name, id):
    return "Hello, " + name + ", your id is: " + str(id)

@app.route('/onlyget', methods=['POST'])                           # limiting our webpages to specific request methods , (routing)
def get_req():                                                     # allow webpage to only get requests, doesn't allow put, post, push
    return 'You can only get this webpage.'

@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)                           # get_or_404 -> because if it doesn't exist we don't want to break our code
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    
    post = BlogPost.query.get_or_404(id)

    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post = post)

if __name__ == "__main__":
    app.run(debug=True)                                            # breakdown our errors (debug)

# Dynamic files - HTML
# Static files - CSS, JavaScript
# 1:41:08