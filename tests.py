from models import DEFAULT_IMAGE_URL, User, Post
from app import app, db
from unittest import TestCase
import os

os.environ["DATABASE_URL"] = "postgresql:///blogly_test"


# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()


        self.client = app.test_client()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        db.session.add(test_user)
        db.session.commit()


        test_post = Post(
            title="test1_title",
            content="test1_content",
            user_id=test_user.id

        )
        db.session.add(test_post)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id
        self.post_id = test_post.id


    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()


    ############################ USER TESTS ###################################

    def test_show_homepage(self):
        """Should redirect to /users"""
        print('\n\n***TEST 1***\n\n')
        with self.client as c:
            resp = c.get('/')
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, '/users')

    def test_show_users(self):
        """Should load the user list template"""
        print('\n\n***TEST 2***\n\n')
        with self.client as c:
            resp = c.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("***User List***", html)  # be more specific


    def test_handle_add_user_form(self):
        # check if new user appears on user list
        """Should connect and submit data to the database"""
        print('\n\n***TEST 3***\n\n')
        with self.client as c:
            resp = c.post(
                '/users/new',
                data={'first_name': 'Stuart',
                      'last_name': "Fleisher",
                      'image_url': ""
                      },
                follow_redirects=True)
            html = resp.get_data(as_text=True)

            user_count = User.query.count()
            self.assertEqual(resp.status_code, 200)
            self.assertTrue(user_count > 1)
            self.assertIn("Stuar", html)

    def test_delete_user(self):
        """Test if a user has been deleted from database"""

        #consider testing that posts are removed

        print('\n\n***USER TEST 4***\n\n')

        with self.client as c:
            resp = c.post(f'/users/{self.user_id}/delete',
                          follow_redirects=True)
            html = resp.get_data(as_text=True)
            user_count = User.query.count()

            self.assertEqual(resp.status_code, 200)
            self.assertTrue(user_count == 0)
            self.assertNotIn("test1_first", html)


    ############################ POST TESTS ###################################


    def test_show_post(self):
        """Should load the post page"""

        print('\n\n***POST TEST 1***\n\n')
        with self.client as c:
            resp = c.get(f'/posts/{self.post_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("test1_content", html)


    def test_add_post(self):
        """Should add new a post and redirect"""

        print('\n\n***POST TEST 2***\n\n')
        initial_count = Post.query.count()
        with self.client as c:
            resp = c.post(
                f'/users/{self.user_id}/posts/new',
                data={
                    'title': 'test2_title',
                    'content': 'test2_content'
                },
                follow_redirects=True
            )
            html = resp.get_data(as_text=True)
            post_count = Post.query.count()

            self.assertEqual(resp.status_code, 200)
            self.assertTrue(post_count = initial_count +1) #compare count before and after route
            self.assertIn("test2_title", html)



    def test_edit_post(self):
        """Should update the post from form and redirect"""

        print('\n\n***POST TEST 3***\n\n')
        with self.client as c:
            resp = c.post(
                f'/posts/{self.post_id}/edit',
                data={
                    'title': 'new_title',
                    'content': 'new_content'
                },
                follow_redirects=True
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("new_title", html)
            self.assertIn("new_content", html)


    def test_delete_post(self):
        """Should delete the post and redirect"""

        print('\n\n***POST TEST 4***\n\n')

        with self.client as c:
            resp = c.post(
                f'/posts/{self.post_id}/delete',
                follow_redirects=True
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200) #consider testing count
            self.assertNotIn("test1_title", html)
