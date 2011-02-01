from google.appengine.ext import db
from tipfy.ext.auth.model import gen_salt, gen_pwhash, User as TipfyUser

class User(db.Model):
    created = db.DateTimeProperty(auto_now_add=True)

class AuthUser(TipfyUser):
    user = db.ReferenceProperty(User)

    @classmethod
    def create(cls, username, auth_id, **kwargs):
        """Creates a new user and returns it. If the username already exists,
        returns None.

        :param username:
            Unique username.
        :param auth_id:
            Authentication id, according the the authentication method used.
        :param kwargs:
            Additional entity attributes.
        :returns:
            The newly created user or None if the username already exists.
        """
        kwargs['username'] = username
        kwargs['key_name'] = username
        kwargs['auth_id'] = auth_id
        # Generate an initial session id.
        kwargs['session_id'] = gen_salt(length=32)

        if 'user' not in kwargs:
            u = User()
            u.put()
            kwargs['user'] = u

        if 'password_hash' in kwargs:
            # Password is already hashed.
            kwargs['password'] = kwargs.pop('password_hash')
        elif 'password' in kwargs:
            # Password is not hashed: generate a hash.
            kwargs['password'] = gen_pwhash(kwargs['password'])

        def txn():
            if cls.get_by_username(username) is not None:
                # Username already exists.
                return None

            user = cls(**kwargs)
            user.put()
            return user

        return db.run_in_transaction(txn)
