from flask import Flask, render_template, redirect, request, Response
import jinja2
import requests
import json
import numpy as np
from cv2 import cv2
from bson import json_util
import aux
import base64

app = Flask(__name__)

if __name__ == '__main__':
    app.run(host='127.0.0.0', port=6001, debug=True)