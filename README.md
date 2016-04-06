
port = '5434'
@app.route('/blog/api/v1.0/blogs', methods=['GET'])
@app.route('/blog/api/v1.0/blogs', methods=['POST'])
@app.route('/blog/api/v1.0/blog/<string:blog_id>', methods=['GET'])
@app.route('/blog/api/v1.0/blog/<string:blog_id>', methods=['PUT'])
@app.route('/blog/api/v1.0/blog/<string:blog_id>', methods=['DELETE'])


