#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from mensapp.services.xmlParser import XmlParser

class Test_XmlParser(unittest.TestCase):

    __Parser = XmlParser()

    __Xml = """
        <root>
            <node1>
                <node2>
                    <node3/>
                </node2>
            </node1>
            <node4>
                <node5 />
                <node6>I am a value</node6>
            </node4>
            <node7 theAttribute="fooBar" />
            <node8 theAttribute="foo" />
            <node1/>
        </root>
        """

    __NoneNodeExceptionMessage = "Given node must not be None."

    __NoneOrEmptyNameExceptionMesssage = "Given name must not be None or empty."

    def setUp(self):
        self.__RootNode = self.__Parser.GetRootNodeFromXml(self.__Xml)
        return super(Test_XmlParser, self).setUp()

    def test_GetRootNodeFromXml(self):
        expectedName = "root"
        self.assertEqual(expectedName, self.__RootNode.tag)

    def test_GetRootNodeFromXmlNone(self):
        expectedMessage = "XML must be a string."
        with self.assertRaises(ValueError) as cm:
            self.__Parser.GetRootNodeFromXml(None)
        exception = cm.exception
        self.assertEqual(expectedMessage, exception.message)

    def test_GetRootNodeFromXmlEmpty(self):
        expectedMessage = "Given XML is not valid ''"
        with self.assertRaises(ValueError) as cm:
            self.__Parser.GetRootNodeFromXml("")
        exception = cm.exception
        self.assertEqual(expectedMessage, exception.message)

    def test_GetRootNodeFromXmlInvalidShort(self):
        expectedMessage = "Given XML is not valid 'Trolololo'"
        with self.assertRaises(ValueError) as cm:
            self.__Parser.GetRootNodeFromXml("Trolololo")
        exception = cm.exception
        self.assertEqual(expectedMessage, exception.message)

    def test_GetRootNodeFromXmlInvalidLong(self):
        expectedMessage = "Given XML is not valid 'Trolololo12345678912...'"
        with self.assertRaises(ValueError) as cm:
            self.__Parser.GetRootNodeFromXml("Trolololo12345678912345")
        exception = cm.exception
        self.assertEqual(expectedMessage, exception.message)

    def test_FindNodeOuter(self):
        expectedName = "node1"
        node = self.__Parser.FindNode(self.__RootNode, expectedName)
        self.assertEqual(expectedName, node.tag)

    def test_FindNodeInner(self):
        expectedName = "node2"
        node = self.__Parser.FindNode(self.__RootNode, expectedName)
        self.assertEqual(expectedName, node.tag)

    def test_FindNodeInnerEmpty(self):
        expectedName = "node3"
        node = self.__Parser.FindNode(self.__RootNode, expectedName)
        self.assertEqual(expectedName, node.tag)

    def test_FindNodeInnerSecondLevel(self):
        expectedName = "node4"
        node = self.__Parser.FindNode(self.__RootNode, expectedName)
        self.assertEqual(expectedName, node.tag)

    def test_FindNodeInnerSecondLevelEmpty(self):
        expectedName = "node5"
        node = self.__Parser.FindNode(self.__RootNode, expectedName)
        self.assertEqual(expectedName, node.tag)

    def test_FindNodeNone(self):
        expectedMessage = self.__NoneNodeExceptionMessage
        with self.assertRaises(ValueError) as cm:
            node = self.__Parser.FindNode(None, "node1")
        exception = cm.exception
        self.assertEqual(expectedMessage, exception.message)

    def test_FindNodeNameNone(self):
        expectedMessage = self.__NoneOrEmptyNameExceptionMesssage
        with self.assertRaises(ValueError) as cm:
            node = self.__Parser.FindNode(self.__RootNode, None)
        exception = cm.exception
        self.assertEqual(expectedMessage, exception.message)

    def test_FindNodeNameEmpty(self):
        expectedMessage = self.__NoneOrEmptyNameExceptionMesssage
        with self.assertRaises(ValueError) as cm:
            node = self.__Parser.FindNode(self.__RootNode, "")
        exception = cm.exception
        self.assertEqual(expectedMessage, exception.message)

    def test_FindNodeValue(self):
        value = self.__Parser.FindNodeValue(self.__RootNode, "node6")
        expectedValue = "I am a value"
        self.assertEqual(expectedValue, value)

    def test_FindNodeValueNone(self):
        expectedMessage = self.__NoneNodeExceptionMessage
        with self.assertRaises(ValueError) as cm:
            node = self.__Parser.FindNodeValue(None, "node1")
        exception = cm.exception
        self.assertEqual(expectedMessage, exception.message)

    def test_FindNodeValueNameNone(self):
        expectedMessage = self.__NoneOrEmptyNameExceptionMesssage
        with self.assertRaises(ValueError) as cm:
            node = self.__Parser.FindNodeValue(self.__RootNode, None)
        exception = cm.exception
        self.assertEqual(expectedMessage, exception.message)

    def test_FindNodeValueNameEmpty(self):
        expectedMessage = self.__NoneOrEmptyNameExceptionMesssage
        with self.assertRaises(ValueError) as cm:
            node = self.__Parser.FindNodeValue(self.__RootNode, "")
        exception = cm.exception
        self.assertEqual(expectedMessage, exception.message)

    def test_FindNodes(self):
        exptectedCount = 2
        expectedName = "node1"
        nodes = self.__Parser.FindNodes(self.__RootNode, expectedName)
        self.assertEqual(exptectedCount, len(nodes))
        self.assertEqual(expectedName, nodes[0].tag)
        self.assertEqual(expectedName, nodes[1].tag)

    def test_FindNodesValueNone(self):
        expectedMessage = self.__NoneNodeExceptionMessage
        with self.assertRaises(ValueError) as cm:
            node = self.__Parser.FindNodes(None, "node1")
        exception = cm.exception
        self.assertEqual(expectedMessage, exception.message)

    def test_FindNodesValueNameNone(self):
        expectedMessage = self.__NoneOrEmptyNameExceptionMesssage
        with self.assertRaises(ValueError) as cm:
            node = self.__Parser.FindNodes(self.__RootNode, None)
        exception = cm.exception
        self.assertEqual(expectedMessage, exception.message)

    def test_FindNodesValueNameEmpty(self):
        expectedMessage = self.__NoneOrEmptyNameExceptionMesssage
        with self.assertRaises(ValueError) as cm:
            node = self.__Parser.FindNodes(self.__RootNode, "")
        exception = cm.exception
        self.assertEqual(expectedMessage, exception.message)

    def test_FindAttributedNode(self):
        expectedName = "node8"
        attributeValue = "foo"
        attributeName = "theAttribute"
        node = self.__Parser.FindAttributedNode(self.__RootNode, expectedName, attributeName, attributeValue)
        self.assertEqual(expectedName, node.tag)

    def test_FindAttributedNodeNone(self):
        expectedMessage = self.__NoneNodeExceptionMessage
        with self.assertRaises(ValueError) as cm:
            node = self.__Parser.FindAttributedNode(None, "node8", "theAttribute", "foo")
        exception = cm.exception
        self.assertEqual(expectedMessage, exception.message)

    def test_FindAttributedNodeNameNone(self):
        expectedMessage = self.__NoneOrEmptyNameExceptionMesssage
        with self.assertRaises(ValueError) as cm:
            node = self.__Parser.FindAttributedNode(self.__RootNode, None, "theAttribute", "foo")
        exception = cm.exception
        self.assertEqual(expectedMessage, exception.message)

    def test_FindAttributedNodeNameEmpty(self):
        expectedMessage = self.__NoneOrEmptyNameExceptionMesssage
        with self.assertRaises(ValueError) as cm:
            node = self.__Parser.FindAttributedNode(self.__RootNode, "", "theAttribute", "foo")
        exception = cm.exception
        self.assertEqual(expectedMessage, exception.message)

    def test_FindNodeAttribute(self):
        expectedAttributeValue = "fooBar"
        attributeName = "theAttribute"
        node = self.__Parser.FindAttributedNode(self.__RootNode, "node7", attributeName, expectedAttributeValue)
        attributeValue = self.__Parser.FindNodeAttribute(node, attributeName)
        self.assertEqual(expectedAttributeValue, attributeValue)

    def test_FindNodeAttributeNone(self):
        expectedMessage = self.__NoneNodeExceptionMessage
        with self.assertRaises(ValueError) as cm:
            node = self.__Parser.FindNodeAttribute(None, "foo")
        exception = cm.exception
        self.assertEqual(expectedMessage, exception.message)

    def test_FindNodeAttributeNameNone(self):
        node = self.__Parser.FindAttributedNode(self.__RootNode, "node7", "theAttribute", "fooBar")
        expectedMessage = self.__NoneOrEmptyNameExceptionMesssage
        with self.assertRaises(ValueError) as cm:
            node = self.__Parser.FindNodeAttribute(node, None)
        exception = cm.exception
        self.assertEqual(expectedMessage, exception.message)

    def test_FindNodeAttributeNameEmpty(self):
        node = self.__Parser.FindAttributedNode(self.__RootNode, "node7", "theAttribute", "fooBar")
        expectedMessage = self.__NoneOrEmptyNameExceptionMesssage
        with self.assertRaises(ValueError) as cm:
            node = self.__Parser.FindNodeAttribute(node, "")
        exception = cm.exception
        self.assertEqual(expectedMessage, exception.message)