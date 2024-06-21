from flask import Flask, request, jsonify
import tensorflow as tens
from tensorflow.python.saved_model import signature_constants
import tensorflow.contrib.image
from tensorflow.python.saved_model import tag_constants
import bchlib
import os
from PIL import Image, ImageOps
import numpy


app = Flask(__name__)

# Loading the TensorFlow model
#model_path = 
sess = tens.InteractiveSession(graph=tens.Graph())
model = tens.saved_model.loader.load(sess, [tag_constants.SERVING], model_path)

'''
Retrieve the name of the input tensor for the secret message from the TensorFlow model's signature definition
Retrieve the name of the input tensor for the image from the TensorFlow model's signature definition
Fetch the actual tensor for the secret message from the TensorFlow graph using the retrieved name
Fetch the actual tensor for the image from the TensorFlow graph using the retrieved name
Retrieve the name of the output tensor for the encoding key from the TensorFlow model's signature definition
Retrieve the name of the output tensor for the residual from the TensorFlow model's signature definition
Fetch the actual tensor for the encoding key from the TensorFlow graph using the retrieved name
Fetch the actual tensor for the residual from the TensorFlow graph using the retrieved name
'''

#Defining input tensors
provided_secret = model.signature_def[signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY].inputs['secret'].name
provided_image = model.signature_def[signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY].inputs['image'].name
processed_secret = tens.get_default_graph().get_tensor_by_name(provided_secret)
processed_image = tens.get_default_graph().get_tensor_by_name(provided_image)

#Defining output tensors
output_name = model.signature_def[signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY].outputs['encoding_key'].name
residual_name = model.signature_def[signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY].outputs['residual'].name
final_output = tens.get_default_graph().get_tensor_by_name(output_name)
final_residual = tens.get_default_graph().get_tensor_by_name(residual_name)

#Defining BCH error-correcting code parameters
BCH_POLYNOMIAL = 137
BCH_BITS = 5
bch = bchlib.BCH(BCH_POLYNOMIAL, BCH_BITS)

@app.route('/encode_image', methods=['POST'])
def encode_image():
    #Processing the request
    data = request.get_json()
    image_path = data['image_path']
    secret = data['secret']
    save_dir = data['save_dir']

    #Encoding the secret message
    if len(secret) > 7:
        return jsonify({'error': 'Can only encode 56bits (7 characters) with ECC'}), 400

    data = bytearray(secret + ' '*(7-len(secret)), 'utf-8')
    ecc = bch.encode(data)
    packet = data + ecc

    packet_binary = ''.join(format(x, '08b') for x in packet)
    secret = [int(x) for x in packet_binary]
    secret.extend([0,0,0,0])

    #Loading and processing the image
    image = Image.open(image_path).convert("RGB")

    width = 400
    height = 400
    image = numpy.array(ImageOps.fit(image, (width, height)), dtype=numpy.float32)

    image /= 255.

    #Running the TensorFlow model
    feed_dict = {processed_secret: [secret],
                 processed_image: [image]}

    hidden_img, residual = sess.run([final_output, final_residual], feed_dict=feed_dict)

    #Processing the output images
    rescaled = (hidden_img[0] * 255).astype(numpy.uint8)
    raw_img = (image * 255).astype(numpy.uint8)
    residual = residual[0] +.5

    residual = (residual * 255).astype(numpy.uint8)

    #Saving the output images
    save_name = image_path.split('/')[-1].split('.')[0]

    imag = Image.fromarray(numpy.array(rescaled))
    imag.save(os.path.join(save_dir, f'{save_name}_hidden.png'))

    imag = Image.fromarray(numpy.squeeze(numpy.array(residual)))
    imag.save(os.path.join(save_dir, f'{save_name}_residual.png'))

    #Returning a success response
    return jsonify({'message': 'Sleuth successful'}), 200

if __name__ == "__main__":
    app.run(debug=True)