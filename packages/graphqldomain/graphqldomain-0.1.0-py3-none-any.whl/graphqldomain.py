"""A GraphQL domain for Sphinx."""
from typing import (
    Dict,
    Iterable,
    Iterator,
    List,
    NamedTuple,
    Optional,
    Sequence,
    Tuple,
    Type,
)

from docutils import nodes
from docutils.nodes import Element
from docutils.parsers.rst import Directive, directives
from graphql.language import ast as gql_ast
from graphql.language.parser import Parser
from graphql.language.token_kind import TokenKind
from sphinx import addnodes
from sphinx.addnodes import desc_signature, pending_xref
from sphinx.application import Sphinx
from sphinx.builders import Builder
from sphinx.directives import ObjectDescription
from sphinx.domains import Domain, Index, IndexEntry, ObjType
from sphinx.environment import BuildEnvironment
from sphinx.roles import XRefRole
from sphinx.util.docfields import GroupedField
from sphinx.util import logging
from sphinx.util.nodes import make_refnode

__version__ = "0.1.0"
logger = logging.getLogger(__name__)


class ObjectEntry(NamedTuple):
    """Information about a declared object for use in indexing the domain.

    These are created in :method:`GQLObject.add_target_and_index`
    for use in :class:`GraphQLSchemaIndex`.
    """

    docname: str
    """The name of the Sphinx document that the object was declared in."""
    node_id: str
    """The identifier of the declared object.

    This is the fully qualified name of the type.
    They are already guaranteed to be unique or they would create conflicts in the schema.
    """


class GQLObject(ObjectDescription[Tuple[str, Optional[str]]]):
    """The base class for any GraphQL type."""

    option_spec = {
        "noindex": directives.flag,
    }
    doc_field_types = [
        GroupedField(
            "argument",
            label="Arguments",
            names=("arg", "argument"),
        ),
    ]

    obj_type: str
    """The name of the type.

    This is used as a key in the domain data and as the name of the Sphinx object type.
    Therefore any value of :attr:``obj_type`` must also exist in
    :attr:`GQLDomain.initial_data` and :attr:`GQLDomain.object_types`.
    """
    parent_type: Optional[str] = None

    def add_target_and_index(
        self, name: Tuple[str, Optional[str]], sig: str, signode: desc_signature
    ) -> None:
        node_id = signode["fullname"]

        signode["ids"].append(node_id)
        if "noindex" not in self.options:
            self.env.domaindata["gql"][self.obj_type][
                signode["fullname"]
            ] = ObjectEntry(
                self.env.docname,
                node_id,
            )

    def _handle_signature_directives(
        self, signode: desc_signature, ast_nodes: Sequence[gql_ast.ConstDirectiveNode]
    ) -> None:
        for directive_node in ast_nodes:
            signode += addnodes.desc_sig_space()

            signode += addnodes.desc_sig_operator("", "@")
            directive_name = directive_node.name.value
            signode += pending_xref(
                "",
                nodes.Text(directive_name),
                refdomain="gql",
                reftype="directive",
                reftarget=directive_name,
                refspecific=True,
            )

            self._handle_signature_const_arguments(signode, directive_node.arguments)

    def _handle_signature_const_arguments(
        self, signode: desc_signature, ast_nodes: Sequence[gql_ast.ConstArgumentNode]
    ) -> None:
        if not ast_nodes:
            return

        signode += addnodes.desc_sig_operator("", "(")

        for i, argument_node in enumerate(ast_nodes):
            if i != 0:
                signode += addnodes.desc_sig_punctuation("", ",")
                signode += addnodes.desc_sig_space()

            signode += addnodes.desc_sig_name("", argument_node.name.value)
            signode += addnodes.desc_sig_punctuation("", ":")
            signode += addnodes.desc_sig_space()
            self._handle_signature_literal(signode, argument_node.value)

        signode += addnodes.desc_sig_operator("", ")")

    def _handle_signature_input_values(
        self,
        signode: desc_signature,
        ast_nodes: Sequence[gql_ast.InputValueDefinitionNode],
    ) -> None:
        if not ast_nodes:
            return

        signode += addnodes.desc_sig_operator("", "(")

        for i, argument_node in enumerate(ast_nodes):
            if i != 0:
                signode += addnodes.desc_sig_punctuation("", ",")
                signode += addnodes.desc_sig_space()

            signode += addnodes.desc_sig_name("", argument_node.name.value)
            signode += addnodes.desc_sig_punctuation("", ":")
            signode += addnodes.desc_sig_space()
            self._handle_signature_type_reference(signode, argument_node.type)
            self._handle_signature_default_value(signode, argument_node.default_value)
            self._handle_signature_directives(signode, argument_node.directives)

        signode += addnodes.desc_sig_operator("", ")")

    def _handle_signature_default_value(
        self, signode: desc_signature, ast_nodes: Optional[gql_ast.ConstValueNode]
    ) -> None:
        if not ast_nodes:
            return

        signode += addnodes.desc_sig_space()
        signode += addnodes.desc_sig_operator("", "=")
        signode += addnodes.desc_sig_space()

        self._handle_signature_literal(signode, ast_nodes)

    def _handle_signature_literal(
        self, signode: desc_signature, ast_nodes: Optional[gql_ast.ConstValueNode]
    ) -> None:
        if isinstance(ast_nodes, gql_ast.ListValueNode):
            signode += addnodes.desc_sig_operator("", "[")
            for i, item_node in enumerate(ast_nodes.values):
                if i != 0:
                    signode += addnodes.desc_sig_punctuation("", ",")
                    signode += addnodes.desc_sig_space()

                self._handle_signature_literal(signode, item_node)

            signode += addnodes.desc_sig_operator("", "]")

        elif isinstance(ast_nodes, gql_ast.ObjectValueNode):
            signode += addnodes.desc_sig_operator("", "{")
            for i, field_node in enumerate(ast_nodes.fields):
                if i != 0:
                    signode += addnodes.desc_sig_punctuation("", ",")
                    signode += addnodes.desc_sig_space()

                signode += addnodes.desc_sig_name("", field_node.name.value)
                signode += addnodes.desc_sig_punctuation("", ":")
                signode += addnodes.desc_sig_space()
                self._handle_signature_literal(signode, field_node.value)

            signode += addnodes.desc_sig_operator("", "}")

        elif isinstance(ast_nodes, (gql_ast.IntValueNode, gql_ast.FloatValueNode)):
            signode += addnodes.desc_sig_literal_number("", ast_nodes.value)
        elif isinstance(ast_nodes, gql_ast.StringValueNode):
            signode += addnodes.desc_sig_operator("", '"')
            signode += addnodes.desc_sig_literal_string("", ast_nodes.value)
            signode += addnodes.desc_sig_operator("", '"')
        elif isinstance(ast_nodes, gql_ast.BooleanValueNode):
            signode += addnodes.desc_sig_keyword("", str(ast_nodes.value).lower())
        elif isinstance(ast_nodes, gql_ast.NullValueNode):
            signode += addnodes.desc_sig_keyword("", "null")
        elif isinstance(ast_nodes, gql_ast.EnumValueNode):
            signode += addnodes.desc_sig_name("", ast_nodes.value)
        # Variable values are a valid literal but not in schemas
        else:
            raise TypeError(f"Unknown literal node type '{type(ast_nodes)}'")

    def _handle_signature_type_reference(
        self,
        signode: desc_signature,
        ast_node: gql_ast.TypeNode,
    ) -> None:
        if isinstance(ast_node, gql_ast.NamedTypeNode):
            type_name = ast_node.name.value
            signode += pending_xref(
                "",
                nodes.Text(type_name),
                refdomain="gql",
                reftype="any",
                reftarget=type_name,
                refspecific=True,
            )
        elif isinstance(ast_node, gql_ast.NonNullTypeNode):
            self._handle_signature_type_reference(signode, ast_node.type)
            signode += addnodes.desc_sig_operator("", "!")
        elif isinstance(ast_node, gql_ast.ListTypeNode):
            signode += addnodes.desc_sig_operator("", "[")
            self._handle_signature_type_reference(signode, ast_node.type)
            signode += addnodes.desc_sig_operator("", "]")
        else:
            raise TypeError(f"Unknown type node '{type(ast_node)}")


class GQLParentObject(GQLObject):
    """A base class for any GraphQL types that can have child entities."""

    def before_content(self) -> None:
        """Set the domain context to be this object."""
        if self.names:
            fullname, _ = self.names[-1]
            # GraphQL entities can only have on level of nesting,
            # so we only need to set and unset the context
            # rather than needing to maintain a stack.
            self.env.ref_context[f"gql:{self.obj_type}"] = fullname

    def after_content(self) -> None:
        """Unset the domain context."""
        self.env.ref_context[f"gql:{self.obj_type}"] = None


class GQLChildObject(GQLObject):
    """A base class for any GraphQL types that only exists as the child of another type.

    This class uses the context set by the parent :class:`GQLParentObject`
    to correctly prefix the name of this entity with the parent
    and tell Sphinx to associate this child with the parent.
    """

    parent_type: str
    """The value of the :attr:`obj_type` attribute on the parent object."""

    def _resolve_names(
        self, name: str, signode: desc_signature
    ) -> Tuple[str, Optional[str]]:
        parent_name = self.env.ref_context.get(f"gql:{self.parent_type}")
        if parent_name:
            fullname = f"{parent_name}.{name}"
        else:
            fullname = name
        signode["fullname"] = fullname
        return (fullname, parent_name)


class GQLField(GQLChildObject):
    """A base class for any field type.

    See Also:
        https://spec.graphql.org/June2018/#FieldDefinition
    """

    def handle_signature(
        self, sig: str, signode: desc_signature
    ) -> Tuple[str, Optional[str]]:
        parser = Parser(sig, no_location=True)
        parser.expect_token(TokenKind.SOF)
        node = parser.parse_field_definition()
        parser.expect_token(TokenKind.EOF)

        name = node.name.value
        signode += addnodes.desc_name(name, name)

        self._handle_signature_input_values(signode, node.arguments)

        signode += addnodes.desc_sig_operator("", ":")
        signode += addnodes.desc_sig_space()

        self._handle_signature_type_reference(signode, node.type)

        self._handle_signature_directives(signode, node.directives)

        return self._resolve_names(name, signode)


class GQLDirective(GQLObject):
    """Represents the definition of a GraphQL Directive.

    See also:
        https://spec.graphql.org/June2018/#sec-Type-System.Directives
    """

    obj_type = "directive"

    def handle_signature(
        self, sig: str, signode: desc_signature
    ) -> Tuple[str, Optional[str]]:
        # https://spec.graphql.org/June2018/#sec-Type-System.Directives
        parser = Parser("directive " + sig, no_location=True)
        parser.expect_token(TokenKind.SOF)
        node = parser.parse_directive_definition()
        parser.expect_token(TokenKind.EOF)

        prefix = [nodes.Text("directive"), addnodes.desc_sig_space()]
        signode += addnodes.desc_annotation(str(prefix), "", *prefix)
        signode += addnodes.desc_sig_space()
        signode += addnodes.desc_sig_operator("", "@")

        name = node.name.value
        signode += addnodes.desc_name(name, name)

        self._handle_signature_input_values(signode, node.arguments)

        signode += addnodes.desc_sig_space()
        signode += addnodes.desc_sig_keyword("", "on")
        signode += addnodes.desc_sig_space()

        for i, location in enumerate(node.locations):
            if i != 0:
                signode += addnodes.desc_sig_space()
                signode += addnodes.desc_sig_operator("", "|")
                signode += addnodes.desc_sig_space()

            signode += nodes.Text(location.value)

        signode["fullname"] = name
        return (name, None)


class GQLEnum(GQLParentObject):
    """Represents the definition of a GraphQL Enum.

    See also:
        https://spec.graphql.org/June2018/#sec-Enums
    """

    obj_type = "enum"

    def handle_signature(
        self, sig: str, signode: desc_signature
    ) -> Tuple[str, Optional[str]]:
        # https://spec.graphql.org/June2018/#sec-Interfaces
        parser = Parser("enum " + sig, no_location=True)
        parser.expect_token(TokenKind.SOF)
        node = parser.parse_enum_type_definition()
        parser.expect_token(TokenKind.EOF)

        prefix = [nodes.Text("enum"), addnodes.desc_sig_space()]
        signode += addnodes.desc_annotation(str(prefix), "", *prefix)

        name = node.name.value
        signode += addnodes.desc_name(name, name)

        self._handle_signature_directives(signode, node.directives)

        signode["fullname"] = name
        return (name, None)


class GQLEnumValue(GQLChildObject):
    """Represents the definition of a value on a GraphQL Enum.

    See also:
        https://spec.graphql.org/June2018/#sec-Enums
    """

    obj_type = "enum:value"
    parent_type = "enum"

    def handle_signature(
        self, sig: str, signode: desc_signature
    ) -> Tuple[str, Optional[str]]:
        # https://spec.graphql.org/June2018/#EnumValueDefinition
        parser = Parser(sig, no_location=True)
        parser.expect_token(TokenKind.SOF)
        node = parser.parse_enum_value_definition()
        parser.expect_token(TokenKind.EOF)

        name = node.name.value
        signode += addnodes.desc_name(name, name)

        self._handle_signature_directives(signode, node.directives)

        return self._resolve_names(name, signode)


class GQLInput(GQLParentObject):
    """Represents the definition of a GraphQL Input Object.

    See also:
        https://spec.graphql.org/June2018/#sec-Input-Objects
    """

    obj_type = "input"

    def handle_signature(
        self, sig: str, signode: desc_signature
    ) -> Tuple[str, Optional[str]]:
        # https://spec.graphql.org/June2018/#sec-Input-Objects
        parser = Parser("input " + sig, no_location=True)
        parser.expect_token(TokenKind.SOF)
        node = parser.parse_input_object_type_definition()
        parser.expect_token(TokenKind.EOF)

        prefix = [nodes.Text("input"), addnodes.desc_sig_space()]
        signode += addnodes.desc_annotation(str(prefix), "", *prefix)

        name = node.name.value
        signode += addnodes.desc_name(name, name)

        self._handle_signature_directives(signode, node.directives)

        signode["fullname"] = name
        return (name, None)


class GQLInputField(GQLChildObject):
    """Represents the definition of a field on a GraphQL Input Object.

    See also:
        https://spec.graphql.org/June2018/#sec-Input-Objects
    """

    obj_type = "input:field"
    parent_type = "input"

    def handle_signature(
        self, sig: str, signode: desc_signature
    ) -> Tuple[str, Optional[str]]:
        parser = Parser(sig, no_location=True)
        parser.expect_token(TokenKind.SOF)
        node = parser.parse_input_value_def()
        parser.expect_token(TokenKind.EOF)

        name = node.name.value
        signode += addnodes.desc_name(name, name)

        signode += addnodes.desc_sig_operator("", ":")
        signode += addnodes.desc_sig_space()

        self._handle_signature_type_reference(signode, node.type)

        self._handle_signature_default_value(signode, node.default_value)

        self._handle_signature_directives(signode, node.directives)

        return self._resolve_names(name, signode)


class GQLInterface(GQLParentObject):
    """Represents the definition of a GraphQL Interface.

    See also:
        https://spec.graphql.org/June2018/#sec-Interfaces
    """

    obj_type = "interface"

    def handle_signature(
        self, sig: str, signode: desc_signature
    ) -> Tuple[str, Optional[str]]:
        # https://spec.graphql.org/June2018/#sec-Interfaces
        parser = Parser("interface " + sig, no_location=True)
        parser.expect_token(TokenKind.SOF)
        node = parser.parse_interface_type_definition()
        parser.expect_token(TokenKind.EOF)

        prefix = [nodes.Text("interface"), addnodes.desc_sig_space()]
        signode += addnodes.desc_annotation(str(prefix), "", *prefix)

        name = node.name.value
        signode += addnodes.desc_name(name, name)

        self._handle_signature_directives(signode, node.directives)

        signode["fullname"] = name
        return (name, None)


class GQLInterfaceField(GQLField):
    """Represents the definition of a field on a GraphQL Interface.

    See also:
        https://spec.graphql.org/June2018/#sec-Interfaces
    """

    obj_type = "interface:field"
    parent_type = "interface"


class GQLScalar(GQLObject):
    """Represents the definition of a GraphQL Scalar.

    See also:
        https://spec.graphql.org/June2018/#sec-Scalars
    """

    obj_type = "scalar"

    def handle_signature(
        self, sig: str, signode: desc_signature
    ) -> Tuple[str, Optional[str]]:
        parser = Parser("scalar " + sig, no_location=True)
        parser.expect_token(TokenKind.SOF)
        node = parser.parse_scalar_type_definition()
        parser.expect_token(TokenKind.EOF)

        prefix = [nodes.Text("scalar"), addnodes.desc_sig_space()]
        signode += addnodes.desc_annotation(str(prefix), "", *prefix)

        name = node.name.value
        signode += addnodes.desc_name(name, name)

        self._handle_signature_directives(signode, node.directives)

        signode["fullname"] = name
        return (name, None)


class GQLType(GQLParentObject):
    """Represents the definition of a GraphQL Type Object.

    See also:
        https://spec.graphql.org/June2018/#sec-Objects
    """

    obj_type = "type"

    def handle_signature(
        self, sig: str, signode: desc_signature
    ) -> Tuple[str, Optional[str]]:
        # https://spec.graphql.org/June2018/#sec-Objects
        parser = Parser("type " + sig, no_location=True)
        parser.expect_token(TokenKind.SOF)
        node = parser.parse_object_type_definition()
        parser.expect_token(TokenKind.EOF)

        prefix = [nodes.Text("type"), addnodes.desc_sig_space()]
        signode += addnodes.desc_annotation(str(prefix), "", *prefix)

        name = node.name.value
        signode += addnodes.desc_name(name, name)

        interfaces = node.interfaces
        if interfaces:
            signode += addnodes.desc_sig_space()
            signode += addnodes.desc_sig_keyword("", "implements")
            signode += addnodes.desc_sig_space()
            for i, interface in enumerate(interfaces):
                if i != 0:
                    signode += addnodes.desc_sig_space()
                    signode += addnodes.desc_sig_operator("", "&")
                    signode += addnodes.desc_sig_space()

                interface_type = interface.name.value
                signode += pending_xref(
                    "",
                    nodes.Text(interface_type),
                    refdomain="gql",
                    reftype="interface",
                    reftarget=interface_type,
                    refspecific=True,
                )

        self._handle_signature_directives(signode, node.directives)

        signode["fullname"] = name
        return (name, None)


class GQLTypeField(GQLField):
    """Represents the definition of a field on a GraphQL Type Object.

    See also:
        https://spec.graphql.org/June2018/#sec-Objects
    """

    obj_type = "type:field"
    parent_type = "type"


class GQLUnion(GQLObject):
    """Represents the definition of a GraphQL Union.

    See also:
        https://spec.graphql.org/June2018/#sec-Unions
    """

    obj_type = "union"

    def handle_signature(
        self, sig: str, signode: desc_signature
    ) -> Tuple[str, Optional[str]]:
        parser = Parser("union " + sig, no_location=True)
        parser.expect_token(TokenKind.SOF)
        node = parser.parse_union_type_definition()
        parser.expect_token(TokenKind.EOF)

        prefix = [nodes.Text("union"), addnodes.desc_sig_space()]
        signode += addnodes.desc_annotation(str(prefix), "", *prefix)

        name = node.name.value
        signode += addnodes.desc_name(name, name)

        self._handle_signature_directives(signode, node.directives)

        member_nodes = node.types
        if member_nodes:
            for i, member_node in enumerate(member_nodes):
                if i == 0:
                    signode += addnodes.desc_sig_space()
                    signode += addnodes.desc_sig_operator("", "=")
                    signode += addnodes.desc_sig_space()
                else:
                    signode += addnodes.desc_sig_space()
                    signode += addnodes.desc_sig_operator("", "|")
                    signode += addnodes.desc_sig_space()

                member_type = member_node.name.value
                signode += pending_xref(
                    "",
                    nodes.Text(member_type),
                    refdomain="gql",
                    reftype="any",
                    reftarget=member_type,
                    refspecific=True,
                )

        signode["fullname"] = name
        return (name, None)


class GraphQLSchemaIndex(Index):
    """The index generator for the GraphQL domain."""

    name = "index"
    localname = "GraphQL Object Index"
    shortname = "index"

    def _anchor(self, fullname: str) -> str:
        return fullname.lower().split("(", 1)[0]

    def generate(
        self, docnames: Optional[Iterable[str]] = None
    ) -> Tuple[List[Tuple[str, List[IndexEntry]]], bool]:
        content: Dict[str, List[IndexEntry]] = {}

        for fullname, _, objtype, docname, node_id, __ in sorted(
            self.domain.get_objects()
        ):
            # Only index top level objects to eliminate name collisions
            if objtype in ("enumvalue", "field"):
                continue

            name = fullname
            subtype = 0  # Always zero because we don't index child types
            anchor = node_id
            extra = ""
            qualifier = ""
            descr = ""
            entry = IndexEntry(name, subtype, docname, anchor, extra, qualifier, descr)

            entries = content.setdefault(fullname[0].lower(), [])
            entries.append(entry)

        sorted_content = sorted(content.items())

        return (sorted_content, True)


class GraphQLDomain(Domain):
    """The definition of the GraphQL Sphinx Domain."""

    name = "gql"
    label = "GraphQL"
    object_types: Dict[str, ObjType] = {
        "directive": ObjType("directive", "directive"),
        "enum": ObjType("enum", "enum"),
        "enum:value": ObjType("enum-value", "enum"),
        "input": ObjType("input", "input"),
        "input:field": ObjType("input-field", "input"),
        "interface": ObjType("interface", "interface"),
        "interface:field": ObjType("interface-field", "interface"),
        "scalar": ObjType("scalar", "scalar"),
        "type": ObjType("type", "type"),
        "type:field": ObjType("type-field", "type"),
        "union": ObjType("union", "union"),
    }

    directives: Dict[str, Type[Directive]] = {
        "directive": GQLDirective,
        "enum": GQLEnum,
        "enum:value": GQLEnumValue,
        "input": GQLInput,
        "input:field": GQLInputField,
        "interface": GQLInterface,
        "interface:field": GQLInterfaceField,
        "scalar": GQLScalar,
        "type": GQLType,
        "type:field": GQLTypeField,
        "union": GQLUnion,
    }

    # mypy complains because many types are allowed other than XRefRole.
    # However this class isn't going to be used for subclassing
    # so violating variance rules is acceptable.
    roles: Dict[str, XRefRole] = {  # type: ignore[assignment]
        "directive": XRefRole(),
        "enum": XRefRole(),
        "enum:value": XRefRole(),
        "input": XRefRole(),
        "input:field": XRefRole(),
        "interface": XRefRole(),
        "interface:field": XRefRole(),
        "scalar": XRefRole(),
        "type": XRefRole(),
        "type:field": XRefRole(),
        "union": XRefRole(),
    }

    initial_data: Dict[str, Dict[str, ObjectEntry]] = {
        "directive": {},
        "enum": {},
        "enum:value": {},
        "input": {},
        "input:field": {},
        "interface": {},
        "interface:field": {},
        "scalar": {},
        "type": {},
        "type:field": {},
        "union": {},
    }

    indices = [GraphQLSchemaIndex]

    def clear_doc(self, docname: str) -> None:
        for object_type in self.object_types:
            type_data = self.data[object_type]
            for fullname, entry in list(type_data.items()):
                if entry.docname == docname:
                    del type_data[fullname]

    def resolve_xref(
        self,
        env: BuildEnvironment,
        fromdocname: str,
        builder: Builder,
        typ: str,
        target: str,
        node: pending_xref,
        contnode: Element,
    ) -> Optional[Element]:
        for object_type in self.object_types:
            type_data = self.data[object_type]
            for fullname, entry in list(type_data.items()):
                if fullname == target:
                    # mypy error caused by incomplete docutils type annotations:
                    # https://github.com/python/typeshed/issues/1269
                    return make_refnode(  # type: ignore[no-any-return]
                        builder,
                        fromdocname,
                        entry.docname,
                        entry.node_id,
                        [contnode],
                        fullname,
                    )

        return None

    def resolve_any_xref(
        self,
        env: BuildEnvironment,
        fromdocname: str,
        builder: Builder,
        target: str,
        node: pending_xref,
        contnode: Element,
    ) -> List[Tuple[str, Element]]:
        """Resolve the pending_xref ``node`` with the given ``target``.

        The reference comes from an "any" or similar role,
        which means that Sphinx doesn't know the type.

        For now we don't resolve "any" xref nodes.
        """
        return []

    def get_objects(self) -> Iterator[Tuple[str, str, str, str, str, int]]:
        for object_type in self.object_types:
            type_data = self.data[object_type]
            for fullname, entry in list(type_data.items()):
                yield (
                    fullname,
                    fullname,
                    object_type,
                    entry.docname,
                    # Names already abide by the rules of anchors
                    # (https://spec.graphql.org/June2018/#Name).
                    entry.node_id,
                    1,
                )

    def merge_domaindata(
        self, docnames: List[str], otherdata: Dict[str, Dict[str, ObjectEntry]]
    ) -> None:
        """Merge the data from multiple workers when working in parallel."""
        for typ, type_data in self.data.items():
            other_type_data = otherdata[typ]
            for fullname, other_entry in other_type_data.items():
                if fullname in type_data and other_entry != type_data[fullname]:
                    entry = type_data[fullname]
                    other_docname = self.env.doc2path(other_entry[0])
                    this_docname = self.env.doc2path(entry[0])
                    logger.warning(
                        f"Duplicate GraphQL {typ} type definition {fullname} in {other_docname}, "
                        f"other instance is in {this_docname}"
                    )
                else:
                    type_data[fullname] = other_entry


def setup(app: Sphinx) -> Dict[str, bool]:
    """Prepare the extension."""
    app.add_domain(GraphQLDomain)

    return {"parallel_read_safe": True, "parallel_write_safe": True}
