from flask import Flask , jsonify,request ,render_template
import os
app = Flask(__name__)

@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    return render_template("upload.html")






if __name__ == '__main__':
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT, debug=True)