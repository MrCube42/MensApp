class Parser(object):
    """description of class"""

    def FindNode(self, sourceNode, nodeName):
        xpath = ".//{0}".format(nodeName)
        targetNode = sourceNode.find(xpath)
        return targetNode

    def FindAttributedNode(self, sourceNode, nodeName, attribute, attributeCompareValue):
        xpath = ".//{0}[@{1}='{2}']".format(nodeName, attribute, attributeCompareValue)
        targetNode = sourceNode.find(xpath)
        return targetNode

    def FindNodeValue(self, sourceNode, nodeName):
        targetNode = self.FindNode(sourceNode, nodeName)
        return targetNode.text

    def FindNodes(self, sourceNode, nodeName):
        xpath = ".//{0}".format(nodeName)
        nodes = sourceNode.findall(xpath)
        return nodes

    def FindNodeAttribute(self, sourceNode, attributeName):
        return sourceNode.get(attributeName)