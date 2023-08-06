#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
#############################################################
#                                                           #
#      Copyright @ 2023 -  Dashingsoft corp.                #
#      All rights reserved.                                 #
#                                                           #
#      Pyarmor                                              #
#                                                           #
#      Version: 8.0.1 -                                     #
#                                                           #
#############################################################
#
#
#  @File: cli/ruler.py
#
#  @Author: Jondy Zhao (pyarmor@163.com)
#
#  @Create Date: Tue Feb  7 10:46:47 CST 2023
#

# Start of source code
#

import ast
import re

from fnmatch import fnmatchcase
from json import dumps as json_dumps


SCOPE_NODE_TYPES = ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef


def abs_name(qualname, name, level=0):
    if not level:
        return name
    if qualname.count('.') < level:
        raise RuntimeError('relative import overflow')
    return '.'.join(qualname.split('.')[:-level] + ([name] if name else []))


def apply_rule(name, rule):
    '''Return True if name matches rule, otherwise False

    >>> apply_rule('abc', '*c')
    True
    >>> apply_rule('abc', 'ab*')
    True
    >>> apply_rule('abc', 'a*c')
    True
    >>> apply_rule('abc', '/[a-z]+/')
    True
    >>> apply_rule('abc', 'xyz abc 123')
    True
    >>> apply_rule('abc', 'abc')
    True
    >>> apply_rule('abc', 'a b c')
    False
    '''

    if rule.startswith('*'):
        return name.endswith(rule[1:])
    elif rule.endswith('*'):
        return name.startswith(rule[:-1])
    elif rule.startswith('/'):
        return bool(re.match(rule[1:-1], name))
    elif rule.find(' ') > 0:
        return name in rule.split()
    else:
        return fnmatchcase(name, rule)


def check_rules(value, includes, excludes):
    return ((not includes or any([apply_rule(x, value) for x in includes]))
            and not any([apply_rule(x, value) for x in excludes]))


class Visitor(object):
    '''Travel each ndoe with its ancestors in stack

    >>> tree = ast.parse('a = b')

    >>> def show(item):
    ...     node, attr = item[:2]
    ...     s = type(node).__name__ + '.' + attr
    ...     if len(item) == 3:
    ...         s += '[%d]' % item[2]
    ...     return s

    >>> visitor = Visitor(tree)
    >>> for node in visitor.travel():
    ...     print('visit node:', type(node).__name__)
    ...     print('ancestors: ', [show(x) for x in visitor._stack])
    visit node: Assign
    ancestors:  ['Module.body[0]']
    visit node: Name
    ancestors:  ['Module.body[0]', 'Assign.targets[0]']
    visit node: Name
    ancestors:  ['Module.body[0]', 'Assign.value']
    '''

    def __init__(self, tree):
        self._tree = tree
        self._stack = []

    @property
    def stack(self):
        return [x for x in self._stack if isinstance(x, SCOPE_NODE_TYPES)]

    @property
    def domain(self):
        return '.'.join([x[0].name for x in self.stack])

    @property
    def top(self, n=0):
        return self._stack[-n - 1]

    def travel(self, ignored=None):

        def visit(node):
            for attr, child in ast.iter_fields(node):
                if attr in ('ctx',):
                    continue

                if ignored and isinstance(child, ignored):
                    continue

                if isinstance(child, ast.AST):
                    self._stack.append((node, attr))
                    yield child
                    for x in visit(child):
                        yield x
                    self._stack.pop()

                elif isinstance(child, list):
                    index = 0
                    for item in child:
                        if isinstance(item, ast.AST):
                            self._stack.append((node, attr, index))
                            yield item
                            for x in visit(item):
                                yield x
                            self._stack.pop()
                        index += 1

        for x in visit(self._tree):
            yield x


class Ruler(object):

    def __init__(self, includes, excludes):
        self._includes = includes if includes else []
        self._excludes = excludes if excludes else []

    def check(self, value):
        return check_rules(value, self._includes, self._excludes)


class NodeRuler(Ruler):

    def __init__(self, includes, excludes, visitor=None):
        super().__init__(includes, excludes)
        self._visitor = visitor


# Unused but reserved
def _check_node_rule(node, qualname, rule):
    n = rule.find(':')
    rscope = '' if n == -1 else rule[:n]
    rname = rule[n+1:]

    if qualname.startswith(rscope) or \
       (rscope[:1] == '@' and node.lineno == int(rscope[1:])):
        callee_name = get_node_name(node)
        if callee_name is None:
            return False
        if rname[0] == '=':
            return rname[1:] == callee_name
        elif rname[0] == '+':
            return callee_name.startswith(rname)
        elif rname[0] == '-':
            return callee_name.endswith(rname[1:])
        elif rname[0] == '*':
            # TBD: auto mode
            return False
        elif rname[0] == '/':
            return callee_name.find(rname[1:]) > -1
        elif rname[0] == '?':
            return re.search(rname[:1], callee_name) is not None
        else:
            return callee_name in rname.split()


############################################################
#
# Define classes and functions for module types
#
############################################################

class Dict(dict):

    def __getattr__(self, attr):
        if attr in self._FIELDS:
            return self[attr]
        raise AttributeError(attr)

    def __eq__(self, a):
        return self.name == a.name and self.cls == a.cls


class Field(Dict):

    _FIELDS = 'name', 'cls'

    def __init__(self, name, cls='', private=0):
        super().__init__(name=name, cls=cls)


class Type(Dict):

    _FIELDS = 'name', 'cls', 'fields', 'privates', 'imports'

    def __init__(self, name, cls='class'):
        super().__init__(name=name, cls=cls, fields=[], imports={})

    def append(self, field):
        if field and field not in self.fields:
            self.fields.append(field)

    def find(self, name):
        for x in self.fields:
            if name == x.name:
                return x
        for x in self.imports:
            if x == name:
                return self.imports[x]

    def imp_node(self, node, qualname=''):
        if isinstance(node, ast.Import):
            for x in node.names:
                asname = x.asname if x.asname else x.name
                self.imports[asname] = Field(x.name, 'module')

        elif isinstance(node, ast.ImportFrom):
            pkgname = '.' * node.level + node.module if node.module else ''
            for x in node.names:
                asname = x.asname if x.asname else x.name
                self.imports[asname] = Field(pkgname + ',' + x.name, '?')

    def add_node(self, node):
        name = node.id if isinstance(node, ast.Name) else \
            node.name if isinstance(node, SCOPE_NODE_TYPES) else \
            None
        if name:
            cls = '' if isinstance(node, ast.Name) else \
                'class' if isinstance(node, ast.ClassDef) else \
                'function' if isinstance(node, ast.FunctionDef) else \
                'asyncfunction'
            self.append(Field(name, cls))

    def extend(self, fields):
        for x in fields:
            if isinstance(x, ast.AST):
                self.add_node(x)
                continue

            self.append(x if isinstance(x, Field) else
                        Field(x) if isinstance(x, str) else
                        None)

    def __str__(self):
        return json_dumps(self, indent=2)


class ModuleInfo(object):

    def __init__(self, name=None, node=None, co=None):
        self._name = name
        self._node = node
        self._co = co

    def reset(self, name=None, node=None, co=None):
        self._name = name
        self._node = node
        self._co = co

    @property
    def module_types(self):
        return self._get_module_types(self._name, self._node)

    @property
    def using_modules(self):
        return self._get_using_modules(self._name, self._node)

    def _search_class_attrs(self, func):
        func_attrs = set()

        def visit(node):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Attribute):
                        stack = []
                        while isinstance(target, ast.Attribute):
                            stack.insert(0, target.attr)
                            target = target.value
                        if isinstance(target, ast.Name):
                            if target.id == prefix:
                                func_attrs.add(stack[0])

            elif isinstance(node, SCOPE_NODE_TYPES):
                func_attrs.add(node)

            else:
                for child in ast.iter_child_nodes(node):
                    visit(child)

        prefix = func.args.args[0].arg if func.args.args else '@'
        for x in func.body:
            visit(x)
        return func_attrs

    def _get_module_types(self, qualname, tree):
        module_types = {}
        scope = []

        def prepare(node):
            if isinstance(node, SCOPE_NODE_TYPES):
                key = '.'.join(scope)
                if key in module_types:
                    module_types[key].add_node(node)

                scope.append(node.name)

                if isinstance(node, ast.ClassDef):
                    key = '.'.join(scope)
                    # TBD: ? duplicated class names in one script
                    module_types[key] = Type(key)

            for child in ast.iter_child_nodes(node):
                prepare(child)

            if isinstance(node, SCOPE_NODE_TYPES):
                scope.pop()

        def visit(node):
            if isinstance(node, ast.Assign):
                key = '.'.join(scope)
                if key in module_types:
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            module_types[key].add_node(target)

            elif isinstance(node, ast.Import):
                key = '.'.join(scope)
                if key in module_types:
                    module_types[key].imp_node(node)

            elif isinstance(node, ast.ImportFrom):
                key = '.'.join(scope)
                if key in module_types:
                    # TBD: node.names = ['*']
                    module_types[key].imp_node(node, qualname)

            elif isinstance(node, SCOPE_NODE_TYPES):
                key = '.'.join(scope)
                scope.append(node.name)
                if key != qualname and key in module_types \
                   and hasattr(node, 'func') and hasattr(node, 'args') \
                   and 'staticmethod' not in node.decorator_list:
                    module_types[key].extend(self._search_class_attrs(node))

            for child in ast.iter_child_nodes(node):
                visit(child)

            if isinstance(node, SCOPE_NODE_TYPES):
                scope.pop()

        module_types[qualname] = Type(qualname, cls='module')
        scope = [qualname]
        prepare(tree)

        scope = [qualname]
        visit(tree)

        return module_types

    def _get_using_modules(self, qualname, tree):
        using_modules = set()

        def visit(node):
            if isinstance(node, ast.Import):
                using_modules.update([x.name for x in node.names])

            elif isinstance(node, ast.ImportFrom):
                using_modules.add(abs_name(qualname, node.module, node.level))

            else:
                for child in ast.iter_child_nodes(node):
                    visit(child)

        visit(tree)
        return using_modules

    # The following methodes are unused
    def _get_hidden_imports(self, tree):
        hidden_imports = []

        def visit(node):
            if (isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id in ('__import__', '__dict__')
                and node.func.args
                and isinstance(node.func.args[0], (ast.Str, ast.Constant))):
                # TODO: __import__(x, , , from_list, level)
                pass

            elif (isinstance(node, ast.Call)
                  and isinstance(node.func, ast.Name)
                  and node.func.id in ('getattr', 'setattr')
                  and len(node.args) > 1
                  and isinstance(node.args[0], (ast.Name))
                  and isinstance(node.args[1], (ast.Str, ast.Constant))):
                # TODO: getattr or setattr for node.args[0].id
                pass

            for child in ast.iter_child_nodes(node):
                visit(child)

        visit(tree)
        return hidden_imports

    def _get_chain_attrs(self, tree):
        chain_attrs = {}
        scope = []

        def visit(node):
            if isinstance(node, SCOPE_NODE_TYPES):
                scope.append(node.name)

            elif isinstance(node, ast.Attribute):
                stack = []
                attrnode = node
                while isinstance(attrnode, ast.Attribute):
                    stack.insert(0, attrnode.attr)
                    attrnode = attrnode.value

                key = '.'.join(scope)
                chain_attrs.setdefault(key, set())

                # case: a.b.c
                if isinstance(attrnode, ast.Name):
                    chain_attrs[key].add('.'.join([attrnode.id] + stack))
                    return

                # case: Cls().x.y.z
                elif (isinstance(attrnode, ast.Call) and
                      isinstance(attrnode.func, ast.Name)):
                    chain_attrs[key].add('.'.join([attrnode.func.id] + stack))
                    return

                # case: 'abc'.join(...)
                elif isinstance(attrnode, (ast.Str, ast.Constant)):
                    value = getattr(attrnode,
                                    's' if hasattr(attrnode, 's') else 'value')
                    chain_attrs[key].add('.'.join([type(value)] + stack))
                    return

                else:
                    chain_attrs[key].add('.'.join(['?'] + stack))
                    node = attrnode

            for child in ast.iter_child_nodes(node):
                visit(child)

            if isinstance(node, SCOPE_NODE_TYPES):
                scope.pop()

        visit(tree)
        return chain_attrs

    def _get_body_names(self, node):
        attrs = set()

        def visit(node):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        attrs.add(target)

            elif isinstance(node, SCOPE_NODE_TYPES):
                attrs.add(node)

            else:
                for child in ast.iter_child_nodes(node):
                    visit(child)

        for x in node.body:
            visit(x)
        return attrs

    def _get_module_names(self, tree):
        module_names = {}
        scope = []

        def visit(node):
            if isinstance(node, SCOPE_NODE_TYPES):
                scope.append(node.name)

            elif isinstance(node, ast.Name):
                key = '.'.join(scope)
                module_names.setdefault(key, set())
                module_names[key].add(node.id)
                return

            for child in ast.iter_child_nodes(node):
                visit(child)

            if isinstance(node, SCOPE_NODE_TYPES):
                scope.pop()

        visit(tree)
        return module_names

    def _get_module_attrs(self, tree):
        module_attrs = set()

        def visit(node):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        module_attrs.add(target.id)

            elif isinstance(node, SCOPE_NODE_TYPES):
                module_attrs.add(node.name)

            else:
                for child in ast.iter_child_nodes(node):
                    visit(child)

        def visit2(node):
            if isinstance(node, ast.Global):
                module_attrs.update(node.names)

            else:
                for child in ast.iter_child_nodes(node):
                    visit2(child)

        visit(tree)
        visit2(tree)
        return module_attrs

    def _get_import_names(self, tree):
        import_names = {}

        def visit(node):
            if isinstance(node, ast.ImportFrom):
                name = '.' * node.level + node.module if node.module else ''
                import_names.setdefault(name, set())
                import_names[name].update([x.name for x in node.names])
            else:
                for child in ast.iter_child_nodes(node):
                    visit(child)

        visit(tree)
        return import_names

    def _get_import_modules(self, tree):
        import_modules = {}

        def visit(node):
            if isinstance(node, ast.Import):
                for name, asname in [(x.name, x.asname) for x in node.names]:
                    import_modules[asname if asname else name] = name

            else:
                for child in ast.iter_child_nodes(node):
                    visit(child)

        visit(tree)
        return import_modules

    def _get_import_attrs(self, tree):
        module_attrs = {}
        Attr = ast.Attribute
        Name = ast.Name

        def visit(node):
            if isinstance(node, Attr) and isinstance(node.value, Name):
                name = node.value.id
                if name in self.import_modules:
                    module_attrs.setdefault(name, set())
                    module_attrs[name].add(node.attr)
            else:
                for child in ast.iter_child_nodes(node):
                    visit(child)

        visit(tree)
        return module_attrs

    def _get_mapped_names(self, tree):
        mapped_names = {'': set(self._get_module_attrs(tree))}
        scope = []

        def visit(node):
            if isinstance(node, SCOPE_NODE_TYPES):
                if scope:
                    key = '.'.join(scope)
                    mapped_names.setdefault(key, set())
                    mapped_names[key].add(node.name)
                scope.append(node.name)

            for child in ast.iter_child_nodes(node):
                visit(child)

            if isinstance(node, SCOPE_NODE_TYPES):
                scope.pop()

        visit(tree)
        return mapped_names


class PackageRelations(object):

    def __init__(self, ctx):
        self.ctx = ctx

    def _import_star_names(self, modname):
        try:
            return dir(__import__(modname))
        except ModuleNotFoundError:
            pass

    def process(self, clean=True):
        for res in self.ctx.resources:
            if not res.is_script():
                continue

            if not res.mtree:
                res.reparse()

            qualname = res.fullname
            minfo = ModuleInfo(qualname, res.mtree)

            self.ctx.module_types.update(minfo.module_types)
            self.ctx.module_relations[qualname] = minfo.using_modules

            if clean:
                res.clean()

#
# End of source code


if __name__ == "__main__":
    import doctest
    doctest.testmod()
