from flask import Flask, request
from pymongo import MongoClient, collection
import context
import uuid
import datetime
import jwt

app = Flask(__name__)
main_context = context.MainContext()
user_context = context.UserContext(main_context)


@app.route('/api/login')
def login():
    username = request.args.get("user_name")
    passhash = request.args.get("password_hash")

    user = user_context.find_user(username)

    if user is None:
        return 'User not found'
    if passhash != user.password_hash:
        return 'Incorrect password'

    # delau token
    payload = dict()
    payload["user_name"] = username
    payload["user_id"] = user.id
    payload["role"] = user.role
    payload["email"] = user.email

    encoded_jwt = jwt.encode(payload, 'Pisos6Blyat9Chlen', algorithm='HS256')
    return encoded_jwt


# zagruzka faila
@app.route('/api/upload_file', methods=["POST"])
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
    file_note = dict()
    file_note["name"] = file_name
    file_note["type"] = file_name[file_name.index(".") + 1:]
    file_note["size"] = stream.limit
    file_note["path"] = "files/" + file_name_uuid
    file_id = str(files.insert_one(file_note).inserted_id)
    return file_id


# publikyu post
@app.route('/api/upload_post', methods=["POST"])
def upload_post():
    token = request.args.get("token")
    payload = jwt.decode(token, key="Pisos6Blyat9Chlen", algorithms=["HS256"])
    post_data = request.json
    post_node = dict()
    post_node["title"] = post_data["title"]
    post_node["description"] = post_data["description"]
    post_node["attachments"] = post_data["attachments"]
    post_node["category"] = post_data["category"]
    post_node["tags"] = post_data["tags"]
    post_node["publisher"] = payload["user_id"]
    post_node["date"] = datetime.datetime.now()
    if payload["role"] == "student":
        wait_list.insert_one(post_node)
    else:
        main_list.insert_one(post_node)
    return ""


# uydalenie posta
@app.route("/api/delete_post")
def delete_post():
    token = request.args.get("token")
    post_id = request.args.get("post_id")
    payload = jwt.decode(token, key="Pisos6Blyat9Chlen", algorithms=["HS256"])
    found_posts = main_list.find({"_id": collection.ObjectId(post_id)})
    if found_posts.count() == 0:
        return "Post not found"
    post = found_posts[0]
    if payload["role"] == "admin":
        main_list.delete_one({"_id": collection.ObjectId(post_id)})
        return ""

    if payload["user_id"] == post["publisher"]:
        main_list.delete_one({"_id": collection.ObjectId(post_id)})
        return ""
    return "Access denied"


if __name__ == '__main__':
    app.run(debug=True)
