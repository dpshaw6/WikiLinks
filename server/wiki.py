#!/usr/bin/python

import cgi
import cgitb
import sqlite3

cgitb.enable()

print("Content-Type: text/html;charset=utf-8")
print()

# Get the origin and destination as sent from the client
arguments = cgi.FieldStorage()
for key in arguments.keys():
	if key == "origin":
		origin = arguments[key].value
	if key == "destination":
		destination = arguments[key].value

# Spaces in the database are represented by underscores
origin = origin.replace(" ", "_")
destination = destination.replace(" ", "_")

# Connect to the database (assumed location is on the same machine as this script.
# I just put a softlink from where I had the actual database to the cgi-bin directory.)
dbconn = sqlite3.connect("wiki.sql")

print("<head>")
print("<title>Six Degrees of Wikipedia -- RESULTS!</title>")
print("</head>")
print("<body bgcolor=\"lightcyan\" text=\"maroon\"><h1>")

# Get the origin and destination ids from the database or return an error if 
# they're not present.
try:
	query = "SELECT id FROM page WHERE name = '" + destination +"';"
	destination_id = dbconn.execute(query).fetchone()[0]
except TypeError:
	print("Error: '" + str(arguments["destination"]) + "not found in database.")
	print("</h1></body></html>")
	exit()

try:
	query = "SELECT id FROM page WHERE name = '" + origin +"';"
	origin_id = dbconn.execute(query).fetchone()[0]
except TypeError:
	print("Error: '" + str(arguments["origin"]) + "not found in database.")
	print("</h1></body></html>")
	exit()

# Breadth-First-Search: We will search the potential links at each level of the link 
# structure, storing previously searched links in a dictionary to reduce the amount
# of database reads required
depth = 0
found = False
origins = []
origins.append(origin_id)
parents = {}
dest_dict = {}
while (not found):
	depth += 1
	num_origins = len(origins)
	i_origin = 0
	i_select_call = 0
	while i_origin < num_origins:
		current = origins.pop(0)
		try:
			# Check to see if we've already searched the database for this link
			destinations = dest_dict[current]
		except KeyError:
			# Query the database, if necessary
			query = "SELECT destination_id FROM link WHERE source_id = '" + str(current) + "';"
			destinations = dbconn.execute(query).fetchall()
			dest_dict[current] = destinations
			i_select_call += 1
		for destination in destinations:
			# Create a list of parents that a particular destination has
			try:
				current_list = parents[destination[0]]
			except KeyError:
				current_list = []
			current_list.append(current) 
			parents[destination[0]] = current_list
			if destination[0] == destination_id:
				# If we've reached the final destination, exit
				found = True
				break
			origins.append(destination[0])
		i_origin += 1

	if depth == 6: # It shouldn't get this far but, just so we don't fall into an infinite loop.
		break

if not found:
	print("Link exceeds 6 connections!")
	print("</h1></body></html>")
	exit()

print ("Found in " + str(depth) + " steps.")
print("</h1>")
print("<h2>")

# We know we found the links but now we need to find the path
next_id_from_top = origin_id
while depth > 0:
	next_ids = [destination_id]
	done = False
	while not done:
		next_id = next_ids.pop(0)
		query = "SELECT name FROM page WHERE id = '" + str(next_id) + "';"
		dest_name = dbconn.execute(query).fetchone()[0]
		parent_ids = parents[next_id]
		for parent_id in parent_ids:
			query = "SELECT name FROM page WHERE id = '" + str(parent_id) + "';"
			parent_name = dbconn.execute(query).fetchone()[0]
			if parent_id == next_id_from_top:
				done = True
				break
			next_ids.append(parent_id)

	print(parent_name.encode('ascii', 'ignore').decode('ascii') + " links to " + dest_name.encode('ascii', 'ignore').decode('ascii'))
	print("<br>")
	depth -= 1
	next_id_from_top = next_id

print("</h2></body></html>")
