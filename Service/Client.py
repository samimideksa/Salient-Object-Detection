import os
import grpc
# import inference
import inference_pb2
import inference_pb2_grpc
import base64

from PIL import Image
import  sys


from inspect import getsourcefile
import os.path
import sys
from Server import DetectObjectServicer

current_path = os.path.abspath(getsourcefile(lambda:0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]

sys.path.insert(0, parent_dir)

# from hed import Network ,estimate
import argparse

parser = argparse.ArgumentParser()


class ClientTest():
	def __init__(self,port='localhost:50051',image_output='client_out'):
		self.port = port
		self.image_output = image_output

	def open_grpc_channel(self):
		channel = grpc.insecure_channel('localhost:50051')
		stub = inference_pb2_grpc.DetectObjectStub(channel)
		return stub		

	def send_request(self,stub,im):
		print("here 1")
		img = Image.open(im)
		out_file_name = self.image_output+'.png'
		img = img.resize((480,320))
		img_b = img.tobytes() 


		image_file = inference_pb2.ImageFile(image = img_b)

		response = stub.DetectObject(image_file)
		# response = stub.DetectObject(image_file)
		# response = DetectObjectServicer.DetectObject(image_file)

		image = Image.frombytes(data=response.image,size=(320,320),mode='L')

		return image
	def close_channel(self,channel):
		pass


if __name__ == "__main__":
    parser.add_argument("--image_input",type=str,help='image path')
    parser.add_argument("--image_output",type=str,default='client_out',help='output image file name like "client_out"')
    parser.add_argument("--port",type=str,default='localhost:50051' ,help='port you are using like :   "localhost:50051" ')

    args = parser.parse_args()

    if len(sys.argv) == 1:
    	parser.print_help()
    	sys.exit()

    client_test = ClientTest(args)
    stub = client_test.open_grpc_channel()
    image = client_test.send_request(stub, args.image_input)
    image.save("try.jpg")