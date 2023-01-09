import mimetypes
from flask import Flask, jsonify, request, Response
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_marshmallow import Marshmallow
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/digilog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
ma = Marshmallow(app)


class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text(100))
    date = db.Column(db.DateTime, default=datetime.datetime.now)
    # img = db.Column(db.Text, unique=True, nullable=False)
    # mimetype = db.Column(db.Text, nullable=False)

    def __init__(self, title, body):
        self.title = title
        self.body = body


class ArticleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'body', 'date')


article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)


@app.route('/add', methods=['POST'])
def add_article():
    title = request.json['title']
    body = request.json['body']

    articles = Articles(title, body)
    db.session.add(articles)
    db.session.commit()
    return article_schema.jsonify(articles)


@app.route('/get', methods=['GET'])
def get_articles():
    all_articles = Articles.query.all()
    results = articles_schema.dump(all_articles)
    return jsonify(results)


@app.route('/get/<id>/', methods=['GET'])
def post_details(id):
    article = Articles.query.get(id)
    return article_schema.jsonify(article)


@app.route('/update/<id>', methods=['PUT'])
def update_article(id):
    article = Articles.query.get(id)

    title = request.json['title']
    body = request.json['body']

    article.title = title
    article.body = body

    db.session.commit()
    return article_schema.jsonify(article)


@app.route('/delete/<id>', methods=['DELETE'])
def article_delete(id):
    article = Articles.query.get(id)

    db.session.delete(article)
    db.session.commit()
    return article_schema.jsonify(article)


'''@app.route('/upload', methods=['POST'])
def upload():
    pic = request.files['pic']

    if not pic:
        return 'No Picture Uploaded', 400

    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    img = img = pic.read(), mimetype = mimetype, name = filename)
    db.session.add(img)
    db.session.commit()
    return 'Image uploaded', 200
'''

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
