from flask import Flask
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for
from flask.ext.pymongo import PyMongo
import logging
from logging.handlers import RotatingFileHandler
import datetime

app = Flask(__name__)

handler = RotatingFileHandler('logs/blogservice.log', maxBytes=40960, backupCount=3)
handler.setLevel(logging.DEBUG)
app.logger.addHandler(handler)
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)
log.addHandler(handler)

# connect to mongo with defaults
mongo = PyMongo(app)

debug = True


def epr(s):
    app.logger.error(s)
    if(debug):
        print s


def dpr(s):
    app.logger.debug(s)
    if(debug):
        print s


def make_public_blog(blog):
    new_blog = {}
    for field in blog:
        if field == 'id':
            new_blog['uri'] = url_for(
                'get_blog',
                blog_id=blog['id'],
                _external=True
                )
        if field == '_id':
            pass
        else:
            try:
                new_blog[field] = blog[field]
            except Exception as e:
                epr("{} - {}".format(field, e))
    return new_blog


@app.errorhandler(404)
def not_found(error):
    epr("404 not found")
    return make_response(jsonify({'error': 'not found'}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'bad request'}), 400)


@app.errorhandler(409)
def duplicate_resource(error):
    return make_response(jsonify({'error': 'duplicate resource id'}), 409)


@app.errorhandler(500)
def internal_server_error(error):
    return make_response(jsonify({'error': 'internal server error'}), 500)


@app.route('/blog/api/v1.0/blogs', methods=['GET'])
def get_blogs():
    blogs = []
    cursor = mongo.db.blogs.find()
    cursor.sort("created-date", 1)
    for blog in cursor:
        dpr("Found blog {}".format(blog))
        blogs.append(blog)
    cursor.close()
    if len(blogs) != 0:
        return jsonify({'blogs': [make_public_blog(blog) for blog in blogs]})
    else:
        abort(404)


@app.route('/blog/api/v1.0/blogs', methods=['POST'])
def create_blog():
    if not request.json:
        epr("Not request json")
        abort(400)
    if 'title' not in request.json or 'id' not in request.json or 'content'not in request.json or 'tags' not in request.json:
        epr("Incomplete data")
        abort(400)
    blog = {
        'id': request.json['id'],
        'title': request.json['title'],
        'content': request.json['content'],
        'description': request.json.get('description', ""),
        'tags': request.json.get('tags', ""),
        'last-update': datetime.datetime.utcnow(),
        'created-date': datetime.datetime.utcnow(),
        'author': request.json.get('author', "")
        }
    cursor = mongo.db.blogs.find({'id': blog['id']}).limit(1)
    if cursor.count() > 0:
        epr("Duplicate blog id")
        cursor.close()
        abort(409)
    cursor.close()
    mongo.db.blogs.insert(blog)
    dpr("Blog inserted")
    return jsonify({'blog': make_public_blog(blog)}), 201


@app.route('/blog/api/v1.0/blog/<string:blog_id>', methods=['GET'])
def get_blog(blog_id):
    cursor = mongo.db.blogs.find()
    blog = [blog for blog in cursor if blog['id'] == blog_id]
    cursor.close()
    if len(blog) == 0:
        epr("Could not find blog")
        abort(404)
    dpr("Found blog {}".format(blog))
    return jsonify({'blog': make_public_blog(blog[0])})


@app.route('/blog/api/v1.0/blog/<string:blog_id>', methods=['PUT'])
def update_blog(blog_id):
    cursor = mongo.db.blogs.find()
    blog = [blog for blog in cursor if blog['id'] == blog_id]
    cursor.close()
    if len(blog) == 0:
        epr("Could not find blog with id {}".format(blog_id))
        abort(404)
    else:
        blog = blog[0]
    if not request.json:
        epr("Invalid json")
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        epr("Did not provide title in request (or title not unicode)")
        abort(400)
    if 'description' in request.json and type(request.json['description']) != unicode:
        epr("Did not provide description in request (or description not unicode)")
        abort(400)
    if 'content' in request.json and type(request.json['content']) != unicode:
        epr("Did not provide content in request (or content not unicode)")
        abort(400)
    if 'tags' in request.json and type(request.json['tags']) != unicode:
        epr("Did not provide tags in request (or tags not unicode)")
        abort(400)
    if 'author' in request.json and type(request.json['author']) != unicode:
        epr("Did not provide author in request (or author not unicode)")
        abort(400)
    for fieldname in ['title', 'description', 'content', 'tags', 'author']:
        blog[fieldname] = request.json.get(fieldname, blog[fieldname])
    result = mongo.db.blogs.update_one(
        {"id": blog_id},
        {
            "$set": {
                "title": blog["title"],
                "description": blog["description"],
                "content": blog["content"],
                "tags": blog["tags"],
                "author": blog["author"],
                "last-update": datetime.datetime.utcnow(),
            }
        }
        )
    dpr(result)
    dpr("Updated blog id {}".format(blog_id))
    return jsonify({'blog': make_public_blog(blog)})


@app.route('/blog/api/v1.0/blog/<string:blog_id>', methods=['DELETE'])
def delete_blog(blog_id):
    blog = mongo.db.blogs.find_one_or_404({'id': blog_id})
    if len(blog) == 0:
        epr("Blog with id {} not found".format(blog_id))
        abort(404)
    mongo.db.blogs.delete_one({"id": blog_id})
    dpr("Blog id {} deleted".format(blog_id))
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6541)
#   app.run(debug=True,host='0.0.0.0',port=6541)
