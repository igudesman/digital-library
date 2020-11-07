from flask import Flask, request, jsonify, send_file
import context
import uuid
import datetime
import jwt

app = Flask(__name__)
main_context = context.MainContext()
user_context = context.UserContext(main_context)
list_context = context.ListContext(main_context)
files = context.FileContext(main_context)


@app.route('/api/user/login')
def login():
    username = request.args.get("user_name")
    passhash = request.args.get("password_hash")

    user = user_context.find_user(username)

    if user is None:
        return 'User not found', 404
    if passhash != user.password_hash:
        return 'Incorrect password', 401

    # delau token
    payload = dict()
    payload["user_name"] = username
    payload["user_id"] = user.id
    payload["role"] = user.role
    payload["email"] = user.email

    encoded_jwt = jwt.encode(payload, 'Pisos6Blyat9Chlen', algorithm='HS256')
    return encoded_jwt


@app.route('/api/user/change_password')
def change_password():
    token = request.args.get("token")
    old_hash = request.args.get("old_hash")
    new_hash = request.args.get("new_hash")
    if new_hash is None or new_hash.strip() == "":
        return "Invalid new password", 403
    if old_hash is None or old_hash.strip() == "":
        return "Invalid old password", 403

    payload = jwt.decode(token, key="Pisos6Blyat9Chlen", algorithms=["HS256"])
    user = user_context.find_user(payload["user_name"])
    if user is None:
        return "User not found", 404
    if old_hash != user.password_hash:
        return "Old and new password are different", 403

    user_context.change_password(payload["user_name"], new_hash)
    return ""


@app.route("/api/user/delete")
def delete_user():
    token = request.args.get("token")
    user_name = request.args.get("user_name")
    payload = jwt.decode(token, key="Pisos6Blyat9Chlen", algorithms=["HS256"])
    if payload["role"] != "admin":
        return "Access denied", 403

    user = user_context.find_user(user_name)
    if user is None:
        return "User not found", 404
    if user.role == "admin":
        return "Access denied", 403
    user_context.delete_user(user_name)
    return ""


# zagruzka faila
@app.route('/api/files/upload', methods=["POST"])
def upload_file():
    file_name = request.args.get("file_name")
    token = request.args.get("token")
    payload = jwt.decode(token, key="Pisos6Blyat9Chlen", algorithms=["HS256"])
    stream = request.stream
    file_name_uuid = str(uuid.uuid4())
    file_stream = open("files/" + file_name_uuid, "wb")
    file_stream.write(stream.read())
    file_stream.flush()
    file_stream.close()
    file_type = file_name[file_name.index(".") + 1:]
    file = context.FileDBModel()
    file.name = file_name
    file.type = file_type
    file.size = stream.limit
    file.path = 'files/' + file_name_uuid
    return files.add_file(file)


@app.route('/api/files/get_info')
def get_file_info():
    token = request.args.get("token")
    file_id = request.args.get("file_id")
    payload = jwt.decode(token, key="Pisos6Blyat9Chlen", algorithms=["HS256"])
    file = files.find_file(file_id)
    if file is None:
        return "File not found", 404
    return file.to_response_dict()


@app.route('/api/files/download')
def download_file():
    token = request.args.get("token")
    file_id = request.args.get("file_id")
    payload = jwt.decode(token, key="Pisos6Blyat9Chlen", algorithms=["HS256"])
    file = files.find_file(file_id)
    if file is None:
        return "File not found", 404
    return send_file(file.path, as_attachment=True, attachment_filename=file.name)


# publikyu post
@app.route('/api/post/upload', methods=["POST"])
def upload_post():
    token = request.args.get("token")
    payload = jwt.decode(token, key="Pisos6Blyat9Chlen", algorithms=["HS256"])
    post_data = request.json
    post = context.PostDBModel()
    post.title = post_data["title"]
    post.description = post_data["description"]
    post.attachments = post_data["attachments"]
    post.category = post_data["category"]
    post.tags = post_data["tags"]
    post.publisher = payload["user_id"]
    post.date = datetime.datetime.now()
    if payload["role"] == "student":
        list_context.add_post(post, "wait")
    else:
        list_context.add_post(post, "main")
    return ""


# uydalenie posta
@app.route("/api/post/delete")
def delete_post():
    token = request.args.get("token")
    post_id = request.args.get("post_id")
    collection = request.args.get("collection")
    if collection is None or collection.strip() == "":
        collection = "main"
    payload = jwt.decode(token, key="Pisos6Blyat9Chlen", algorithms=["HS256"])

    post = list_context.find_post(post_id, collection)
    if post is None:
        return "Post not found", 404

    if payload["role"] == "admin":
        list_context.delete_post(post_id, collection)
        return ""

    if payload["user_id"] == post["publisher"]:
        list_context.delete_post(post_id, collection)
        return ""
    return "Access denied", 403


@app.route("/api/post/accept")
def accept_post():
    token = request.args.get("token")
    post_id = request.args.get("post_id")
    payload = jwt.decode(token, key="Pisos6Blyat9Chlen", algorithms=["HS256"])
    if payload["role"] == "student":
        return "Access denied", 403
    else:
        post = list_context.find_post(post_id, "wait")
        if post is None:
            return "Post not found", 404
        list_context.accept_post(post_id)
        return ""


#poisk
@app.route("/api/post/search")
def search():
    token = request.args.get("token")
    search_str = request.args.get("search_str")
    if search_str is None:
        search_str = ""
    else:
        search_str = search_str.strip().lower()

    category = request.args.get("category")
    if category is not None:
        category = category.strip().lower()
    tags = request.args.get("tags")
    if tags is not None and tags.strip().lower() != "":
        tags = tags.strip().lower().split(",")
    offset = request.args.get("offset")
    limit = request.args.get("limit")
    if offset is None:
        offset = 0
    else:
        try:
            offset = int(offset)
        except ValueError:
            offset = 0
    if limit is None:
        limit = 20
    else:
        try:
            limit = int(limit)
        except ValueError:
            limit = 20
    collection = request.args.get("collection")
    if collection is None or collection.strip() == "":
        collection = "main"

    payload = jwt.decode(token, key="Pisos6Blyat9Chlen", algorithms=["HS256"])
    if collection == "wait" and payload["role"] != "student":
        result = list_context.search("wait", search_str, category, tags, offset, limit)
    elif collection == "main":
        result = list_context.search("main", search_str, category, tags, offset, limit)
    else:
        return "Access denied", 403
    response = list()
    for node in result:
        response.append(node.to_dict())
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
