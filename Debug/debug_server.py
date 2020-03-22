import sys 
from flask import Flask, request, jsonify, redirect, url_for, render_template

sys.path.insert(1, '../Backend/Ziggurats')

print(sys.path)