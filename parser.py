from __future__ import annotations

# -*- coding: utf-8 -*-
"""
parser.py

Recursive descent parser for MATLAB source code.

Features:
    - Functions
    - Assignments
    - Expressions
    - Function calls
    - Array indexing
    - For loops
    - If statements
    - Matrices
    - Element-wise operators
    - Source tracking for error recovery
"""

from tokens import TokenType

from abstract_syntax_tree import (
    Program,
    Function,
    Assignment,
    ExpressionStatement,
    For,
    If,
    Comment,
    Identifier,
    Number,
    String,
    BinaryOp,
    UnaryOp,
    Call,
    Matrix,
    Index,
    Slice,
    End,
    FieldAccess,
    While,
    Switch,
    Case,
    ElseIf,
    Break,
    Continue,
    PropertyBlock,
    ClassDef
)

FUNCTION_LIKE = {
    "sin", "cos", "tan",
    "sqrt", "exp", "log",
    "floor", "ceil", "round", "abs",
    "zeros", "ones"
}

class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.errors = []

    # ======================================================
    # Token utilities
    # ======================================================

    def current(self):
        return self.tokens[self.position]

    def peek(self, offset=1):
        index = self.position + offset
        if index >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[index]

    def advance(self):
        token = self.current()
        self.position += 1
        return token

    def check(self, token_type):
        return self.current().type == token_type

    def match(self, token_type):
        if self.check(token_type):
            self.advance()
            return True
        return False

    def expect(self, token_type):
        if not self.check(token_type):
            raise SyntaxError(
                f"Expected {token_type}, got {self.current()}"
            )
        return self.advance()

    def skip_newlines(self):
        while self.match(TokenType.NEWLINE):
            pass

    def make_node(self, node, token=None):
        if token is None:
            token = self.current()
        node.line = getattr(
            token,
            "line",
            0
        )
        node.source = getattr(
            token,
            "value",
            ""
        )
        return node

    # ======================================================
    # Program
    # ======================================================

    def parse(self):
        statements = []
        self.skip_newlines()

        while not self.check(TokenType.EOF):
            try:
                statement = self.statement()
                if statement is not None:
                    statements.append(
                        statement
                    )
            except Exception as error:
                self.errors.append(
                    {
                        "line":
                            getattr(
                                self.current(),
                                "line",
                                0
                            ),
                        "error":
                            str(error)
                    }
                )
                self.recover_statement()

            self.skip_newlines()

        return self.make_node(
            Program(
                body=statements
            )
        )

    def recover_statement(self):
        """
        Skip tokens until the next MATLAB statement boundary.
        """
        while not self.check(TokenType.EOF):
            if self.check(TokenType.NEWLINE):
                self.advance()
                break
            if self.check(TokenType.SEMICOLON):
                self.advance()
                break
            self.advance()

    # ======================================================
    # Statements
    # ======================================================

    def statement(self):
        if self.check(TokenType.COMMENT):
            token = self.advance()
            return self.make_node(
                Comment(
                    text=token.value
                ),
                token
            )

        if self.check(TokenType.SEMICOLON):
            self.advance()
            return None

        if self.check(TokenType.FUNCTION):
            return self.function()

        if self.check(TokenType.FOR):
            return self.for_loop()

        if self.check(TokenType.IF):
            return self.if_statement()
        
        if self.check(TokenType.TRY):
            return self.try_statement()
        
        if self.check(TokenType.WHILE):
            return self.while_loop()
        
        if self.check(TokenType.SWITCH):
            return self.switch_statement()
        
        if self.check(TokenType.BREAK):
            token = self.advance()
            return self.make_node(Break(), token)

        if self.check(TokenType.CONTINUE):
            token = self.advance()
            return self.make_node(Continue(), token)
        
        if self.check(TokenType.CLASSDEF):
            return self.classdef()

        return self.assignment_or_expression()

    # ======================================================
    # Function
    # ======================================================

    def function(self):
        token = self.expect(
            TokenType.FUNCTION
        )
        outputs = []
        function_name = None

        if self.check(TokenType.IDENTIFIER):
            first = self.advance().value

            if self.match(TokenType.ASSIGN):
                outputs.append(first)
            else:
                function_name = first

        elif self.match(TokenType.LBRACKET):
            while not self.check(TokenType.RBRACKET):
                outputs.append(
                    self.expect(
                        TokenType.IDENTIFIER
                    ).value
                )
                self.match(
                    TokenType.COMMA
                )

            self.expect(
                TokenType.RBRACKET
            )
            self.expect(
                TokenType.ASSIGN
            )
        else:
            raise SyntaxError(
                "Invalid MATLAB function declaration"
            )

        if function_name is None:
            function_name = self.expect(
                TokenType.IDENTIFIER
            ).value

        inputs = []

        self.expect(
            TokenType.LPAREN
        )

        while not self.check(TokenType.RPAREN):
            inputs.append(
                self.expect(
                    TokenType.IDENTIFIER
                ).value
            )
            if not self.match(TokenType.COMMA):
                break

        self.expect(
            TokenType.RPAREN
        )

        body = self.block()

        return self.make_node(
            Function(
                name=function_name,
                inputs=inputs,
                outputs=outputs,
                body=body
            ),
            token
        )
    
    def classdef(self):
        token = self.expect(TokenType.CLASSDEF)
        name = self.expect(TokenType.IDENTIFIER).value
    
        properties = []
        methods = []
    
        self.skip_newlines()
    
        while not self.check(TokenType.END) and not self.check(TokenType.EOF):
    
            # PROPERTIES block
            if self.check(TokenType.PROPERTIES):
                self.advance()  # consume 'properties'
                prop_body = self.block()  # up to 'end' of properties
                properties.append(
                    self.make_node(
                        PropertyBlock(body=prop_body),
                        token
                    )
                )
                self.skip_newlines()
                continue
    
            # METHODS block
            if self.check(TokenType.METHODS):
                self.advance()  # consume 'methods'
                method_body = self.block()  # up to 'end' of methods
    
                # Keep only Function nodes as methods
                for stmt in method_body:
                    if isinstance(stmt, Function):
                        methods.append(stmt)
    
                self.skip_newlines()
                continue
    
            # Anything else inside classdef: skip/recover
            self.recover_statement()
            self.skip_newlines()
    
        # Consume final 'end' for classdef
        if self.check(TokenType.END):
            self.advance()
    
        return self.make_node(
            ClassDef(
                name=name,
                properties=properties,
                methods=methods
            ),
            token
        )

    # ======================================================
    # Blocks
    # ======================================================

    def block(self):
        body = []
        self.skip_newlines()

        while not (
            self.check(TokenType.END)
            or self.check(TokenType.EOF)
        ):
            statement = self.statement()

            if statement is not None:
                body.append(
                    statement
                )

            self.skip_newlines()

        if self.check(TokenType.END):
            self.advance()

        return body

    # ======================================================
    # For Loop
    # ======================================================

    def for_loop(self):
        token = self.expect(
            TokenType.FOR
        )

        variable = self.expect(
            TokenType.IDENTIFIER
        ).value

        self.expect(
            TokenType.ASSIGN
        )

        start = self.expression()

        self.expect(
            TokenType.COLON
        )

        stop = self.expression()

        body = self.block()

        return self.make_node(
            For(
                variable=variable,
                start=start,
                stop=stop,
                body=body
            ),
            token
        )
    

    def while_loop(self):
        token = self.expect(TokenType.WHILE)
    
        # Parse the condition expression on the while line
        condition = self.expression()
    
        # Parse the loop body until 'end'
        body = self.block()
    
        return self.make_node(
            While(
                condition=condition,
                body=body
            ),
            token
        )

    # ======================================================
    # If
    # ======================================================


    def if_statement(self):
        # Consume 'if'
        token = self.expect(TokenType.IF)
    
        # Parse condition after 'if'
        condition = self.expression()
        self.skip_newlines()
    
        # ---- IF body ----
        body = []
        while (
            not self.check(TokenType.ELSEIF)
            and not self.check(TokenType.ELSE)
            and not self.check(TokenType.END)
            and not self.check(TokenType.EOF)
        ):
            stmt = self.statement()
            if stmt is not None:
                body.append(stmt)
            self.skip_newlines()
    
        # ---- ELSEIF blocks ----
        elseif_blocks = []
        while self.check(TokenType.ELSEIF):
            self.advance()  # consume 'elseif'
            elseif_cond = self.expression()
            self.skip_newlines()
    
            elseif_body = []
            while (
                not self.check(TokenType.ELSEIF)
                and not self.check(TokenType.ELSE)
                and not self.check(TokenType.END)
                and not self.check(TokenType.EOF)
            ):
                stmt = self.statement()
                if stmt is not None:
                    elseif_body.append(stmt)
                self.skip_newlines()
    
            elseif_blocks.append(
                self.make_node(
                    ElseIf(
                        condition=elseif_cond,
                        body=elseif_body
                    ),
                    token
                )
            )
    
        # ---- ELSE body (optional) ----
        else_body = []
        if self.check(TokenType.ELSE):
            self.advance()  # consume 'else'
            self.skip_newlines()
    
            while (
                not self.check(TokenType.END)
                and not self.check(TokenType.EOF)
            ):
                stmt = self.statement()
                if stmt is not None:
                    else_body.append(stmt)
                self.skip_newlines()
    
        # Consume final 'end'
        if self.check(TokenType.END):
            self.advance()
    
        return self.make_node(
            If(
                condition=condition,
                body=body,
                elseif_blocks=elseif_blocks,
                else_body=else_body
            ),
            token
        )
    # ======================================================
    # Try
    # ======================================================

    def try_statement(self):
        # Consume 'try'
        token = self.expect(TokenType.TRY)
    
        # ---- TRY BODY ----
        try_body = []
        self.skip_newlines()
    
        # Collect statements until 'catch' or 'end'
        while (
            not self.check(TokenType.CATCH)
            and not self.check(TokenType.END)
            and not self.check(TokenType.EOF)
        ):
            stmt = self.statement()
            if stmt is not None:
                try_body.append(stmt)
            self.skip_newlines()
    
        # ---- CATCH BODY (optional) ----
        catch_body = []
        catch_var = ""
    
        if self.check(TokenType.CATCH):
            self.advance()  # consume 'catch'
    
            # Optional catch variable: catch ME
            if self.check(TokenType.IDENTIFIER):
                catch_var = self.advance().value
    
            self.skip_newlines()
    
            # Collect statements until 'end'
            while (
                not self.check(TokenType.END)
                and not self.check(TokenType.EOF)
            ):
                stmt = self.statement()
                if stmt is not None:
                    catch_body.append(stmt)
                self.skip_newlines()
    
        # Consume the final 'end' if present
        if self.check(TokenType.END):
            self.advance()
    
        from abstract_syntax_tree import Try  # if not already imported at top
    
        return self.make_node(
            Try(
                body=try_body,
                catch_body=catch_body,
                catch_var=catch_var,
            ),
            token,
        )
    
    def switch_statement(self):
        # 'switch' keyword
        token = self.expect(TokenType.SWITCH)
    
        # Expression after 'switch'
        expr = self.expression()
    
        cases = []
        default_body = []
    
        self.skip_newlines()
    
        # Parse case/otherwise blocks until 'end' or EOF
        while (
            not self.check(TokenType.END)
            and not self.check(TokenType.EOF)
        ):
            # CASE branch
            if self.check(TokenType.CASE):
                self.advance()  # consume 'case'
                value = self.expression()
                body = []
    
                self.skip_newlines()
    
                # Collect statements until next CASE / OTHERWISE / END / EOF
                while (
                    not self.check(TokenType.CASE)
                    and not self.check(TokenType.OTHERWISE)
                    and not self.check(TokenType.END)
                    and not self.check(TokenType.EOF)
                ):
                    stmt = self.statement()
                    if stmt is not None:
                        body.append(stmt)
                    self.skip_newlines()
    
                cases.append(
                    self.make_node(
                        Case(
                            value=value,
                            body=body
                        ),
                        token
                    )
                )
                continue
    
            # OTHERWISE branch
            if self.check(TokenType.OTHERWISE):
                self.advance()  # consume 'otherwise'
                default_body = []
    
                self.skip_newlines()
    
                while (
                    not self.check(TokenType.END)
                    and not self.check(TokenType.EOF)
                ):
                    stmt = self.statement()
                    if stmt is not None:
                        default_body.append(stmt)
                    self.skip_newlines()
    
                # Only one 'otherwise' expected; break out
                break
    
            # Fallback: let statement() handle unexpected tokens
            stmt = self.statement()
            if stmt is not None:
                default_body.append(stmt)
            self.skip_newlines()
    
        # Consume final 'end' if present
        if self.check(TokenType.END):
            self.advance()
    
        return self.make_node(
            Switch(
                expression=expr,
                cases=cases,
                default_body=default_body
            ),
            token
        )

    # ======================================================
    # Assignment
    # ======================================================

    def assignment_or_expression(self):
        expression = self.expression()

        if self.match(TokenType.ASSIGN):
            value = self.expression()

            return self.make_node(
                Assignment(
                    target=expression,
                    value=value
                )
            )

        return self.make_node(
            ExpressionStatement(
                expression=expression
            )
        )

    # ======================================================
    # Expressions
    # ======================================================

    def expression(self):
        return self.binary_expression(0)

    PRECEDENCE = {
        TokenType.OR: 1,
        TokenType.AND: 2,
        TokenType.EQUAL: 3,
        TokenType.NOT_EQUAL: 3,
        TokenType.LESS: 4,
        TokenType.LESS_EQUAL: 4,
        TokenType.GREATER: 4,
        TokenType.GREATER_EQUAL: 4,
        TokenType.PLUS: 5,
        TokenType.MINUS: 5,
        TokenType.TIMES: 6,
        TokenType.DIVIDE: 6,
        TokenType.ELEMENT_TIMES: 6,
        TokenType.ELEMENT_DIVIDE: 6,
        TokenType.POWER: 7,
        TokenType.ELEMENT_POWER: 7,
    }

    def binary_expression(self, minimum):
        left = self.unary()

        while True:
            operator_type = self.current().type

            if operator_type not in self.PRECEDENCE:
                break

            precedence = self.PRECEDENCE[
                operator_type
            ]

            if precedence < minimum:
                break

            token = self.advance()

            right = self.binary_expression(
                precedence + 1
            )

            left = self.make_node(
                BinaryOp(
                    operator=token.value,
                    left=left,
                    right=right
                ),
                token
            )

        return left

    def unary(self):

        if self.check(TokenType.MINUS):
    
            token = self.advance()
    
            return self.make_node(
                UnaryOp(
                    operator="-",
                    operand=self.unary()
                ),
                token
            )
    
    
        if self.check(TokenType.PLUS):
    
            token = self.advance()
    
            return self.make_node(
                UnaryOp(
                    operator="+",
                    operand=self.unary()
                ),
                token
            )
    
    
        return self.postfix()

    # ======================================================
    # Postfix (indexing)
    # ======================================================

    def postfix(self):
        """
        Handle postfix operations: field access, indexing, and function calls.
        MATLAB uses () for both calls and indexing.
        """
        node = self.primary()
    
        while True:
            # ---------------------------------
            # Field access: obj.field
            # ---------------------------------
            if self.check(TokenType.DOT):
                self.advance()  # consume '.'
                field = self.expect(TokenType.IDENTIFIER).value
                node = self.make_node(
                    FieldAccess(
                        value=node,
                        field=field
                    )
                )
                continue
    
            # ---------------------------------
            # Parentheses: call or indexing
            # ---------------------------------
            if self.check(TokenType.LPAREN):
                self.advance()
    
                # Parse contents once
                arguments = self.parse_indices()
                self.expect(TokenType.RPAREN)
    
                # Function / method call: foo(x), sqrt(a-1), obj.foo(x)
                if isinstance(node, Identifier) or isinstance(node, FieldAccess):
                    node = self.make_node(
                        Call(
                            function=node,
                            arguments=arguments
                        )
                    )
                    continue
    
                # Otherwise, treat as array indexing: A(i,j)
                node = self.make_node(
                    Index(
                        value=node,
                        indices=arguments
                    )
                )
                continue
    
            break
    
        return node

    def parse_indices(self):
        """
        Parse MATLAB indexing expressions: A(1,2), A(:,end), A(1:5), etc.
        """
        indices = []

        while not self.check(TokenType.RPAREN):
            # Colon (slice)
            if self.check(TokenType.COLON):
                self.advance()
                # Start is empty
                stop = None
                step = None
                
                # Check for stop
                if not self.check(TokenType.COMMA) and not self.check(TokenType.RPAREN):
                    stop = self.expression()
                
                # Check for step
                if self.check(TokenType.COLON):
                    self.advance()
                    if not self.check(TokenType.COMMA) and not self.check(TokenType.RPAREN):
                        step = self.expression()
                
                indices.append(
                    Slice(start=None, stop=stop, step=step)
                )
            else:
                # Try to parse an expression
                expr = self.expression()
                
                # Check if it's a slice (start:stop:step)
                if self.check(TokenType.COLON):
                    self.advance()
                    stop = None
                    step = None
                    
                    if not self.check(TokenType.COMMA) and not self.check(TokenType.RPAREN):
                        stop = self.expression()
                    
                    if self.check(TokenType.COLON):
                        self.advance()
                        if not self.check(TokenType.COMMA) and not self.check(TokenType.RPAREN):
                            step = self.expression()
                    
                    indices.append(
                        Slice(start=expr, stop=stop, step=step)
                    )
                else:
                    # Regular index
                    indices.append(expr)
            
            if not self.match(TokenType.COMMA):
                break

        return indices

    # ======================================================
    # Primary Expressions
    # ======================================================

    def matrix_element(self):
        return self.binary_expression(8)
    
    def primary(self):
        token = self.advance()

        # -------------------------------
        # Matrix
        # -------------------------------

        if token.type == TokenType.LBRACKET:
            rows = []
            row = []

            while not self.check(TokenType.RBRACKET):
                if self.check(TokenType.NEWLINE):
                    self.advance()
                    continue

                if self.check(TokenType.SEMICOLON):
                    self.advance()

                    if row:
                        rows.append(row)
                        row = []

                    continue

                row.append(self.matrix_element())

                self.match(
                    TokenType.COMMA
                )

            self.expect(
                TokenType.RBRACKET
            )

            if row:
                rows.append(row)

            return self.make_node(
                Matrix(
                    rows=rows
                ),
                token
            )

        # -------------------------------
        # Number
        # -------------------------------

        if token.type == TokenType.NUMBER:
            return self.make_node(
                Number(
                    value=float(token.value)
                ),
                token
            )

        # -------------------------------
        # Identifier
        # -------------------------------

        if token.type == TokenType.IDENTIFIER:
            node = self.make_node(
                Identifier(
                    name=token.value
                ),
                token
            )

            # Check for function call
            if self.check(TokenType.LPAREN):
                # Peek ahead to distinguish function call from indexing
                # If we see an identifier followed by (, it could be:
                # 1. func(args) - function call
                # 2. A(i) - array index
                # The postfix() method will handle this after primary()
                pass

            return node

        # -------------------------------
        # Parentheses
        # -------------------------------

        if token.type == TokenType.LPAREN:
            expression = self.expression()
            self.expect(
                TokenType.RPAREN
            )
            return expression
        
        # ------------------------------
        # String
        # ------------------------------
        if token.type == TokenType.STRING:
            return self.make_node(
                String(value=token.value),
                token
            )

        raise SyntaxError(
            f"Unexpected token {token}"
        )
