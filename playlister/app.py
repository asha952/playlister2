from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

client = MongoClient()
db = client.Playlister
playlists = db.playlists
app = Flask(__name__)


def video_url_creator(id_lst):
    videos = []
    for vid_id in id_lst:
        # We know that embedded YouTube videos always have this format
        video = 'https://youtube.com/embed/' + vid_id
        videos.append(video)
    return videos


'''
@app.route('/')
def index():
    """Return homepage."""
    return render_template('home.html', msg='Flask is Cool!!')
'''

'''
# OUR MOCK ARRAY OF PROJECTS
playlists = [
    {'title': 'Cat Videos', 'description': 'Cats acting weird'},
    {'title': '80\'s Music', 'description': 'Don\'t stop believing!'}
]
'''


@app.route('/')
def playlists_index():
    """Show all playlists."""
    # Update this line
    return render_template('playlists_index.html', playlists=playlists.find())


@app.route('/playlists/new')
def playlists_new():
    """Create a new playlist."""
    return render_template('playlists_new.html')


@app.route('/playlists', methods=['POST'])
def playlists_submit():
    """Submit a new playlist."""
    playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description')
    }
    playlists.insert_one(playlist)
    return redirect(url_for('playlists_index'))


# Note the methods parameter that explicitly tells the route that this is a POST
@app.route('/playlists', methods=['POST'])
def playlists_submit():
    """Submit a new playlist."""
    # Grab the video IDs and make a list out of them
    video_ids = request.form.get('video_ids').split()
    # call our helper function to create the list of links
    videos = video_url_creator(video_ids)
    playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': videos,
        'video_ids': video_ids
    }
    playlists.insert_one(playlist)
    return redirect(url_for('playlists_index'))


# Add this with the rest of your import statements
from bson.objectid import ObjectId


# ...


@app.route('/playlists/<playlist_id>')
def playlists_show(playlist_id):
    """Show a single playlist."""
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    return render_template('playlists_show.html', playlist=playlist)


@app.route('/playlists/<playlist_id>', methods=['POST'])
def playlists_update(playlist_id):
    """Submit an edited playlist."""
    video_ids = request.form.get('video_ids').split()
    videos = video_url_creator(video_ids)
    # create our updated playlist
    updated_playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': videos,
        'video_ids': video_ids
    }
    # set the former playlist to the new one we just updated/edited
    playlists.update_one(
        {'_id': ObjectId(playlist_id)},
        {'$set': updated_playlist})
    # take us back to the playlist's show page
    return redirect(url_for('playlists_show', playlist_id=playlist_id))


if __name__ == '__main__':
    app.run(debug=True)
