"""
Module for testing flask api with unittest
"""
import json
import unittest
import urllib
from urllib import request
from urllib.error import HTTPError

class TestGet(unittest.TestCase):
    data = {'list_frame_contour': 'data/bounding_boxes/', "frame_path": 'data/image/'}
    data_bb_missing = {"frame_path": 'data/image/'}
    data_frame_missing = {'list_frame_contour': 'data/bounding_boxes/'}
    data_all_missing = {}
    def test_json_output(self):
        """
        test types of output request
        test values and length of output request
        :return:
        """
        url_values = urllib.parse.urlencode(self.data)
        url = "http://0.0.0.0:5000/Track/"
        full_url = url + '?' + url_values

        req = request.Request(full_url)

        result = request.urlopen(full_url).read()
        output = json.loads(result.decode("utf8"))

        self.assertEqual(type(output), dict)
        for k in output.keys():
            self.assertEqual(type(output[k]), list)
            for item in output[k]:
                self.assertEqual(type(item), int)

        self.assertEqual(output["frame 11"], [0])
        self.assertEqual(output["frame 18"], [0, 1])
        self.assertEqual(output["frame 518"], [62])

        self.assertNotIn("frame 519", output.keys())
        self.assertEqual(len(output), 519)

    def test_json_output_with_dict_input(self):
        """
        test types of output request
        test values and length of output request
        :return:
        """
        data_file = json.load(open('data/bounding_box.json', 'r'))
        data = {'list_frame_contour': json.dumps(data_file), "frame_path": 'data/image/'}

        url_values = urllib.parse.urlencode(data, quote_via=urllib.parse.quote)
        url = "http://0.0.0.0:5000/Track/"
        full_url = url + '?' + url_values

        req = request.Request(full_url)
        req.add_header('Content-Type', 'application/json; charset=utf-8')

        result = request.urlopen(full_url).read()
        result = request.urlopen(req).read()
        output = json.loads(result.decode("utf8"))

        self.assertEqual(type(output), dict)
        for k in output.keys():
            self.assertEqual(type(output[k]), list)
            for item in output[k]:
                self.assertEqual(type(item), int)

        self.assertEqual(output["frame 11"], [0])
        self.assertEqual(output["frame 18"], [0, 1])
        self.assertEqual(output["frame 518"], [62])

        self.assertNotIn("frame 519", output.keys())
        self.assertEqual(len(output), 519)

    def test_error_bb_missing(self):
        """
        tests error message values when list_frame_contour is missing
        :return:
        """
        url_values = urllib.parse.urlencode(self.data_bb_missing)
        url = "http://0.0.0.0:5000/Track/"
        full_url = url + '?' + url_values

        req = request.Request(full_url)
        with self.assertRaises(HTTPError):
            request.urlopen(req).read()

    def test_error_frame_missing(self):
        """
        tests error message values when frame_path is missing
        :return:
        """
        url_values = urllib.parse.urlencode(self.data_frame_missing)
        url = "http://0.0.0.0:5000/Track/"
        full_url = url + '?' + url_values

        req = request.Request(full_url)
        with self.assertRaises(HTTPError):
            request.urlopen(req).read()

    def test_error_all_missing(self):
        """
        tests error message values when list_frame_contour and frame_path are missing
        :return:
        """
        url_values = urllib.parse.urlencode(self.data_all_missing)
        url = "http://0.0.0.0:5000/Track/"
        full_url = url + '?' + url_values

        req = request.Request(full_url)
        with self.assertRaises(HTTPError):
            request.urlopen(req).read()