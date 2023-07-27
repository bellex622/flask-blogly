import os

os.environ["DATABASE_URL"] = "postgresql:///blogly_test"

from unittest import TestCase

from app import app, db
from models import DEFAULT_IMAGE_URL, User

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
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        db.session.add(test_user)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()


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
            self.assertIn("***User List***", html) # be more specific

    def test_handle_add_user_form(self):
        #check if new user appears on user list
        """Should connect and submit data to the database"""
        print('\n\n***TEST 3***\n\n')
        with self.client as c:
            resp = c.post(
                '/users/new',
                data = {'first_name':'Stuart',
                        'last_name':"Fleisher",
                        'image_url': ""
                },
                follow_redirects=True)
            html = resp.get_data(as_text=True)

            user_count = User.query.count()
            self.assertEqual(resp.status_code,200)
            self.assertTrue(user_count > 1)
            self.assertIn("Stuar", html)

    def test_delete_user(self):
        """Test if a user has been deleted from database"""
        with self.client as c:
            resp = c.post(f'/users/{self.user_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)
            user_count = User.query.count()
            
            self.assertEqual(resp.status_code,200)
            self.assertTrue(user_count == 0)
            self.assertNotIn("test1_first", html)






