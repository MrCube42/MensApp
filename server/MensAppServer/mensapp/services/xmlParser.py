#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET

class XmlParser(object):
    """description of class"""

    def GetRootNodeFromXml(self, xml):
        try:
            root = ET.fromstring(xml)
        except ET.ParseError:
            maxLen = 20
            outXml = xml
            if len(xml) > maxLen:
                outXml = u"{0}...".format(xml[:maxLen])
            raise ValueError(u"Given XML is not valid '{0}'".format(outXml))
        except TypeError:
            raise ValueError("XML must be a string.")
        return root

    def FindNode(self, sourceNode, nodeName):
        self.__NodeNoneCheck(sourceNode)
        self.__NameNoneOrEmptyCheck(nodeName)
        xpath = u".//{0}".format(nodeName)
        targetNode = sourceNode.find(xpath)
        return targetNode

    def FindAttributedNode(self, sourceNode, nodeName, attribute, attributeCompareValue):
        self.__NodeNoneCheck(sourceNode)
        self.__NameNoneOrEmptyCheck(nodeName)
        xpath = u".//{0}[@{1}='{2}']".format(nodeName, attribute, attributeCompareValue)
        targetNode = sourceNode.find(xpath)
        return targetNode

    def FindNodeValue(self, sourceNode, nodeName):
        self.__NodeNoneCheck(sourceNode)
        self.__NameNoneOrEmptyCheck(nodeName)
        targetNode = self.FindNode(sourceNode, nodeName)
        return targetNode.text

    def FindNodes(self, sourceNode, nodeName):
        self.__NodeNoneCheck(sourceNode)
        self.__NameNoneOrEmptyCheck(nodeName)
        xpath = u".//{0}".format(nodeName)
        nodes = sourceNode.findall(xpath)
        return nodes

    def FindNodeAttribute(self, sourceNode, attributeName):
        self.__NodeNoneCheck(sourceNode)
        self.__NameNoneOrEmptyCheck(attributeName)
        return sourceNode.get(attributeName)

    def __NodeNoneCheck(self, node):
        if node is None:
            raise ValueError("Given node must not be None.")

    def __NameNoneOrEmptyCheck(self, name):
        if name is None or len(name) == 0:
            raise ValueError("Given name must not be None or empty.")