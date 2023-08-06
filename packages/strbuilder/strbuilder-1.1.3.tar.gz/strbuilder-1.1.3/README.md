# A simple string builder

## sample

```python
from strbuilder import Builder, SurroundBuilder

condition = False

print(
    Builder('base', separator='\n')
    .write('header')
    .write(Builder(separator=', ')
        .write('aaa')
        .write_if(condition, 'bbb')
        .write_if(condition, 'ccc', or_else='ddd'))
    .write(SurroundBuilder(surround='{}')
        .write('surrounded!'))
    .write('footer')
    .build()
)
```

## output

```txt
base
header
aaa, ddd
{surrounded!}
footer
```
