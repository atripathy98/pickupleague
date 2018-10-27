# FIREBASE CONNECTOR
# Author: Animesh Tripathy <a.tripathy101@gmail.com>
# Created: October 25, 2018
# Updated: October 26, 2018
# Purpose: Module for interacting with firebase realtime database

# Import Google Firebase Admin SDK and Async IO
import asyncio
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Certify provided credentials to gain access to database
cred = credentials.Certificate('resources/serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://risingsummoners-e4e70.firebaseio.com"
})

# ------------------------------------------------------
# METHOD: FIND_WITHIN
# RETURN TYPE: DICTIONARY
# PARAMETERS: (reference, searchterm, childterm)
# reference - String indicating FB reference
# searchterm - String value to search for
# childterm - String key to search value for
# RETURN PARAMETERS: (success, key)
# success - boolean value of searchterm being found
# key - optional string when success is true
# Returns key-value dictionary 
# ------------------------------------------------------
def find_within(reference, searchterm, childterm):
	response = {"success": False}
	search_ref = db.reference(reference)
	# Return OrderedDict()
	snapshot = search_ref.order_by_child(childterm).equal_to(searchterm).get()
	if len(snapshot) != 0:
		response["success"] = True
		actual_item = list(snapshot.items())
		response["key"] = actual_item[0][0]
	return response

# ------------------------------------------------------
# METHOD: INSERT_DATA
# PARAMETERS: (reference, datum)
# reference - String indicating FB reference
# datum - Dictionary to append to FB
# RETURN TYPE: NONE
# ------------------------------------------------------
def insert_data(reference, datum):
	main_ref = db.reference(reference)
	insert_ref = main_ref.push()
	datum["key"] = insert_ref.key
	insert_ref.set(datum)

# ------------------------------------------------------
# METHOD: UPDATE_DATA
# PARAMETERS: (reference, key, datum)
# reference - String indicating FB reference
# key - Unique string identifier of data
# datum - Dictionary to append to FB
# RETURN TYPE: NONE
# ------------------------------------------------------
def update_data(reference, key, datum):
	main_ref = db.reference(reference)
	update_ref = main_ref.child(key)
	update_ref.update(datum)

# ------------------------------------------------------
# METHOD: DELETE_DATA
# PARAMETERS: (reference, key, datum)
# reference - String indicating FB reference
# key - Unique string identifier of data
# RETURN TYPE: NONE
# ------------------------------------------------------
def delete_data(reference, key):
	main_ref = db.reference(reference)
	delete_ref = main_ref.child(key)
	delete_ref.delete()

# ------------------------------------------------------
# METHOD: ROLES_CHOSEN
# PARAMETERS: (key)
# key - Unique string identifier of data
# RETURN TYPE: BOOLEAN
# Returns if roles have been chosen for the user
# ------------------------------------------------------
def roles_chosen(key):
	main_ref = db.reference("/summoners")
	check_ref = main_ref.child(key)
	snapshot = check_ref.get()
	if "mainRole" in snapshot and "secRole" in snapshot:
		return True
	return False