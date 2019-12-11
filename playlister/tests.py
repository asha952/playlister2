from unittest import TestCase, main as unittest_main, mock
from app import app, video_url_creator


def sample_id_list(args):
    pass


class PlaylistsTests(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test the playlists homepage."""
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')

    class PlaylistsTests(TestCase):
        ...

    def test_new(self):
        """Test the new playlist creation page."""
        result = self.client.get('/playlists/new')
        self.assertEqual(result.status, '200 OK')

    def test_video_url_creator(self):
        """Test the video_url_creator function"""
        expected_list = ['https://youtube.com/embed/hY7m5jjJ9mM', 'https://youtube.com/embed/CQ85sUNBK7w']
        output_list = video_url_creator(sample_id_list)
        self.assertEqual(expected_list, output_list)

    @mock.patch('pymongo.collection.Collection.update_one')
    def test_update_playlist(self, mock_update, sample_playlist_id=None, sample_form_data=None, sample_playlist=None):
        result = self.client.post(f'/playlists/{sample_playlist_id}', data=sample_form_data)

        self.assertEqual(result.status, '302 FOUND')
        mock_update.assert_called_with({'_id': sample_playlist_id}, {'$set': sample_playlist})
        
        
if __name__ == '__main__':
    unittest_main()