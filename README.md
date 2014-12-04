hangouts-extractor
==================

A simple tool for extracting text messages from Google Hangouts JSON data. Alpha version. Half-working currently.

Sample usage: 

    python extract.py Hangouts.json "John Doe" john-log.txt

Extracts all messages from conversations that contain only two people with the format

    timestamp userid message
