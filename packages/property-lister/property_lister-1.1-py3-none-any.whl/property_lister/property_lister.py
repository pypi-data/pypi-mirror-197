#!/usr/bin/env python3

import datetime
import sys
import os
import sqlite3
import shutil
import re
import binascii
import biplist
import plistlib

start = datetime.datetime.now()

# -------------------------- INFO --------------------------

def basic():
	global proceed
	proceed = False
	print("Property Lister v1.1 ( github.com/ivan-sincek/property-lister )")
	print("")
	print("Usage:   property-lister -db database [-o out   ]")
	print("Example: property-lister -db Cache.db [-o plists]")

def advanced():
	basic()
	print("")
	print("DESCRIPTION")
	print("    Extract property list files from an SQLite unencrypted database file")
	print("DATABASE")
	print("    SQLite unencrypted database file")
	print("    -db <database> - Cache.db | etc.")
	print("OUT")
	print("    Output directory")
	print("    All extracted propery list files will be saved in this directory")
	print("    -o <out> - plists | etc.")

# ------------------- MISCELENIOUS BEGIN -------------------

def read_database(file):
	tmp = ""
	with sqlite3.connect(file) as db:
		tmp = ("").join(db.iterdump())
	db.close()
	return tmp

def remove_directory(directory):
	removed = True
	try:
		if os.path.exists(directory):
			shutil.rmtree(directory)
	except Exception:
		removed = False
		print(("Cannot remove '{0}' related directories/subdirectories and/or files").format(directory))
	return removed

def create_directory(directory):
	created = True
	try:
		if not os.path.exists(directory):
			os.mkdir(directory)
	except Exception:
		created = False
		print(("Cannot create '{0}' related directories/subdirectories and/or files").format(directory))
	return created

def check_directory(directory):
	success = False
	overwrite = "yes"
	if os.path.exists(directory):
		print(("'{0}' directory already exists").format(directory))
		overwrite = input("Overwrite the output directory (yes): ").lower()
	if overwrite == "yes" and remove_directory(directory):
		success = create_directory(directory)
	return success

# -------------------- MISCELENIOUS END --------------------

# -------------------- VALIDATION BEGIN --------------------

# my own validation algorithm

proceed = True

def print_error(msg):
	print(("ERROR: {0}").format(msg))

def error(msg, help = False):
	global proceed
	proceed = False
	print_error(msg)
	if help:
		print("Use -h for basic and --help for advanced info")

args = {"database": None, "out": None}

# TO DO: Better site validation.
def validate(key, value):
	global args
	value = value.strip()
	if len(value) > 0:
		if key == "-db" and args["database"] is None:
			args["database"] = value
			if not os.path.isfile(args["database"]):
				error("File does not exists")
			elif not os.access(args["database"], os.R_OK):
				error("File does not have read permission")
			elif not os.stat(args["database"]).st_size > 0:
				error("File is empty")
			else:
				args["database"] = read_database(args["database"])
				if not args["database"]:
					error("Cannot read database")
		elif key == "-o" and args["out"] is None:
			args["out"] = os.path.abspath(value)

def check(argc, args):
	count = 0
	for key in args:
		if args[key] is not None:
			count += 1
	return argc - count == argc / 2

# --------------------- VALIDATION END ---------------------

# ----------------- GLOBAL VARIABLES BEGIN -----------------

ext_blob = ".dump.blob"
ext_plist = ".dump.plist"
ext_plist_xml = ext_plist + ".xml"

# ------------------ GLOBAL VARIABLES END ------------------

# ----------------------- TASK BEGIN -----------------------

def dump(database, out):
	count = 0
	blobs = re.findall(r"(?<=,x')[\w\d]+", database, re.IGNORECASE)
	if not blobs:
		print("No binary blobs were found")
	else:
		for blob in blobs:
			count += 1
			open(out + os.path.sep + str(count) + ext_blob, "wb").write(binascii.unhexlify(blob))
	return count

def extract(file):
	try:
		data = biplist.readPlist(file)
		os.rename(file, file.replace(ext_blob, ext_plist))
		if isinstance(data, dict):
			count = 0
			for key in data:
				if isinstance(data[key], biplist.Data):
					count += 1
					file = file.replace(ext_plist, "." + str(count) + ext_plist)
					biplist.writePlist(biplist.readPlistFromString(data[key]), file) # NOTE: Extract a property list file from a property list file.
					extract(file)
	except (biplist.InvalidPlistException, biplist.NotBinaryPlistException):
		pass

def convert(file):
	try:
		data = None
		with open(file, "rb") as stream:
			data = plistlib.load(stream)
		stream.close()
		if data:
			open(file, "wb").write(plistlib.dumps(data, fmt = plistlib.FMT_XML))
			os.rename(file, file.replace(ext_plist, ext_plist_xml))
	except (plistlib.InvalidFileException):
		pass

def main():
	argc = len(sys.argv) - 1

	if argc == 0:
		advanced()
	elif argc == 1:
		if sys.argv[1] == "-h":
			basic()
		elif sys.argv[1] == "--help":
			advanced()
		else:
			error("Incorrect usage", True)
	elif argc % 2 == 0 and argc <= len(args) * 2:
		for i in range(1, argc, 2):
			validate(sys.argv[i], sys.argv[i + 1])
		if args["database"] is None or args["out"] is None or not check(argc, args):
			error("Missing a mandatory option (-db, -o)", True)
	else:
		error("Incorrect usage", True)

	if proceed and check_directory(args["out"]):
		print("##########################################################################")
		print("#                                                                        #")
		print("#                          Property Lister v1.1                          #")
		print("#                                     by Ivan Sincek                     #")
		print("#                                                                        #")
		print("# Extract property list files from an SQLite unencrypted database file.  #")
		print("# GitHub repository at github.com/ivan-sincek/property-lister.           #")
		print("# Feel free to donate bitcoin at 1BrZM6T7G9RN8vbabnfXu4M6Lpgztq6Y14.     #")
		print("#                                                                        #")
		print("##########################################################################")
		if dump(args["database"], args["out"]):
			for file in os.listdir(args["out"]):
				if file.endswith(ext_blob):
					extract(args["out"] + os.path.sep + file)
			for file in os.listdir(args["out"]):
				if file.endswith(ext_plist):
					convert(args["out"] + os.path.sep + file)
		print(("Script has finished in {0}").format(datetime.datetime.now() - start))

if __name__ == "__main__":
	main()

# ------------------------ TASK END ------------------------
