# thrift-parser

```bash
pip install thrift-parser
```

`Thrift.g4` is from https://github.com/antlr/grammars-v4


## parse

```python
from thrift_parser import parse_file

lexer, tokens, parser, document = parse_file('tutorial.thrift')
```
or smiple

```python
from thrift_parser import ThriftData

thrift_data = ThriftData.from_file('tutorial.thrift')

print(thrift_data.tokens[0].text)
print(thrift_data.document.children)
```

or you can try antlr's way

```python
from antlr4 import FileStream
from antlr4 import CommonTokenStream
from antlr4 import ParserRuleContext

from thrift_parser.ThriftLexer import ThriftLexer
from thrift_parser.ThriftParser import ThriftParser


def main(file):
    input_stream = FileStream(file, encoding='utf8')
    lexer = ThriftLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ThriftParser(stream)
    ctx = ParserRuleContext()

    parser.enterRule(ctx, 0, 0)
    document = parser.document()
    return document

```


# Why ?

python thrift parser --> thrift-fmt --> auto format my thrift files in one style


# TODO

1. more ast operate, fake_token, fake_context
2. other language?
