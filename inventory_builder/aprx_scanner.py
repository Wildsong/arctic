"""
    We use ArcGIS Pro which keeps everything it does in APRX files.
    This script scans each APRX it finds and adds information about it
    to the database.

    It can't scan your C: drive! Don't keep APRX files there, put them
    on a server in a known place.
"""
import database

if __name__ == "__main__":
    print("All done! That was SOOOO fast!")

