import sys
sys.path.insert(0, 'Service/')

from Client import ClientTest
from Server import *
from PIL import Image
import unittest
import numpy as np 
import subprocess
import torch.nn as nn
import torch


class TestSuiteGrpc(unittest.TestCase):
    def setUp(self):
    	self.image = Image.open('/test/animal2.jpg')
    	self.server = Server()
    	self.server.start_server()
    	self.client = ClientTest()



    def test_grpc_call(self):
    	stub = self.client.open_grpc_channel()
    	result_image = self.client.send_request(stub,self.image)
    	result_image =  result_image.resize((480,320))
    	result_image.save("test/client_out2.png")


    	img_res = np.asarray(Image.open("images/client_out2.png").convert('L'))
    	img_expected = np.asarray(Image.open("images/client_out.png").convert('L'))
    	assert (img_res==img_expected).all()
    	

    def tearDown(self):
        # self.client.channel.close()
        self.server.stop_server()



if __name__ == '__main__':
    suite = unittest.TestSuite()

    suite.addTest(TestSuiteGrpc("test_grpc_call"))
    unittest.main()
