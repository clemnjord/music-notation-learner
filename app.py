import os
import io
import tempfile
from flask import Flask
from flask import send_file
from music21 import *
import os, re


app = Flask(__name__)

@app.route('/')
def hello_world():
    response = "Bug"

    lpConverter = converter.subConverters.ConverterLilypond()

    data = converter.parse("tinynotation: 3/4 c4 d8 f g16 a g f#")

    filePath = lpConverter.write(data, fmt="lilypond", subformats=["png"])



    with open(str(filePath.absolute()), "rb") as file:

        # response = send_file(file, mimetype='image/png')
        response = send_file(io.BytesIO(file.read()), mimetype='image/png')

        pattern = "^" + str(filePath.name).strip(".png").replace(".", "\.") + ".*"

        print("**************\n", pattern, "\n********************")

        purge(str(filePath.parent), pattern)

    return response


def purge(dir, pattern):
    for f in os.listdir(dir):
        if re.search(pattern, f):
            os.remove(os.path.join(dir, f))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
