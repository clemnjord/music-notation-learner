import os
import io
import tempfile
from flask import Flask
from flask import send_file
from music21 import *
import os, re
import logging
import random


app = Flask(__name__)

@app.route('/')
def hello_world():
    response = "Bug"

    lpConverter = converter.subConverters.ConverterLilypond()

    data = generate_notes()

    # filepath = lpConverter.write(data, fmt="svg")
    filepath = lpConverter.write(data, fmt="lilypond", subformats=["svg"])


    with open(str(filepath.absolute()), "rb") as file:
        response = send_file(io.BytesIO(file.read()), mimetype='image/svg+xml')

        pattern = "^" + str(filepath.name).strip(".svg").replace(".", "\.") + ".*"

        print("**************\n", str(filepath.parent), "\n********************")

        purge(str(filepath.parent), pattern)

    return response


def purge(dir, pattern):
    logging.info("Folder location: " + dir)
    for f in os.listdir(dir):
        if re.search(pattern, f):
            os.remove(os.path.join(dir, f))

def generate_notes():
    possible_notes = ["A", "B", "C", "D", "E", "F", "G"]
    possible_lengths = [1, 2, 4, 8, 16]

    file_str = io.StringIO()

    file_str.write("tinynotation: ")

    file_str.write("4/4 ")

    mesure_size = 1.0
    while mesure_size > 0:
        current_note = possible_notes[random.randint(0, len(possible_notes)-1)]

        length_index = random.randint(0, len(possible_lengths)-1)
        current_length = possible_lengths[length_index]

        while mesure_size - 1.0/current_length < 0:
            length_index = random.randint(length_index, len(possible_lengths)-1)
            current_length = possible_lengths[length_index]

        file_str.write(current_note + str(current_length) + " ")
        mesure_size -= 1.0/current_length

    return converter.parse(file_str.getvalue())


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
