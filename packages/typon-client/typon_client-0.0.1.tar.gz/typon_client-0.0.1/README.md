# Typon Client

**Typon Client** is the client library for producing typon code.

```python
import lib_typ_parse.typon_client as typon_client

serviceEndpoint = 'http://127.0.0.1:8081'
api_key = 'API_KEY'
target_module = 'drivers.cache_server_driver'
module_dir = '/home/user/software/cache'
out_dir = '/home/user/software/cache/bin'
exe_name = 'cache_server_driver'

# retrieve .cpp source from server; stores .cpp file in {out_dir}/{exe_name}.cpp
# AND compiles {out_dir}/{exe_name}.cpp to {out_dir}/{exe_name}.exe
typon_client.compileCpp(serviceEndpoint, target_module, module_dir, out_dir, exe_name)
# retrieve .exe source from server; stores .exe file in {out_dir}/{exe_name}.exe
typon_client.compileExe(serviceEndpoint, api_key, target_module, module_dir, out_dir, exe_name)
```

This client intends to support modular software development in the typon language. E.g.

```python
# in {module_dir}
python3 -m {target_module}
```

Except only executable software is generated, not executed.

## Installing Typon Client and Supported Versions

Typon Client is available on PyPI:

```console
$ python3 -m pip install typon_client
```

Typon Client officially supports Python 3.7+.

## Typon Language

Typon is a statically typed language (derived from c++) with an efficient grammar resembling Python3.
This language seeks to capture the performance benefits of c++ while maintaining python level simplicity.
We list the basic grammatical constructs below; then we provide some sample code to fill in the blanks.
Typing is optional when the right-hand side is type resolvable.
Scope (e.g.) brackets are determined by indentation level, like in python.

```python
# type list
primitives = int, int32, uint32, uint64, dbl, char, str, bool, fileptr
# vector
varName: vec[item_type] = [v_1, ... , v_n]
# hash map
varName: hmap[key_type, val_type] = { k_1 : v_1, ... , k_n : v_n }
# sorted map
varName: smap[key_type, val_type] = s{ k_1 : v_1, ... , k_n : v_n }
# tuple
varName: tupl[type_1, ... , type_n ] = t[ v_1, ... , v_n ]

# typed statement
[varName]: [varType] = [varValue]
# non-typed statement
[varName] = [varValue]

# control flow
if [condition]:
  [statement]
else:
  [statement]

for [varName] in [vector]:
  [loopBody]

while [condition]:
  [loopBody]

# function definition
fxn [fxnName](arg_1: [type_1], ... , arg_n: [type_n]) -> [ret_type]:
  [fxn_body]

# class definition, no inheritance
class [className]():
  # constructor
  fxn __init__(args):
    [constructorBody]

  # destructor
  fxn __deinit__():
    [destructorBody]

# imports grammar
include [c_pkg_name]
import [subpkg].[module_name] as [module_alias]
```

## Typon Sample
Sample Typon Code to demonstrate features. Note that custom class instances must be deleted upon use.

```python
include ds_utils
import core.search_index as search_index
import utils.eval_utils as eval_utils
import utils.eval_utils2 as eval_utils2
import utils.eval_structs as eval_structs
import utils.search_utils as search_utils
import parsing.condition_parsing as condition_parsing

# resolution of attr_name type:
# on parse attr_name: check [table_obj.doc_attrs.attr_type_map]
# recall:
# [table_obj.doc_attrs.attr_type_map]: ( attr_id ) => ( attr_type in [ int, dbl, str ] )
# [ int, dbl, str ] ~ [ char(0), char(1), char(2) ]

class search_condition():

    fxn __members__():
        table_obj: search_index.search_table
        eval_tree: eval_structs.evaluation_tree
        valid: bool

    fxn __init__(
        table_obj: search_index.search_table,
        attr_cond_query: str,
        attr_cond_int_values: vec[int],
        attr_cond_dbl_values: vec[dbl],
        attr_cond_str_values: vec[str]
    ):

        this.table_obj = table_obj
        tok_stream = condition_parsing.tokenize_query_text( attr_cond_query, table_obj.condl_consts.delim_chars )
        eval_tree, parse_success = eval_utils2.compute_eval_tree(
            tok_stream,
            0,
            len(tok_stream),
            this,
            attr_cond_int_values,
            attr_cond_dbl_values,
            attr_cond_str_values
        )

        this.eval_tree = eval_tree

        this.valid = true
        if not parse_success:
            this.valid = false

    fxn __deinit__():
        delete this.eval_tree

    fxn matches_doc(
        doc_id: int
    ) -> bool:
        if not this.valid:
            return false

        eval_type = this.eval_tree.evaluate( doc_id, this )
        this.eval_tree.value_type = eval_type

        # case: undefined
        if eval_type == char(4):
            return false
        # case: bool
        if eval_type == char(3):
            return this.eval_tree.val_bool
        # case: str
        if eval_type == char(2):
            return len( this.eval_tree.val_str ) > 0
        # case: dbl
        if eval_type == char(1):
            return this.eval_tree.val_dbl != 0.0
        # case: int
        return this.eval_tree.val_int != 0
```
