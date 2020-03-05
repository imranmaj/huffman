import sys

from . import Tree, Compressor, Decompressor


assert len(sys.argv) == 4, "Takes 3 arguments (command: \"compress\" or \"decompress\", filename to compress/decompress, target filename)"
command = sys.argv[1]
assert command in ("compress", "decompress"), "Unknown command (available commands: \"compress\" and \"decompress\")"
filename = sys.argv[2]
target = sys.argv[3]

if command == "compress":
    with open(filename, "rb") as f:
        file = f.read()
    tree = Tree.from_bytes(file)
    tree.make()
    compressor = Compressor(tree, file)
    with open(target, "wb") as f:
        f.write(compressor.compress())
elif command == "decompress":
    with open(filename, "rb") as f:
        file = f.read()
    decompressor = Decompressor(file)
    with open(target, "wb") as f:
        f.write(decompressor.decompress())