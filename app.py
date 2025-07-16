from flask import Flask, request, send_from_directory
from image_filter import apply_film_filter
from PIL import Image as img, ImageFilter as imgf
import math
import numpy as np
app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome to the film filter!'

form_html = """
<html>
  <head>
    <style>
      body {
        background-color: #fdf6f0;
        font-family: 'Segoe UI', sans-serif;
        color: #4b2e2e;
        text-align: center;
        padding-top: 50px;
      }

      h1 {
        color: #a0522d;
      }

      input[type="file"],
      input[type="submit"] {
        margin: 10px;
        padding: 10px;
        border-radius: 5px;
        border: none;
        font-size: 1em;
      }

      input[type="submit"] {
        background-color: #d8a16f;
        color: white;
        cursor: pointer;
      }

      input[type="submit"]:hover {
        background-color: #c58657;
      }
    </style>
  </head>
  <body>
    <h1>Upload a Photo</h1>
    <form method="POST" enctype="multipart/form-data">
      <label>Select your photo:</label><br>
      <input type="file" name="file"><br>
      <input type="submit" value="Apply Film Filter">
    </form>
  </body>
</html>

"""

original_upload = """
<html>
  <head>
    <style>
      body {
        background-color: #fdf6f0;
        font-family: 'Segoe UI', sans-serif;
        color: #4b2e2e;
        text-align: center;
        padding: 50px;
      }

      h1 {
        color: #a0522d;
        margin-bottom: 40px;
      }

      .images {
        display: flex;
        justify-content: center;
        gap: 40px;
      }

      .images img {
        width: 300px;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
      }

      a {
        display: inline-block;
        margin-top: 40px;
        text-decoration: none;
        color: #a0522d;
        font-weight: bold;
      }
    </style>
  </head>
  <body>
    <h1>Before & After</h1>
    <div class="images">
      <div>
        <p><strong>Original</strong></p>
        <img src="/uploads/original.jpg">
      </div>
      <div>
        <p><strong>Filtered</strong></p>
        <img src="/uploads/filtered.png">
      </div>
    </div>
    <a href="/upload">Try Another Photo</a>
  </body>
</html>

"""

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    method = request.method

    if method == "POST":
        print("Method is POST!")
        file = request.files["file"]
        file.save("uploads/original.jpg")
        base_img = img.open("uploads/original.jpg")
        filtered_img = apply_film_filter(base_img)
        filtered_img.save("uploads/filtered.png")

        return original_upload    
    else:
        return form_html


print(app.url_map)

import os
port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)
