import tensorflow as tf
import numpy as np
import os
import argparse
import sys
from PIL import Image
import numpy as np



def predict(img_bytes,gpu_fraction = 1.0):
	"""
		given image byte as a input it returns
		image byte of object detected 

		input 
			320*320*3 image 
			converted to byte 

		output
			320*320*1 image 
			converted to byte 
	"""
	gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction = gpu_fraction)
	with tf.Session(config=tf.ConfigProto(gpu_options = gpu_options)) as sess:
		saver = tf.train.import_meta_graph('../meta_graph/my-model.meta')
		saver.restore(sess,tf.train.latest_checkpoint('../salience_model'))
		image_batch = tf.get_collection('image_batch')[0]
		pred_mattes = tf.get_collection('mask')[0]

	
		img = Image.frombytes(data=img_bytes,size=(320,320),mode='RGB')
		img  = np.asarray(img).reshape(1, 320,320,3)
		feed_dict = {image_batch:img}
		pred_alpha = sess.run(pred_mattes,feed_dict = feed_dict)
		img_array = pred_alpha[0]
		img_array = img_array.reshape(320,320)
		final_img = Image.fromarray(img_array* 255)
		img_b = final_img.convert('L').tobytes()
		return img_b







img = Image.open("man-eaten-by-lions.jpg")
img = img.resize((320,320))
img_b = img.tobytes() 
i = predict(img_b)
image = Image.frombytes(data=i,size=(320,320),mode='L')
image.convert('L').save("test.png", "PNG", optimize=True)

