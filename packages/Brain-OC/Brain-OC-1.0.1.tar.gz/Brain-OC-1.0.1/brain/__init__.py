# coding=utf8
""" Brain Service

Handles all Authorization / Login requests
"""

__author__ = "Chris Nasr"
__copyright__ = "Ouroboros Coding Inc."
__version__ = "1.0.0"
__email__ = "chris@ouroboroscoding.com"
__created__ = "2022-08-26"

# Python imports
from time import time
import uuid

# Pip imports
import body
from redis import StrictRedis
from RestOC import	Conf, DictHelper, Record_Base, Services, Session, StrHelper

# Records imports
from .records import cache as record_cache, Key, Permissions, User

# Local
from . import access as _access, users as _users, errors

# Export child modules
access = _access
users = _users

class Brain(Services.Service):
	"""Brain Service class

	Service for authorization, sign in, sign up, permissions etc.
	"""

	def _create_key(self, user, type_):
		"""Create Key

		Creates a key used for verification of the user

		Arguments:
			user (str): The ID of the user
			type_ (str): The type of key to make

		Returns:
			str
		"""

		# Create an instance
		oKey = Key({
			'_id': StrHelper.random(32, '_0x'),
			'user': user,
			'type': type_
		})

		# Loop until we resolve the issue
		while True:
			try:

				# Create the key record
				oKey.create()

				# Return the key
				return oKey['_id']

			# If we got a duplicate key error
			except Record_Base.DuplicateException as e:

				# If the primary key is the duplicate
				if 'PRIMARY' in e.args[1]:

					# Generate a new key and try again
					oKey['_id'] = StrHelper.random(32, '_0x')
					continue

				# Else, the type has already been used for the user
				else:

					# Find the existing key
					dKey = Key.filter({'user': user, 'type': type_}, raw=['_id'], limit=1)
					return dKey['_id']

	@classmethod
	def _verify(cls, user, name, right):
		"""Verify

		Checks the user currently in the session has access to the requested
		permission

		Arguments:
			user (str): The ID of the user
			name (str): The name of the permission to check
			right (uint): The specific right on the permission to verify

		Returns:
			bool
		"""

		# Find the permissions
		dPermissions = Permissions.get(user, raw=True)

		# If the user has no permissions at all
		if not dPermissions:
			return False

		# If one permission was requested
		if isinstance(name, str):

			# If we don't have it
			if name not in dPermissions['rights']:
				return False

			# Set the name to use
			sName = name

		# Else, if it's a list
		elif isinstance(name, list):

			# Go through each one, if one matches, store it
			for s in name:
				if s in dPermissions['rights']:
					sName = s
					break

			# Else, return failure
			else:
				return False

		# Else, invalid name data
		else:
			raise Services.ResponseException(error=(body.errors.DATA_FIELDS, [['name', 'invalid, must be string or string[]']]))

		# If one right was requested
		if isinstance(right, int):

			# If the permission doesn't contain the requested right
			if not dPermissions['rights'][sName] & right:
				return False

		# Else, if it's a list of rights
		elif isinstance(right, list):

			# Go through each one, if it passes, break
			for i in right:
				if dPermissions['rights'][sName] & i:
					break

			# Else, no rights matched
			else:
				return False

		# Else, invalid right data
		else:
			raise Services.ResponseException(error=(body.errors.DATA_FIELDS, [['right', 'invalid, must be int or int[]']]))

		# Seems ok
		return True

	def initialise(self):
		"""Initialise

		Initialises the instance and returns itself for chaining

		Returns:
			Authorization
		"""

		# Get config
		self._conf = Conf.get('brain', {
			'user_default_locale': 'en-US',
			'redis_host': 'brain'
		})

		# Create a connection to Redis
		self._redis = StrictRedis(**Conf.get(('redis', self._conf['redis_host']), {
			'host': 'localhost',
			'port': 6379,
			'db': 0
		}))

		# Pass the Redis connection to the records
		record_cache(self._redis)

		# Return self for chaining
		return self

	def permissions_read(self, req):
		"""Permissions read

		Returns all permissions associated with a user

		Arguments:
			req (dict): The request details, which can include 'data',
						'environment', and 'session'

		Returns:
			Services.Response
		"""

		# If the user is missing
		if 'user' not in req['data']:
			return Services.Error(body.errors.DATA_FIELDS, [['user', 'missing']])

		# If this is an internal request
		if '_internal_' in req['data']:

			# Verify the key, remove it if it's ok
			if not Services.internal_key(req['data']['_internal_']):
				raise Services.ResponseException(error=body.errors.SERVICE_INTERNAL_KEY)
			del req['data']['_internal_']

		# Else, check permissions
		else:
			if not self._verify(req['session']['user']['_id'], 'brain_permission', access.READ):
				return Services.Error(body.errors.RIGHTS)

		# Fetch the Permissions
		dPermissions = Permissions.get(req['data']['user'], raw=True)

		# Return all permissions
		return Services.Response(dPermissions)

	def permissions_update(self, req):
		"""Permissions update

		Updates the permissions for a single user

		Arguments:
			req (dict): The request details, which can include 'data',
						'environment', and 'session'

		Returns:
			Services.Response
		"""

		# Check minimum fields
		try: DictHelper.eval(req['data'], ['user', 'rights'])
		except ValueError as e: return Services.Error(body.errors.DATA_FIELDS, [[f, 'missing'] for f in e.args])

		# If this is an internal request
		if '_internal_' in req['data']:

			# Verify the key, remove it if it's ok
			if not Services.internal_key(req['data']['_internal_']):
				raise Services.ResponseException(error=body.errors.SERVICE_INTERNAL_KEY)
			del req['data']['_internal_']

			# Store the user ID as the system user
			sSessionUser = users.SYSTEM_USER_ID

		# Else, check permissions
		else:

			# Verify the rights
			if not self._verify(req['session']['user']['_id'], 'brain_permission', access.UPDATE):
				return Services.Error(body.errors.RIGHTS)

			# Store the user ID
			sSessionUser = req['session']['user']['_id']

		# If the user doesn't exist
		if not User.exists(req['data']['user']):
			return Services.Error(body.errors.DB_NO_RECORD, (req['data']['user'], 'user'))

		# Find the permissions
		oPermissions = Permissions.get(req['data']['user'])
		if not oPermissions:
			return Services.Error(body.errors.DB_NO_RECORD, (req['data']['user'], 'permissions'))

		# Try to set the new permissions
		try:
			oPermissions['rights'] = req['data']['rights']
		except ValueError as e:
			return Services.Error(body.errors.DATA_FIELDS, (e.args[0]))

		# Save the permissions
		bSave = oPermissions.save(changes={'user': sSessionUser})

		# Clear the cache
		if bSave:
			Permissions.clear(req['data']['user'])

		# Return the result
		return Services.Response(bSave)

	def permissions_add_create(self, req):
		"""Permissions Add create

		Addes a specific permission type to existing permissions

		Arguments:
			req (dict): The request details, which can include 'data',
						'environment', and 'session'

		Returns:
			Services.Response
		"""

		# Check minimum fields
		try: DictHelper.eval(req['data'], ['user', 'rights'])
		except ValueError as e: return Services.Error(body.errors.DATA_FIELDS, [[f, 'missing'] for f in e.args])

		# If this is an internal request
		if '_internal_' in req['data']:

			# Verify the key, remove it if it's ok
			access.internal(req['data'])

			# Store the user ID as the system user
			sSessionUser = users.SYSTEM_USER_ID

		# Else, check permissions
		else:

			# Verify the rights
			if not self._verify(req['session']['user']['_id'], 'brain_permission', access.UPDATE):
				return Services.Error(body.errors.RIGHTS)

			# Store the user ID
			sSessionUser = req['session']['user']['_id']

		# If the user doesn't exist
		if not User.exists(req['data']['user']):
			return Services.Error(body.errors.DB_NO_RECORD, [req['data']['user'], 'user'])

		# Find the permissions
		oPermissions = Permissions.get(req['data']['user'])
		if not oPermissions:
			return Services.Error(body.errors.DB_NO_RECORD, [req['data']['user'], 'permissions'])

		# Combine the rights
		dRights = DictHelper.combine(oPermissions['rights'], req['data']['rights'])

		# Try to update the permissions
		try:
			oPermissions['rights'] = dRights
		except ValueError as e:
			return Services.Error(body.errors.DATA_FIELDS, [e.args[0]])

		# Save and return the results
		return Services.Response(
			oPermissions.save(changes={'user': sSessionUser})
		)

	def search_read(self, req):
		"""Search

		Looks up users by search / query

		Arguments:
			req (dict): The request details, which can include 'data',
						'environment', and 'session'

		Returns:
			Services.Response
		"""

		# Check permissions
		self._verify(req['session']['user']['_id'], 'brain_user', access.READ)

		# Check for filter
		if 'filter' not in req['data']:
			return Services.Error(body.errors.DATA_FIELDS, [['filter', 'missing']])

		# If the filter isn't a dict
		if not isinstance(req['data']['filter'], dict):
			return Services.Error(body.errors.DATA_FIELDS, [['filter', 'must be an object']])

		# If fields is not a list
		if 'fields' in req['data'] and not isinstance(req['data']['fields'], list):
			return Services.Error(body.errors.DATA_FIELDS, [['fields', 'must be a list']])

		# Search based on the req['data'] passed
		lRecords = [d['_id'] for d in User.search(req['data']['filter'], raw=['_id'])]

		# If we got something, fetch the records from the cache
		if lRecords:
			lRecords = User.cache(lRecords, raw=('fields' in req['data'] and req['data']['fields'] or True))

		# Remove the passwd
		for d in lRecords:
			del d['passwd']

		# Return the results
		return Services.Response(lRecords)

	def session_read(self, req):
		"""Session

		Returns the ID of the user logged into the current session

		Arguments:
			req (dict): The request details, which can include 'data',
						'environment', and 'session'

		Returns:
			Services.Response
		"""
		return Services.Response({
			'user' : {
				'_id': req['session']['user']['_id']
			}
		})

	def signin_create(self, req):
		"""Signin

		Signs a user into the system

		Arguments:
			req (dict): The request details, which can include 'data',
						'environment', and 'session'

		Returns:
			Result
		"""

		# Check minimum fields
		try: DictHelper.eval(req['data'], ['email', 'passwd'])
		except ValueError as e: return Services.Error(body.errors.DATA_FIELDS, [[f, 'missing'] for f in e.args])

		# Look for the user by alias
		oUser = User.filter({'email': req['data']['email']}, limit=1)
		if not oUser:
			return Services.Error(errors.SIGNIN_FAILED)

		# If it's the system user, reject it
		if oUser['_id'] == users.SYSTEM_USER_ID:
			return Services.Error(errors.SIGNIN_FAILED)

		# Validate the password
		if not oUser.password_validate(req['data']['passwd']):
			return Services.Error(errors.SIGNIN_FAILED)

		# Create a new session
		oSesh = Session.create('sesh:%s' % uuid.uuid4().hex)

		# Store the user ID and information in it
		oSesh['user'] = {'_id': oUser['_id']}

		# Save the session
		oSesh.save()

		# Return the session ID and primary user data
		return Services.Response({
			'session': oSesh.id(),
			'user': oSesh['user']
		})

	def signout_create(self, req):
		"""Signout

		Called to sign out a user and destroy their session

		Arguments:
			req (dict): The request details, which can include 'data',
						'environment', and 'session'

		Returns:
			Services.Response
		"""

		# Close the session so it can no longer be found/used
		if 'session' in req and req['session']:
			req['session'].close()

		# Return OK
		return Services.Response(True)

	def user_create(self, req):
		"""User Create

		Creates a new user

		Arguments:
			req (dict): The request details, which can include 'data',
						'environment', and 'session'

		Returns:
			Services.Response
		"""

		# Check permissions
		self._verify(req['session']['user']['_id'], 'brain_user', access.CREATE)

		# Check minimum fields
		try: DictHelper.eval(req['data'], ['email', 'url'])
		except ValueError as e: return Services.Error(body.errors.DATA_FIELDS, [[f, 'missing'] for f in e.args])

		# Make sure the URL has the {key} field
		if '{key}' not in req['data']['url']:
			return Services.Error(body.errors.DATA_FIELDS, [['url', 'missing {key}']])

		# Pop off the URL
		sURL = req['data'].pop('url')

		# Strip leading and trailing spaces on the email
		req['data']['email'] = req['data']['email'].strip()

		# Make sure the email is valid structurally
		if not body.regex.EMAIL_ADDRESS.match(req['data']['email']):
			return Services.Error(body.errors.DATA_FIELDS, [['email', 'invalid']])

		# Check if a user with that email already exists
		sExistingUserID = User.exists(req['data']['email'], 'email')
		if sExistingUserID:
			return Services.Error(body.errors.DB_DUPLICATE, sExistingUserID)

		# Add the blank password
		req['data']['passwd'] = '000000000000000000000000000000000000000000000000000000000000000000000000'

		# Set not verified
		req['data']['verified'] = False

		# Add defaults
		if 'locale' not in req['data']:
			req['data']['locale'] = self._conf['user_default_locale']

		# Validate by creating a Record instance
		try:
			oUser = User(req['data'])
		except ValueError as e:
			return Services.Error(body.errors.DATA_FIELDS, e.args[0])

		# Create the record
		sID = oUser.create(changes={'user': req['session'] and req['session']['user']['_id'] or users.SYSTEM_USER_ID})

		# Create empty permissions
		oPermissions = Permissions({
			'_user': sID,
			'rights': {}
		})
		oPermissions.create(changes={'user': req['session'] and req['session']['user']['_id'] or users.SYSTEM_USER_ID})

		# If the record was created
		if sID:

			# Create key for setup validation
			sSetupKey = self._create_key(oUser['_id'], 'setup')

			# Email the user the setup link
			oResponse = Services.create('mouth', 'email', {'data': {
				'_internal_': Services.internal_key(),
				'template': {
					'name': 'setup_user',
					'locale': oUser['locale'],
					'variables': {
						'key': sSetupKey,
						'url': sURL.replace('{key}', sSetupKey)
					},
				},
				'to': req['data']['email']
			}})
			if oResponse.error_exists():
				Key.delete_get(sSetupKey)
				return oResponse

		# Return the result
		return Services.Response(sID)

	def user_read(self, req):
		"""User Read

		Fetches an existing user and returns their data

		Arguments:
			req (dict): The request details, which can include 'data',
						'environment', and 'session'

		Returns:
			Services.Response
		"""

		# If there's an ID, check permissions
		if 'data' in req and '_id' in req['data']:
			self._verify(req['session']['user']['_id'], 'brain_user', access.READ)

		# Else, assume the signed in user's Record
		else:
			req['data'] = {'_id': req['session']['user']['_id']}

		# Fetch it from the cache
		dUser = User.cache(req['data']['_id'], raw=True)

		# If it doesn't exist
		if not dUser:
			return Services.Error(body.errors.DB_NO_RECORD, (req['data']['_id'], 'user'))

		# Remove the passwd
		del dUser['passwd']

		# Fetch the permissions and add them to the user
		dPermissions = Permissions.get(req['data']['_id'], raw=['rights'])
		dUser['permissions'] = dPermissions['rights']

		# Return the user data
		return Services.Response(dUser)

	def user_update(self, req):
		"""User Update

		Updates an existing user

		Arguments:
			req (dict): The request details, which can include 'data',
						'environment', and 'session'

		Returns:
			Services.Response
		"""

		# If there's an ID, check permissions
		if '_id' in req['data'] and req['data']['_id'] != req['session']['user']['_id']:

			# If the ID isn't set
			if not req['data']['_id']:
				return Services.Error(body.errors.DATA_FIELDS, [['_id', 'missing']])

			# Make sure the user has the proper permission to do this
			self._verify(req['session']['user']['_id'], 'brain_user', access.UPDATE)

		# Else, assume the signed in user's Record
		else:
			req['data']['_id'] = req['session']['user']['_id']

		# Fetch it from the cache
		oUser = User.cache(req['data']['_id'])

		# If the user isn't found
		if not oUser:
			return Services.Error(body.errors.DB_NO_RECORD, (req['data']['_id'], 'user'))

		# Remove fields that can't be changed
		for k in ['_id', '_created', '_updated', 'email', 'passwd']:
			try: del req['data'][k]
			except KeyError: pass

		# If the email was passed
		if 'email' in req['data']:

			# Strip leading and trailing spaces
			req['data']['email'] = req['data']['email'].strip()

			# Make sure it's valid structurally
			if not body.regex.EMAIL_ADDRESS.match(req['data']['email']):
				return Services.Error(body.errors.DATA_FIELDS, [['email', 'invalid']])

		# Step through each field passed and update/validate it
		lErrors = []
		for f in req['data']:
			try: oUser[f] = req['data'][f]
			except ValueError as e: lErrors.append(e.args[0])

		# If there was any errors
		if lErrors:
			return Services.Error(body.errors.DATA_FIELDS, lErrors)

		# Update the record
		bRes = oUser.save(changes={'user': req['session']['user']['_id']})

		# If it was updated, clear the cache
		if bRes:
			User.clear(oUser['_id'])

		# Return the result
		return Services.Response(bRes)

	def user_email_update(self, req):
		"""User Email update

		Changes the email for the current signed in user

		Arguments:
			req (dict): The request details, which can include 'data',
						'environment', and 'session'

		Returns:
			Services.Response
		"""

		# Check minimum fields
		try: DictHelper.eval(req['data'], ['email', 'email_passwd', 'url'])
		except ValueError as e: return Services.Error(body.errors.DATA_FIELDS, [[f, 'missing'] for f in e.args])

		# Make sure the URL has the {key} field
		if '{key}' not in req['data']['url']:
			return Services.Error(body.errors.DATA_FIELDS, [['url', 'missing {key}']])

		# Find the user
		oUser = User.get(req['session']['user']['_id'])
		if not oUser:
			return Services.Error(body.errors.DB_NO_RECORD, (req['session']['user']['_id'], 'user'))

		# Validate the password
		if not oUser.password_validate(req['data']['email_passwd']):
			return Services.Error(errors.SIGNIN_FAILED)

		# If the email hasn't changed
		if oUser['email'] == req['data']['email']:
			return Services.Response(False)

		# Strip leading and trailing spaces on email
		req['data']['email'] = req['data']['email'].strip()

		# Make sure the email is valid structurally
		if not body.regex.EMAIL_ADDRESS.match(req['data']['email']):
			return Services.Error(body.errors.DATA_FIELDS, [['email', 'invalid']])

		# Look for someone else with that email
		dUser = User.filter({'email': req['data']['email']}, raw=['_id'])
		if dUser:
			return Services.Error(body.errors.DB_DUPLICATE, (req['data']['email'], 'user'))

		# Update the email and verified fields
		try:
			oUser['email'] = req['data']['email']
			oUser['verified'] = False
		except ValueError as e:
			return Services.Error(body.errors.DATA_FIELDS, e.args[0])

		# Generate a new key
		sKey = self._create_key(oUser['_id'], 'verify')

		# Update the user
		bRes = oUser.save(changes={'user':req['session']['user']['_id']})

		# If the user was updated
		if bRes:

			# Clear the cache
			User.clear(oUser['_id'])

			# Create key
			sKey = self._create_key(oUser['_id'], 'verify')

			# Verification template variables
			dTpl = {
				'key': sKey,
				'url': req['data']['url'].replace('{key}', sKey)
			}

			# Email the user the key
			oResponse = Services.create('mouth', 'email', {'data': {
				'_internal_': Services.internal_key(),
				'template': {
					'name': 'verify_email',
					'locale': oUser['locale'],
					'variables': dTpl
				},
				'to': req['data']['email'],
			}})
			if oResponse.error_exists():
				Key.delete_get(sKey)
				return oResponse

		# Return the result
		return Services.Response(bRes)

	def user_email_verify_update(self, req):
		"""User Email Verify update

		Marks the user/email as verified

		Arguments:
			req (dict): The request details, which can include 'data',
						'environment', and 'session'

		Returns:
			Services.Response
		"""

		# If the key is not passed
		if 'key' not in req['data']:
			return Services.Error(body.errors.DATA_FIELDS, [['key', 'missing']])

		# Look for the key
		oKey = Key.get(req['data']['key'])
		if not oKey:
			return Services.Error(body.errors.DB_NO_RECORD, (req['data']['key'], 'key'))

		# Find the user associated with they key
		oUser = User.get(oKey['user'])
		if not oUser:
			return Services.Error(body.errors.DB_NO_RECORD, (oKey['user'], 'user'))

		# Mark the user as verified and save
		oUser['verified'] = True
		bRes = oUser.save(changes={'user': oKey['user']})

		# If the save was successful
		if bRes:

			# Clear the cache
			User.clear(oKey['user'])

			# Delete the key
			oKey.delete()

		# Return the result
		return Services.Response(bRes)

	def user_names_read(self, req):
		"""User Names read

		Returns a list or dict of IDs to names of users

		Arguments:
			req (dict): The request details, which can include 'data',
						'environment', and 'session'

		Returns:
			Services.Response
		"""

		# Make sure we got an ID
		if '_id' not in req['data']:
			return Services.Error(body.errors.DATA_FIELDS, [['_id', 'missing']])

		# If the type is missing
		if 'type' not in req['data'] or not req['data']['type']:
			req['data']['type'] = 'object'

		# Else, if the type is invalid
		elif req['data']['type'] not in ['array', 'object']:
			return Services.Error(body.errors.DATA_FIELDS, [['type', 'invalid']])

		# If we only got one ID
		if isinstance(req['data']['_id'], str):
			req['data']['_id'] = [req['data']['_id']]

		# If the list is empty
		if not req['data']['_id']:
			return Services.Error(body.errors.DATA_FIELDS, [['_id', 'empty']])

		# If the client requested an array, return a list
		if req['data']['type'] == 'array':
			return Services.Response(
				User.get(req['data']['_id'], raw=['_id', 'first_name', 'last_name'], orderby=['first_name', 'last_name'])
			)

		# Else, they requested an object, so return a dict
		else:
			return Services.Response({
				d['_id']: {'first_name':d['first_name'], 'last_name':d['last_name']}
				for d in User.get(req['data']['_id'], raw=['_id', 'first_name', 'last_name'])
			})

	def user_passwd_update(self, req):
		"""User Password update

		Changes the password for the current signed in user

		Arguments:
			req (dict): The request details, which can include 'data',
						'environment', and 'session'

		Returns:
			Services.Response
		"""

		# Make sure we got a new password
		if 'new_passwd' not in req['data']:
			return Services.Error(body.errors.DATA_FIELDS, [['new_passwd', 'missing']])

		# If the id is passed
		if '_id' in req['data'] and req['data']['_id'] is not None:

			# If it doesn't match the logged in user, check permissions
			if req['data']['_id'] != req['session']['user']['_id']:
				self._verify(req['session']['user']['_id'], 'brain_user', access.UPDATE)

		# Else, use the user from the session
		else:

			# If the old password is missing
			if 'passwd' not in req['data']:
				return Services.Error(body.errors.DATA_FIELDS, [['passwd', 'missing']])

			# Store the session as the user ID
			req['data']['_id'] = req['session']['user']['_id']

		# Find the user
		oUser = User.get(req['data']['_id'])
		if not oUser:
			return Services.Error(body.errors.DB_NO_RECORD, (req['data']['_id'], 'user'))

		# If we have an old password
		if 'passwd' in req['data']:

			# Validate it
			if not oUser.password_validate(req['data']['passwd']):
				return Services.Error(body.errors.DATA_FIELDS, [['passwd', 'invalid']])

		# Make sure the new password is strong enough
		if not User.password_strength(req['data']['new_passwd']):
			return Services.Error(errors.PASSWORD_STRENGTH)

		# Set the new password and save
		oUser['passwd'] = User.password_hash(req['data']['new_passwd'])
		oUser.save(changes={'user': req['session']['user']['_id']})

		# Return OK
		return Services.Response(True)

	def user_passwd_forgot_create(self, req):
		"""User Password Forgot create

		Creates the key that will be used to allow a user to change their
		password if they forgot it

		Arguments:
			req (dict): The request details, which can include 'data',
						'environment', and 'session'

		Returns:
			Services.Response
		"""

		# Check minimum fields
		try: DictHelper.eval(req['data'], ['email', 'url'])
		except ValueError as e: return Services.Error(body.errors.DATA_FIELDS, [[f, 'missing'] for f in e.args])

		# Make sure the URL has the {key} field
		if '{key}' not in req['data']['url']:
			return Services.Error(body.errors.DATA_FIELDS, [['url', 'missing {key}']])

		# Look for the user by email
		dUser = User.filter({'email': req['data']['email']}, raw=['_id', 'locale'], limit=1)
		if not dUser:
			return Services.Response(False)

		# Generate a key
		sKey = self._create_key(dUser['_id'], 'forgot')

		# Forgot email template variables
		dTpl = {
			'key': sKey,
			'url': req['data']['url'].replace('{key}', sKey)
		}

		# Email the user the key
		oResponse = Services.create('mouth', 'email', {'data': {
			'_internal_': Services.internal_key(),
			'template': {
				'name': 'forgot_password',
				'locale': dUser['locale'],
				'variables': dTpl
			},
			'to': req['data']['email'],
		}})
		if oResponse.error_exists():
			Key.delete_get(sKey)
			return oResponse

		# Return OK
		return Services.Response(True)

	def user_passwd_forgot_update(self, req):
		"""User Password Forgot update

		Validates the key and changes the password to the given value

		Arguments:
			req (dict): The request details, which can include 'data',
						'environment', and 'session'

		Returns:
			Services.Response
		"""

		# Check minimum fields
		try: DictHelper.eval(req['data'], ['passwd', 'key'])
		except ValueError as e: return Services.Error(body.errors.DATA_FIELDS, [[f, 'missing'] for f in e.args])

		# Look up the key
		oKey = Key.get(req['data']['key'])
		if not oKey:
			return Services.Error(body.errors.DB_NO_RECORD, (req['data']['key'], 'key'))

		# Make sure the new password is strong enough
		if not User.password_strength(req['data']['passwd']):
			return Services.Error(errors.PASSWORD_STRENGTH)

		# Find the User
		oUser = User.get(oKey['user'])
		if not oUser:
			return Services.Error(body.errors.DB_NO_RECORD, (oKey['user'], 'user'))

		# Store the new password, mark verified, and update
		oUser['passwd'] = User.password_hash(req['data']['passwd'])
		oUser['verified'] = True
		oUser.save(changes=False)

		# Delete the key
		oKey.delete()

		# Return OK
		return Services.Response(True)

	def user_setup_read(self, req):
		"""User Setup read

		Validates the key exists and returns the user's info

		Arguments:
			req (dict): The request details, which can include 'data',
						'environment', and 'session'

		Returns:
			Services.Response
		"""

		# If the key is missing
		if 'key' not in req['data']:
			return Services.Error(body.errors.DATA_FIELDS, [['key', 'missing']])

		# Look up the key
		dKey = Key.get(req['data']['key'], raw=True)
		if not dKey:
			return Services.Error(body.errors.DB_NO_RECORD, (req['data']['key'], 'key'))

		# Get the user
		dUser = User.get(dKey['user'], raw=True)
		if not dUser:
			return Services.Error(body.errors.DB_NO_RECORD, (dKey['user'], 'user'))

		# Delete unnecessary fields
		for k in ['_id', '_created', '_updated', 'passwd', 'verified']:
			del dUser[k]

		# Return the user
		return Services.Response(dUser)

	def user_setup_update(self, req):
		"""User Setup update

		Finishes setting up the account for the user by setting their password
		and verified fields

		Arguments:
			req (dict): The request details, which can include 'data',
						'environment', and 'session'

		Returns:
			Services.Response
		"""

		# Verify the minimum fields
		try: DictHelper.eval(req['data'], ['passwd', 'key'])
		except ValueError as e: return Services.Error(body.errors.DATA_FIELDS, [[f, 'missing'] for f in e.args])

		# Look up the key
		oKey = Key.get(req['data']['key'])
		if not oKey:
			return Services.Error(body.errors.DB_NO_RECORD, (req['data']['key'], 'key'))
		req['data'].pop('key')

		# Find the user
		oUser = User.get(oKey['user'])
		if not oUser:
			return Services.Error(body.errors.DB_NO_RECORD, (oKey['user'], 'user'))

		# Make sure the new password is strong enough
		if not User.password_strength(req['data']['passwd']):
			return Services.Error(errors.PASSWORD_STRENGTH)

		# Pop off the password
		sPassword = req['data'].pop('passwd')

		# Go through the remaining fields and attempt to update
		lErrors = []
		for k in req['data']:
			try: oUser[k] = req['data'][k]
			except ValueError as e: lErrors.append(e.args[0])
		if lErrors:
			return Services.Error(body.errors.DATA_FIELDS, lErrors)

		# Set the new password, mark as verified, and save
		oUser['passwd'] = User.password_hash(sPassword)
		oUser['verified'] = True
		oUser.save(changes={'user': oKey['user']})

		# Delete the key
		oKey.delete()

		# Create a new session, store the user ID, and save it
		oSesh = Session.create()
		oSesh['user'] = {'_id': oUser['_id']}
		oSesh.save()

		# Return the session ID
		return Services.Response(oSesh.id())

	def users_by_email_read(self, req):
		"""Users By E-Mail read

		Finds a user given their unique email address

		Arguments:
			req (dict): The request details, which can include 'data',
						'environment', and 'session'

		Returns:
			Services.Response
		"""

		# If this is an internal request
		if '_internal_' in req['data']:

			# Verify the key, remove it if it's ok
			access.internal(req['data'])

			# Store the user ID as the system user
			sSessionUser = users.SYSTEM_USER_ID

		# Else, check permissions
		else:

			# Verify the rights
			if not self._verify(req['session']['user']['_id'], 'brain_user', access.READ):
				return Services.Error(body.errors.RIGHTS)

			# Store the user ID
			sSessionUser = req['session']['user']['_id']

		# If we are missing the ID
		if 'email' not in req['data']:
			return Services.Error(body.errors.DATA_FIELDS, [['email', 'missing']])

		# If the fields are passed
		if 'fields' in req['data']:

			# If it's not a list
			if not isinstance(req['data']['fields'], list):
				return Services.Error(body.errors.DATA_FIELDS, [['fields', 'must be an array']])

		# Else, set default fields
		else:
			req['data']['fields'] = ['_id', 'email', 'first_name', 'last_name']

		# If the order is passed
		if 'order' in req['data']:

			# If it's not a list
			if not isinstance(req['data']['order'], list):
				return Services.Error(body.errors.DATA_FIELDS, [['order', 'must be an array']])

		# Else, set default fields
		else:
			req['data']['order'] = ['first_name', 'last_name']

		# If we only got one email
		mLimit = isinstance(req['data']['email'], str) and 1 or None

		# Find and return the user(s)
		return Services.Response(
			User.get(req['data']['email'], index='email', raw=req['data']['fields'], orderby=req['data']['order'], limit=mLimit)
		)

	def users_by_id_read(self, req):
		"""Users By ID read

		Finds all users with a specific id

		Arguments:
			req (dict): The request details, which can include 'data',
						'environment', and 'session'

		Returns:
			Services.Response
		"""

		# If this is an internal request
		if '_internal_' in req['data']:

			# Verify the key, remove it if it's ok
			access.internal(req['data'])

			# Store the user ID as the system user
			sSessionUser = users.SYSTEM_USER_ID

		# Else, check permissions
		else:

			# Verify the rights
			if not self._verify(req['session']['user']['_id'], 'brain_user', access.READ):
				return Services.Error(body.errors.RIGHTS)

			# Store the user ID
			sSessionUser = req['session']['user']['_id']

		# If we are missing the ID
		if '_id' not in req['data']:
			return Services.Error(body.errors.DATA_FIELDS, [['_id', 'missing']])

		# If the fields are passed
		if 'fields' in req['data']:

			# If it's not a list
			if not isinstance(req['data']['fields'], list):
				return Services.Error(body.errors.DATA_FIELDS, [['fields', 'must be an array']])

		# Else, set default fields
		else:
			req['data']['fields'] = ['_id', 'email', 'first_name', 'last_name']

		# If the order is passed
		if 'order' in req['data']:

			# If it's not a list
			if not isinstance(req['data']['order'], list):
				return Services.Error(body.errors.DATA_FIELDS, [['order', 'must be an array']])

		# Else, set default fields
		else:
			req['data']['order'] = ['first_name', 'last_name']

		# Find and return the users
		return Services.Response(
			User.get(req['data']['_id'], raw=req['data']['fields'], orderby=req['data']['order'])
		)

	def verify_read(self, req):
		"""Verify read

		Checks the user currently in the session has access to the requested
		permission

		Arguments:
			req (dict): The request details, which can include 'data',
						'environment', and 'session'

		Returns:
			Services.Response
		"""

		# Check minimum fields
		try: DictHelper.eval(req['data'], ['name', 'right'])
		except ValueError as e: return Services.Error(body.errors.DATA_FIELDS, [[f, 'missing'] for f in e.args])

		# Verify and return the result
		return Services.Response(
			self._verify(
				req['session']['user']['_id'],
				req['data']['name'],
				req['data']['right']
			)
		)