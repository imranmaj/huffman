# Huffman

An implementation of Huffman compression

## Requirements

No dependencies. Requires Python 3.8+.

## Usage

```
$ python -m huffman (compress | decompress) <target file> <destination/output file>
```

## Examples

#### To compress a file

If you have a file you want to compress named `example.txt`,

```
$ python -m huffman compress example.txt example.huff
```

will create a compressed version of the file called `example.huff`.

#### To decompress a file

If you have a file you want to decompress called `example.huff`,

```
$ python -m huffman decompress example.huff example.out
```

will create a decompressed version of the file called `example.out`.

## License

See `LICENSE.md` for the full license under which this software is provided.