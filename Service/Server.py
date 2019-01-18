import grpc
from concurrent import futures
import time

import inference_pb2
import inference_pb2_grpc
import sys
sys.path.append('..')
import infer

class DetectObjectServicer(inference_pb2_grpc.DetectObjectServicer):
	def DetectObject(self,request,context):
		print("Hello")
		response = inference_pb2.ImageFile()
		response.image = infer.predict(request.image)
		return response


class Server():
	def __init__(self):
		self.port = '[::]:50051'
		self.server = None
	def start_server(self):
		self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
		inference_pb2_grpc.add_DetectObjectServicer_to_server(DetectObjectServicer(),self.server)
		print('Starting server. Listening on port 50051.')
		self.server.add_insecure_port(self.port)
		self.server.start()		
	def stop_server(self):
		self.server.stop(0)

#  	