

class NodeNotFoundError(Exception):
    pass

class LeafNotFoundError(NodeNotFoundError):
    pass

class TreeNotMadeError(Exception):
    pass