from bson.objectid import ObjectId
from flask import Flask, redirect, render_template, request, url_for
import os
from pymongo import MongoClient

# Flask simple setup
app = Flask(__name__)
# app.config["ENV"] = "development"

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Playlister')
client = MongoClient(host=f'{host}?retryWrites=false')  # MongoClient()
# client = MongoClient()
playlister_db = client.get_default_database()  # client.Playlister

playlist_collection = playlister_db.playlists
comment_collection = playlister_db.comments


@app.route("/")
def playlists_view():
    """Show all playlists."""
    return render_template("playlists_view.html", playlists=playlist_collection.find())


@app.route("/playlists", methods=['POST'])
def playlists_submit():
    """Handle save playlist form action"""
    playlist_document = {
        'title': request.form.get('title-input'),
        'description': request.form.get('description-input'),
        'videos': request.form.get('videos-input').split(),
    }
    playlist_id = playlist_collection.insert_one(playlist_document).inserted_id
    return redirect(url_for("playlists_show", playlist_id=playlist_id))


@app.route("/playlists/<playlist_id>")
def playlists_show(playlist_id):
    playlist_document = playlist_collection.find_one({
        "_id": ObjectId(playlist_id)
    })
    comment_documents = comment_collection.find({
        "playlist_id": ObjectId(playlist_id),
    })
    return render_template("playlists_show.html", playlist=playlist_document, comments=comment_documents)


@app.route("/playlists/<playlist_id>/edit")
def playlists_edit(playlist_id):
    """Render edit template for playlist with playlist_id"""
    playlist_document = playlist_collection.find_one({"_id": ObjectId(playlist_id)})
    return render_template("playlists_edit.html", playlist=playlist_document, title='Edit Playlist')


@app.route("/playlists/<playlist_id>", methods=["POST"])
def playlist_update(playlist_id):
    """Submit an edited playlist"""
    updated_playlist = {
        "title": request.form.get("title-input"),
        "description": request.form.get("description-input"),
        "videos": request.form.get("videos-input").split(),
    }
    playlist_collection.update_one(
        {"_id": ObjectId(playlist_id)},
        {"$set": updated_playlist}
    )
    return redirect(url_for("playlists_show", playlist_id=playlist_id))


@app.route("/playlists/<playlist_id>/delete", methods=["POST"])
def playlist_delete(playlist_id):
    """Delete playlist by playlist_id"""
    playlist_collection.delete_one({
        "_id": ObjectId(playlist_id),
    })
    return redirect(url_for("playlists_view"))


@app.route("/playlists/new")
def playlists_new():
    """Create a playlist"""
    return render_template("playlists_new.html", playlist={}, title="New Playlist")


@app.route("/playlists/comments", methods=["POST"])
def comments_new():
    """Submit a new comment"""
    comment = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'playlist_id': ObjectId(request.form.get('playlist_id'))
    }
    print(comment)
    comment_id = comment_collection.insert_one(comment).inserted_id
    return redirect(url_for('playlists_show', playlist_id=request.form.get('playlist_id')))


@app.route("/playlists/comments/<comment_id>", methods=["POST"])
def comments_delete(comment_id):
    comment = comment_collection.find_one({
        "_id": ObjectId(comment_id)
    })
    comment_collection.delete_one({
        "_id": ObjectId(comment_id)
    })
    return redirect(url_for("playlists_show", playlist_id=comment_id))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
