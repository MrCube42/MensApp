﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import mock
from mock import Mock

from mensapp.services.argumentParser import ArgumentParser

class Test_ArgumentParser(unittest.TestCase):

    # the request for the argument parser must be mocked
    # so that the request.get() returns proper test values

    def test_HasMensaIdTrue(self):
        mockRequest = Mock()
        returnValues = ["42", "20150402", "20150407-20150410"]
        mockRequest.get.side_effect = lambda arg: returnValues.pop(0)
        parser = ArgumentParser(mockRequest)
        self.assertTrue(parser.HasMensaId())

    def test_HasMensaIdFalse(self):
        mockRequest = Mock()
        returnValues = ["", "20150402", "20150407-20150410"]
        mockRequest.get.side_effect = lambda arg: returnValues.pop(0)
        parser = ArgumentParser(mockRequest)
        self.assertFalse(parser.HasMensaId())

    def test_GetMensaId(self):
        idString = "4711"
        expectedId = int(idString)
        mockRequest = Mock()
        returnValues = [idString, "20150402", "20150407-20150410"]
        mockRequest.get.side_effect = lambda arg: returnValues.pop(0)
        parser = ArgumentParser(mockRequest)
        self.assertEqual(expectedId, parser.GetMensaId())

    def test_HasDatespanTrue(self):
        mockRequest = Mock()
        returnValues = ["42", "20150402", "20150407-20150410"]
        mockRequest.get.side_effect = lambda arg: returnValues.pop(0)
        parser = ArgumentParser(mockRequest)
        self.assertTrue(parser.HasDateSpan())

    def test_HasDatespanFalse(self):
        mockRequest = Mock()
        returnValues = ["42", "20150402", ""]
        mockRequest.get.side_effect = lambda arg: returnValues.pop(0)
        parser = ArgumentParser(mockRequest)
        self.assertFalse(parser.HasDateSpan())