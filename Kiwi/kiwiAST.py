from __future__ import annotations

# Default libraries
# -----------------

from typing import Any, Optional
from itertools import chain

# Custom libraries
# ----------------

from pegen.parser import memoize, memoize_left_rec, Parser
from pegen.tokenizer import Tokenizer
import Kiwi.components.kiwiASO as kiwi


class AST:
    """
    The main task of this class is
    - convert tokens to AST
    """

    parser: KiwiParser
    module: kiwi.Module

    def __init__(self, tokenizer: Tokenizer):
        self.parser = KiwiParser(tokenizer)
        self.module = self.parser.start()


#
# Keywords and soft keywords are listed at the end of the parser definition.
class KiwiParser(Parser):

    @memoize
    def start(self) -> Optional[kiwi . Module]:
        # start: import_stmts statements $ | import_stmts $ | statements $ | $
        mark = self._mark()
        if (
            (i := self.import_stmts())
            and
            (v := self.statements())
            and
            (_endmarker := self.expect('ENDMARKER'))
        ):
            return kiwi . Module ( i , v )
        self._reset(mark)
        if (
            (i := self.import_stmts())
            and
            (_endmarker := self.expect('ENDMARKER'))
        ):
            return kiwi . Module ( i , [] )
        self._reset(mark)
        if (
            (v := self.statements())
            and
            (_endmarker := self.expect('ENDMARKER'))
        ):
            return kiwi . Module ( [] , v )
        self._reset(mark)
        if (
            (_endmarker := self.expect('ENDMARKER'))
        ):
            return kiwi . Module ( [] , [] )
        self._reset(mark)
        return None

    @memoize
    def import_stmts(self) -> Optional[Any]:
        # import_stmts: ((import_stmt | from_import_stmt))+
        mark = self._mark()
        if (
            (v := self._loop1_1())
        ):
            return list ( chain . from_iterable ( v ) )
        self._reset(mark)
        return None

    @memoize
    def import_stmt(self) -> Optional[Any]:
        # import_stmt: "import" dotted_as_names ((NEWLINE | ';'))+
        mark = self._mark()
        if (
            (literal := self.expect("import"))
            and
            (v := self.dotted_as_names())
            and
            (_loop1_2 := self._loop1_2())
        ):
            return v
        self._reset(mark)
        return None

    @memoize
    def from_import_stmt(self) -> Optional[Any]:
        # from_import_stmt: "from" dotted_name import_stmt
        mark = self._mark()
        if (
            (literal := self.expect("from"))
            and
            (v := self.dotted_name())
            and
            (a := self.import_stmt())
        ):
            return [kiwi . Alias ( '' . join ( v ) , a )]
        self._reset(mark)
        return None

    @memoize
    def dotted_as_names(self) -> Optional[Any]:
        # dotted_as_names: ','.dotted_as_name+
        mark = self._mark()
        if (
            (_gather_3 := self._gather_3())
        ):
            return _gather_3
        self._reset(mark)
        return None

    @memoize
    def dotted_as_name(self) -> Optional[Any]:
        # dotted_as_name: dotted_name "as" NAME_ | dotted_name
        mark = self._mark()
        if (
            (v := self.dotted_name())
            and
            (literal := self.expect("as"))
            and
            (a := self.NAME_())
        ):
            return kiwi . Alias ( '' . join ( v ) , a )
        self._reset(mark)
        if (
            (v := self.dotted_name())
        ):
            return kiwi . Alias ( '' . join ( v ) , v [- 1] )
        self._reset(mark)
        return None

    @memoize_left_rec
    def dotted_name(self) -> Optional[Any]:
        # dotted_name: dotted_name '.' NAME_ | NAME_
        mark = self._mark()
        if (
            (v := self.dotted_name())
            and
            (literal := self.expect('.'))
            and
            (a := self.NAME_())
        ):
            return [* v , a]
        self._reset(mark)
        if (
            (v := self.NAME_())
        ):
            return [v]
        self._reset(mark)
        return None

    @memoize
    def statements(self) -> Optional[Any]:
        # statements: statement+
        mark = self._mark()
        if (
            (_loop1_5 := self._loop1_5())
        ):
            return _loop1_5
        self._reset(mark)
        return None

    @memoize
    def statement(self) -> Optional[Any]:
        # statement: simple_stmt ((NEWLINE | ';'))+ | compound_stmt
        mark = self._mark()
        if (
            (v := self.simple_stmt())
            and
            (_loop1_6 := self._loop1_6())
        ):
            return v
        self._reset(mark)
        if (
            (v := self.compound_stmt())
        ):
            return v
        self._reset(mark)
        return None

    @memoize
    def statement_newline(self) -> Optional[Any]:
        # statement_newline: simple_stmt (NEWLINE)+
        mark = self._mark()
        if (
            (v := self.simple_stmt())
            and
            (_loop1_7 := self._loop1_7())
        ):
            return v
        self._reset(mark)
        return None

    @memoize
    def simple_stmt(self) -> Optional[Any]:
        # simple_stmt: assignment | expression | return_stmt | 'pass' | 'break' | 'continue'
        mark = self._mark()
        if (
            (assignment := self.assignment())
        ):
            return assignment
        self._reset(mark)
        if (
            (expression := self.expression())
        ):
            return expression
        self._reset(mark)
        if (
            (return_stmt := self.return_stmt())
        ):
            return return_stmt
        self._reset(mark)
        if (
            (literal := self.expect('pass'))
        ):
            return kiwi . Pass ( )
        self._reset(mark)
        if (
            (literal := self.expect('break'))
        ):
            return kiwi . Break ( )
        self._reset(mark)
        if (
            (literal := self.expect('continue'))
        ):
            return kiwi . Continue ( )
        self._reset(mark)
        return None

    @memoize
    def compound_stmt(self) -> Optional[Any]:
        # compound_stmt: function_def | namespace_def | if_stmt | while_stmt | match_stmt
        mark = self._mark()
        if (
            (function_def := self.function_def())
        ):
            return function_def
        self._reset(mark)
        if (
            (namespace_def := self.namespace_def())
        ):
            return namespace_def
        self._reset(mark)
        if (
            (if_stmt := self.if_stmt())
        ):
            return if_stmt
        self._reset(mark)
        if (
            (while_stmt := self.while_stmt())
        ):
            return while_stmt
        self._reset(mark)
        if (
            (match_stmt := self.match_stmt())
        ):
            return match_stmt
        self._reset(mark)
        return None

    @memoize
    def assignment(self) -> Optional[Any]:
        # assignment: annotations '=' ','.expression+ | ','.expression+ '=' ','.expression+ | ','.expression+ augassign ','.expression+ | annotations
        mark = self._mark()
        if (
            (a := self.annotations())
            and
            (literal := self.expect('='))
            and
            (v := self._gather_8())
        ):
            return kiwi . AnnAssignment ( * a , v )
        self._reset(mark)
        if (
            (i := self._gather_10())
            and
            (literal := self.expect('='))
            and
            (v := self._gather_12())
        ):
            return kiwi . Assignment ( i , v )
        self._reset(mark)
        if (
            (i := self._gather_14())
            and
            (o := self.augassign())
            and
            (v := self._gather_16())
        ):
            return kiwi . AugAssignment ( i , o , v )
        self._reset(mark)
        if (
            (a := self.annotations())
        ):
            return kiwi . Annotation ( * a )
        self._reset(mark)
        return None

    @memoize
    def annotations(self) -> Optional[Any]:
        # annotations: expression ':' expression expression* | ','.expression+ '->' expression expression*
        mark = self._mark()
        if (
            (i := self.expression())
            and
            (literal := self.expect(':'))
            and
            (t := self.expression())
            and
            (a := self._loop0_18(),)
        ):
            return [i] , t , a
        self._reset(mark)
        if (
            (i := self._gather_19())
            and
            (literal := self.expect('->'))
            and
            (t := self.expression())
            and
            (a := self._loop0_21(),)
        ):
            return i , t , a
        self._reset(mark)
        return None

    @memoize
    def augassign(self) -> Optional[Any]:
        # augassign: '+=' | '-=' | '*=' | '/=' | '%='
        mark = self._mark()
        if (
            (literal := self.expect('+='))
        ):
            return kiwi . Token ( '+=' )
        self._reset(mark)
        if (
            (literal := self.expect('-='))
        ):
            return kiwi . Token ( '-=' )
        self._reset(mark)
        if (
            (literal := self.expect('*='))
        ):
            return kiwi . Token ( '*=' )
        self._reset(mark)
        if (
            (literal := self.expect('/='))
        ):
            return kiwi . Token ( '/=' )
        self._reset(mark)
        if (
            (literal := self.expect('%='))
        ):
            return kiwi . Token ( '%=' )
        self._reset(mark)
        return None

    @memoize
    def return_stmt(self) -> Optional[Any]:
        # return_stmt: 'return' expression
        mark = self._mark()
        if (
            (literal := self.expect('return'))
            and
            (v := self.expression())
        ):
            return kiwi . Return ( v )
        self._reset(mark)
        return None

    @memoize
    def block(self) -> Optional[Any]:
        # block: NEWLINE INDENT statements DEDENT NEWLINE | statement_newline
        mark = self._mark()
        if (
            (_newline := self.expect('NEWLINE'))
            and
            (_indent := self.expect('INDENT'))
            and
            (v := self.statements())
            and
            (_dedent := self.expect('DEDENT'))
            and
            (_newline_1 := self.expect('NEWLINE'))
        ):
            return v
        self._reset(mark)
        if (
            (v := self.statement_newline())
        ):
            return [v]
        self._reset(mark)
        return None

    @memoize
    def hiding_block(self) -> Optional[Any]:
        # hiding_block: NEWLINE INDENT blocks DEDENT NEWLINE
        mark = self._mark()
        if (
            (_newline := self.expect('NEWLINE'))
            and
            (_indent := self.expect('INDENT'))
            and
            (v := self.blocks())
            and
            (_dedent := self.expect('DEDENT'))
            and
            (_newline_1 := self.expect('NEWLINE'))
        ):
            return v
        self._reset(mark)
        return None

    @memoize
    def blocks(self) -> Optional[Any]:
        # blocks: private_block public_block | public_block private_block | private_block | public_block | statements
        mark = self._mark()
        if (
            (pr := self.private_block())
            and
            (pu := self.public_block())
        ):
            return pr [0] , pu [0] , [* pr [1] , * pu [1]]
        self._reset(mark)
        if (
            (pu := self.public_block())
            and
            (pr := self.private_block())
        ):
            return pr [0] , pu [0] , [* pr [1] , * pu [1]]
        self._reset(mark)
        if (
            (pr := self.private_block())
        ):
            return pr [0] , [] , pr [1]
        self._reset(mark)
        if (
            (pu := self.public_block())
        ):
            return [] , pu [0] , pu [1]
        self._reset(mark)
        if (
            (d := self.statements())
        ):
            return [] , [] , d
        self._reset(mark)
        return None

    @memoize
    def private_block(self) -> Optional[Any]:
        # private_block: statements 'private' ':' block statements | statements 'private' ':' block | 'private' ':' block statements | 'private' ':' block
        mark = self._mark()
        if (
            (d1 := self.statements())
            and
            (literal := self.expect('private'))
            and
            (literal_1 := self.expect(':'))
            and
            (p := self.block())
            and
            (d2 := self.statements())
        ):
            return p , [* d1 , * d2]
        self._reset(mark)
        if (
            (d := self.statements())
            and
            (literal := self.expect('private'))
            and
            (literal_1 := self.expect(':'))
            and
            (p := self.block())
        ):
            return p , d
        self._reset(mark)
        if (
            (literal := self.expect('private'))
            and
            (literal_1 := self.expect(':'))
            and
            (p := self.block())
            and
            (d := self.statements())
        ):
            return p , d
        self._reset(mark)
        if (
            (literal := self.expect('private'))
            and
            (literal_1 := self.expect(':'))
            and
            (p := self.block())
        ):
            return p , []
        self._reset(mark)
        return None

    @memoize
    def public_block(self) -> Optional[Any]:
        # public_block: statements 'public' ':' block statements | statements 'public' ':' block | 'public' ':' block statements | 'public' ':' block
        mark = self._mark()
        if (
            (d1 := self.statements())
            and
            (literal := self.expect('public'))
            and
            (literal_1 := self.expect(':'))
            and
            (p := self.block())
            and
            (d2 := self.statements())
        ):
            return p , [* d1 , * d2]
        self._reset(mark)
        if (
            (d := self.statements())
            and
            (literal := self.expect('public'))
            and
            (literal_1 := self.expect(':'))
            and
            (p := self.block())
        ):
            return p , d
        self._reset(mark)
        if (
            (literal := self.expect('public'))
            and
            (literal_1 := self.expect(':'))
            and
            (p := self.block())
            and
            (d := self.statements())
        ):
            return p , d
        self._reset(mark)
        if (
            (literal := self.expect('public'))
            and
            (literal_1 := self.expect(':'))
            and
            (p := self.block())
        ):
            return p , []
        self._reset(mark)
        return None

    @memoize
    def namespace_def(self) -> Optional[Any]:
        # namespace_def: 'namespace' NAME_ ':' hiding_block
        mark = self._mark()
        if (
            (literal := self.expect('namespace'))
            and
            (i := self.NAME_())
            and
            (literal_1 := self.expect(':'))
            and
            (b := self.hiding_block())
        ):
            return kiwi . NamespaceDef ( i , * b )
        self._reset(mark)
        return None

    @memoize
    def function_def(self) -> Optional[Any]:
        # function_def: 'function' NAME_ '(' parameters ')' '->' return_param '<' '-' expression ':' block | 'function' NAME_ '(' parameters ')' '<' '-' expression ':' block | 'function' NAME_ '(' parameters ')' '->' return_param ':' block | 'function' NAME_ '(' parameters ')' ':' block
        mark = self._mark()
        if (
            (literal := self.expect('function'))
            and
            (i := self.NAME_())
            and
            (literal_1 := self.expect('('))
            and
            (p := self.parameters())
            and
            (literal_2 := self.expect(')'))
            and
            (literal_3 := self.expect('->'))
            and
            (r := self.return_param())
            and
            (literal_4 := self.expect('<'))
            and
            (literal_5 := self.expect('-'))
            and
            (pr := self.expression())
            and
            (literal_6 := self.expect(':'))
            and
            (b := self.block())
        ):
            return kiwi . FuncDef ( i , p [0] , p [1] , r , pr , b )
        self._reset(mark)
        if (
            (literal := self.expect('function'))
            and
            (i := self.NAME_())
            and
            (literal_1 := self.expect('('))
            and
            (p := self.parameters())
            and
            (literal_2 := self.expect(')'))
            and
            (literal_3 := self.expect('<'))
            and
            (literal_4 := self.expect('-'))
            and
            (pr := self.expression())
            and
            (literal_5 := self.expect(':'))
            and
            (b := self.block())
        ):
            return kiwi . FuncDef ( i , p [0] , p [1] , None , pr , b )
        self._reset(mark)
        if (
            (literal := self.expect('function'))
            and
            (i := self.NAME_())
            and
            (literal_1 := self.expect('('))
            and
            (p := self.parameters())
            and
            (literal_2 := self.expect(')'))
            and
            (literal_3 := self.expect('->'))
            and
            (r := self.return_param())
            and
            (literal_4 := self.expect(':'))
            and
            (b := self.block())
        ):
            return kiwi . FuncDef ( i , p [0] , p [1] , r , None , b )
        self._reset(mark)
        if (
            (literal := self.expect('function'))
            and
            (i := self.NAME_())
            and
            (literal_1 := self.expect('('))
            and
            (p := self.parameters())
            and
            (literal_2 := self.expect(')'))
            and
            (literal_3 := self.expect(':'))
            and
            (b := self.block())
        ):
            return kiwi . FuncDef ( i , p [0] , p [1] , None , None , b )
        self._reset(mark)
        return None

    @memoize
    def parameters(self) -> Optional[Any]:
        # parameters: param_no_default* param_with_default*
        # nullable=True
        mark = self._mark()
        if (
            (p := self._loop0_22(),)
            and
            (d := self._loop0_23(),)
        ):
            return [* p , * map ( lambda x : x [0] , d )] , list ( map ( lambda x : x [1] , d ) )
        self._reset(mark)
        return None

    @memoize
    def param_no_default(self) -> Optional[Any]:
        # param_no_default: annotations ',' | annotations &')' | '=' NAME_ ',' | '=' NAME_ &')'
        mark = self._mark()
        if (
            (v := self.annotations())
            and
            (literal := self.expect(','))
        ):
            return kiwi . Parameter ( v [0] , v [1] )
        self._reset(mark)
        if (
            (v := self.annotations())
            and
            self.positive_lookahead(self.expect, ')')
        ):
            return kiwi . Parameter ( v [0] , v [1] )
        self._reset(mark)
        if (
            (literal := self.expect('='))
            and
            (i := self.NAME_())
            and
            (literal_1 := self.expect(','))
        ):
            return kiwi . RefParameter ( i )
        self._reset(mark)
        if (
            (literal := self.expect('='))
            and
            (i := self.NAME_())
            and
            self.positive_lookahead(self.expect, ')')
        ):
            return kiwi . RefParameter ( i )
        self._reset(mark)
        return None

    @memoize
    def param_with_default(self) -> Optional[Any]:
        # param_with_default: annotations '=' expression ',' | annotations '=' expression &')' | '=' NAME_ '=' expression ',' | '=' NAME_ '=' expression &')'
        mark = self._mark()
        if (
            (a := self.annotations())
            and
            (literal := self.expect('='))
            and
            (v := self.expression())
            and
            (literal_1 := self.expect(','))
        ):
            return kiwi . Parameter ( a [0] , a [1] ) , v
        self._reset(mark)
        if (
            (a := self.annotations())
            and
            (literal := self.expect('='))
            and
            (v := self.expression())
            and
            self.positive_lookahead(self.expect, ')')
        ):
            return kiwi . Parameter ( a [0] , a [1] ) , v
        self._reset(mark)
        if (
            (literal := self.expect('='))
            and
            (i := self.NAME_())
            and
            (literal_1 := self.expect('='))
            and
            (v := self.expression())
            and
            (literal_2 := self.expect(','))
        ):
            return kiwi . RefParameter ( i ) , v
        self._reset(mark)
        if (
            (literal := self.expect('='))
            and
            (i := self.NAME_())
            and
            (literal_1 := self.expect('='))
            and
            (v := self.expression())
            and
            self.positive_lookahead(self.expect, ')')
        ):
            return kiwi . RefParameter ( i ) , v
        self._reset(mark)
        return None

    @memoize
    def return_param(self) -> Optional[Any]:
        # return_param: expression | '=' NAME_
        mark = self._mark()
        if (
            (expression := self.expression())
        ):
            return expression
        self._reset(mark)
        if (
            (literal := self.expect('='))
            and
            (i := self.NAME_())
        ):
            return kiwi . RefParameter ( i )
        self._reset(mark)
        return None

    @memoize
    def if_stmt(self) -> Optional[Any]:
        # if_stmt: 'if' expression ':' block 'else' if_stmt | 'if' expression ':' block 'else' ':' block | 'if' expression ':' block
        mark = self._mark()
        if (
            (literal := self.expect('if'))
            and
            (c := self.expression())
            and
            (literal_1 := self.expect(':'))
            and
            (t := self.block())
            and
            (literal_2 := self.expect('else'))
            and
            (e := self.if_stmt())
        ):
            return kiwi . IfElse ( c , t , e )
        self._reset(mark)
        if (
            (literal := self.expect('if'))
            and
            (c := self.expression())
            and
            (literal_1 := self.expect(':'))
            and
            (t := self.block())
            and
            (literal_2 := self.expect('else'))
            and
            (literal_3 := self.expect(':'))
            and
            (e := self.block())
        ):
            return kiwi . IfElse ( c , t , e )
        self._reset(mark)
        if (
            (literal := self.expect('if'))
            and
            (c := self.expression())
            and
            (literal_1 := self.expect(':'))
            and
            (t := self.block())
        ):
            return kiwi . IfElse ( c , t , [] )
        self._reset(mark)
        return None

    @memoize
    def while_stmt(self) -> Optional[Any]:
        # while_stmt: 'while' expression ':' block
        mark = self._mark()
        if (
            (literal := self.expect('while'))
            and
            (c := self.expression())
            and
            (literal_1 := self.expect(':'))
            and
            (b := self.block())
        ):
            return kiwi . While ( c , b )
        self._reset(mark)
        return None

    @memoize
    def match_stmt(self) -> Optional[Any]:
        # match_stmt: "match" expression ':' case_block
        mark = self._mark()
        if (
            (literal := self.expect("match"))
            and
            (v := self.expression())
            and
            (literal_1 := self.expect(':'))
            and
            (c := self.case_block())
        ):
            return kiwi . MatchCase ( v , c )
        self._reset(mark)
        return None

    @memoize
    def case_block(self) -> Optional[Any]:
        # case_block: NEWLINE INDENT cases DEDENT NEWLINE
        mark = self._mark()
        if (
            (_newline := self.expect('NEWLINE'))
            and
            (_indent := self.expect('INDENT'))
            and
            (v := self.cases())
            and
            (_dedent := self.expect('DEDENT'))
            and
            (_newline_1 := self.expect('NEWLINE'))
        ):
            return v
        self._reset(mark)
        return None

    @memoize
    def cases(self) -> Optional[Any]:
        # cases: (',' NEWLINE*).case+
        mark = self._mark()
        if (
            (_gather_24 := self._gather_24())
        ):
            return _gather_24
        self._reset(mark)
        return None

    @memoize
    def case(self) -> Optional[Any]:
        # case: "case" expression ':' block
        mark = self._mark()
        if (
            (literal := self.expect("case"))
            and
            (k := self.expression())
            and
            (literal_1 := self.expect(':'))
            and
            (b := self.block())
        ):
            return kiwi . Case ( k , b )
        self._reset(mark)
        return None

    @memoize
    def expression(self) -> Optional[Any]:
        # expression: lambda_def | inversion '?' inversion ':' inversion | inversion
        mark = self._mark()
        if (
            (lambda_def := self.lambda_def())
        ):
            return lambda_def
        self._reset(mark)
        if (
            (c := self.inversion())
            and
            (literal := self.expect('?'))
            and
            (t := self.inversion())
            and
            (literal_1 := self.expect(':'))
            and
            (e := self.inversion())
        ):
            return kiwi . IfExpression ( c , t , e )
        self._reset(mark)
        if (
            (v := self.inversion())
        ):
            return kiwi . Expression ( v )
        self._reset(mark)
        return None

    @memoize
    def lambda_def(self) -> Optional[Any]:
        # lambda_def: "lambda" lambda_parameters ':' expression
        mark = self._mark()
        if (
            (literal := self.expect("lambda"))
            and
            (p := self.lambda_parameters())
            and
            (literal_1 := self.expect(':'))
            and
            (r := self.expression())
        ):
            return kiwi . LambdaDef ( p , r )
        self._reset(mark)
        return None

    @memoize
    def lambda_parameters(self) -> Optional[Any]:
        # lambda_parameters: ','.lambda_param+ | lambda_param?
        # nullable=True
        mark = self._mark()
        if (
            (v := self._gather_26())
        ):
            return v
        self._reset(mark)
        if (
            (opt := self.lambda_param(),)
        ):
            return []
        self._reset(mark)
        return None

    @memoize
    def lambda_param(self) -> Optional[Any]:
        # lambda_param: NAME_
        mark = self._mark()
        if (
            (v := self.NAME_())
        ):
            return kiwi . LambdaParameter ( v )
        self._reset(mark)
        return None

    @memoize
    def inversion(self) -> Optional[Any]:
        # inversion: '!' inversion | comparison
        mark = self._mark()
        if (
            (literal := self.expect('!'))
            and
            (x := self.inversion())
        ):
            return kiwi . UnaryOp ( x , '!' )
        self._reset(mark)
        if (
            (comparison := self.comparison())
        ):
            return comparison
        self._reset(mark)
        return None

    @memoize
    def comparison(self) -> Optional[Any]:
        # comparison: sum compare_op_sum_pair+ | sum
        mark = self._mark()
        if (
            (f := self.sum())
            and
            (v := self._loop1_28())
        ):
            return kiwi . Compare ( [f , * list ( map ( lambda x : x [1] , v ) )] , list ( map ( lambda x : x [0] , v ) ) )
        self._reset(mark)
        if (
            (sum := self.sum())
        ):
            return sum
        self._reset(mark)
        return None

    @memoize
    def compare_op_sum_pair(self) -> Optional[Any]:
        # compare_op_sum_pair: eq_sum | noteq_sum | lte_sum | lt_sum | gte_sum | gt_sum
        mark = self._mark()
        if (
            (eq_sum := self.eq_sum())
        ):
            return eq_sum
        self._reset(mark)
        if (
            (noteq_sum := self.noteq_sum())
        ):
            return noteq_sum
        self._reset(mark)
        if (
            (lte_sum := self.lte_sum())
        ):
            return lte_sum
        self._reset(mark)
        if (
            (lt_sum := self.lt_sum())
        ):
            return lt_sum
        self._reset(mark)
        if (
            (gte_sum := self.gte_sum())
        ):
            return gte_sum
        self._reset(mark)
        if (
            (gt_sum := self.gt_sum())
        ):
            return gt_sum
        self._reset(mark)
        return None

    @memoize
    def eq_sum(self) -> Optional[Any]:
        # eq_sum: '==' sum
        mark = self._mark()
        if (
            (literal := self.expect('=='))
            and
            (v := self.sum())
        ):
            return kiwi . Token ( '==' ) , v
        self._reset(mark)
        return None

    @memoize
    def noteq_sum(self) -> Optional[Any]:
        # noteq_sum: '!=' sum
        mark = self._mark()
        if (
            (literal := self.expect('!='))
            and
            (v := self.sum())
        ):
            return kiwi . Token ( '!=' ) , v
        self._reset(mark)
        return None

    @memoize
    def lte_sum(self) -> Optional[Any]:
        # lte_sum: '<=' sum
        mark = self._mark()
        if (
            (literal := self.expect('<='))
            and
            (v := self.sum())
        ):
            return kiwi . Token ( '<=' ) , v
        self._reset(mark)
        return None

    @memoize
    def lt_sum(self) -> Optional[Any]:
        # lt_sum: '<' sum
        mark = self._mark()
        if (
            (literal := self.expect('<'))
            and
            (v := self.sum())
        ):
            return kiwi . Token ( '<' ) , v
        self._reset(mark)
        return None

    @memoize
    def gte_sum(self) -> Optional[Any]:
        # gte_sum: '>=' sum
        mark = self._mark()
        if (
            (literal := self.expect('>='))
            and
            (v := self.sum())
        ):
            return kiwi . Token ( '>=' ) , v
        self._reset(mark)
        return None

    @memoize
    def gt_sum(self) -> Optional[Any]:
        # gt_sum: '>' sum
        mark = self._mark()
        if (
            (literal := self.expect('>'))
            and
            (v := self.sum())
        ):
            return kiwi . Token ( '>' ) , v
        self._reset(mark)
        return None

    @memoize_left_rec
    def sum(self) -> Optional[Any]:
        # sum: sum '+' term | sum '-' term | term
        mark = self._mark()
        if (
            (x := self.sum())
            and
            (literal := self.expect('+'))
            and
            (y := self.term())
        ):
            return kiwi . BinaryOp ( x , y , kiwi . Token ( '+' ) )
        self._reset(mark)
        if (
            (x := self.sum())
            and
            (literal := self.expect('-'))
            and
            (y := self.term())
        ):
            return kiwi . BinaryOp ( x , y , kiwi . Token ( '-' ) )
        self._reset(mark)
        if (
            (term := self.term())
        ):
            return term
        self._reset(mark)
        return None

    @memoize_left_rec
    def term(self) -> Optional[Any]:
        # term: term '*' factor | term '/' factor | term '%' factor | factor
        mark = self._mark()
        if (
            (x := self.term())
            and
            (literal := self.expect('*'))
            and
            (y := self.factor())
        ):
            return kiwi . BinaryOp ( x , y , kiwi . Token ( '*' ) )
        self._reset(mark)
        if (
            (x := self.term())
            and
            (literal := self.expect('/'))
            and
            (y := self.factor())
        ):
            return kiwi . BinaryOp ( x , y , kiwi . Token ( '/' ) )
        self._reset(mark)
        if (
            (x := self.term())
            and
            (literal := self.expect('%'))
            and
            (y := self.factor())
        ):
            return kiwi . BinaryOp ( x , y , kiwi . Token ( '%' ) )
        self._reset(mark)
        if (
            (factor := self.factor())
        ):
            return factor
        self._reset(mark)
        return None

    @memoize
    def factor(self) -> Optional[Any]:
        # factor: '+' factor | '-' factor | power
        mark = self._mark()
        if (
            (literal := self.expect('+'))
            and
            (x := self.factor())
        ):
            return kiwi . UnaryOp ( x , kiwi . Token ( '+' ) )
        self._reset(mark)
        if (
            (literal := self.expect('-'))
            and
            (x := self.factor())
        ):
            return kiwi . UnaryOp ( x , kiwi . Token ( '-' ) )
        self._reset(mark)
        if (
            (power := self.power())
        ):
            return power
        self._reset(mark)
        return None

    @memoize
    def power(self) -> Optional[Any]:
        # power: primary '**' factor | primary
        mark = self._mark()
        if (
            (x := self.primary())
            and
            (literal := self.expect('**'))
            and
            (y := self.factor())
        ):
            return kiwi . BinaryOp ( x , y , kiwi . Token ( '**' ) )
        self._reset(mark)
        if (
            (primary := self.primary())
        ):
            return primary
        self._reset(mark)
        return None

    @memoize_left_rec
    def primary(self) -> Optional[Any]:
        # primary: "match" expression ':' key_block | primary '.' NAME_ | primary '(' arguments ')' | primary '(' ')' | atom
        mark = self._mark()
        if (
            (literal := self.expect("match"))
            and
            (k := self.expression())
            and
            (literal_1 := self.expect(':'))
            and
            (c := self.key_block())
        ):
            return kiwi . MatchExpr ( k , c )
        self._reset(mark)
        if (
            (v := self.primary())
            and
            (literal := self.expect('.'))
            and
            (a := self.NAME_())
        ):
            return kiwi . Attribute ( v , a )
        self._reset(mark)
        if (
            (i := self.primary())
            and
            (literal := self.expect('('))
            and
            (v := self.arguments())
            and
            (literal_1 := self.expect(')'))
        ):
            return kiwi . Call ( i , v )
        self._reset(mark)
        if (
            (i := self.primary())
            and
            (literal := self.expect('('))
            and
            (literal_1 := self.expect(')'))
        ):
            return kiwi . Call ( i , [] )
        self._reset(mark)
        if (
            (atom := self.atom())
        ):
            return atom
        self._reset(mark)
        return None

    @memoize
    def atom(self) -> Optional[Any]:
        # atom: NAME_ | 'true' | 'false' | 'none' | 'promise' | SELECTOR_ | STRING_ | NUMBER_ | group
        mark = self._mark()
        if (
            (NAME_ := self.NAME_())
        ):
            return NAME_
        self._reset(mark)
        if (
            (literal := self.expect('true'))
        ):
            return kiwi . Token ( 'true' )
        self._reset(mark)
        if (
            (literal := self.expect('false'))
        ):
            return kiwi . Token ( 'false' )
        self._reset(mark)
        if (
            (literal := self.expect('none'))
        ):
            return kiwi . Token ( 'none' )
        self._reset(mark)
        if (
            (literal := self.expect('promise'))
        ):
            return kiwi . Token ( 'promise' )
        self._reset(mark)
        if (
            (SELECTOR_ := self.SELECTOR_())
        ):
            return SELECTOR_
        self._reset(mark)
        if (
            (STRING_ := self.STRING_())
        ):
            return STRING_
        self._reset(mark)
        if (
            (NUMBER_ := self.NUMBER_())
        ):
            return NUMBER_
        self._reset(mark)
        if (
            (group := self.group())
        ):
            return group
        self._reset(mark)
        return None

    @memoize
    def group(self) -> Optional[Any]:
        # group: '(' expression ')'
        mark = self._mark()
        if (
            (literal := self.expect('('))
            and
            (v := self.expression())
            and
            (literal_1 := self.expect(')'))
        ):
            return v
        self._reset(mark)
        return None

    @memoize
    def arguments(self) -> Optional[Any]:
        # arguments: args ','? &')'
        mark = self._mark()
        if (
            (v := self.args())
            and
            (opt := self.expect(','),)
            and
            self.positive_lookahead(self.expect, ')')
        ):
            return v
        self._reset(mark)
        return None

    @memoize
    def args(self) -> Optional[Any]:
        # args: ','.expression+
        mark = self._mark()
        if (
            (v := self._gather_29())
        ):
            return v
        self._reset(mark)
        return None

    @memoize
    def key_block(self) -> Optional[Any]:
        # key_block: NEWLINE INDENT match_keys NEWLINE DEDENT
        mark = self._mark()
        if (
            (_newline := self.expect('NEWLINE'))
            and
            (_indent := self.expect('INDENT'))
            and
            (v := self.match_keys())
            and
            (_newline_1 := self.expect('NEWLINE'))
            and
            (_dedent := self.expect('DEDENT'))
        ):
            return v
        self._reset(mark)
        return None

    @memoize
    def match_keys(self) -> Optional[Any]:
        # match_keys: (',' NEWLINE*).match_key+
        mark = self._mark()
        if (
            (_gather_31 := self._gather_31())
        ):
            return _gather_31
        self._reset(mark)
        return None

    @memoize
    def match_key(self) -> Optional[Any]:
        # match_key: "default" '->' expression | expression "to" expression '->' expression | expression '->' expression
        mark = self._mark()
        if (
            (literal := self.expect("default"))
            and
            (literal_1 := self.expect('->'))
            and
            (v := self.expression())
        ):
            return kiwi . MatchKey ( None , None , v )
        self._reset(mark)
        if (
            (f := self.expression())
            and
            (literal := self.expect("to"))
            and
            (t := self.expression())
            and
            (literal_1 := self.expect('->'))
            and
            (v := self.expression())
        ):
            return kiwi . MatchKey ( f , t , v )
        self._reset(mark)
        if (
            (f := self.expression())
            and
            (literal := self.expect('->'))
            and
            (v := self.expression())
        ):
            return kiwi . MatchKey ( f , f , v )
        self._reset(mark)
        return None

    @memoize
    def NUMBER_(self) -> Optional[Any]:
        # NUMBER_: NUMBER
        mark = self._mark()
        if (
            (v := self.number())
        ):
            return kiwi . Number ( v . string )
        self._reset(mark)
        return None

    @memoize
    def NAME_(self) -> Optional[Any]:
        # NAME_: NAME
        mark = self._mark()
        if (
            (v := self.name())
        ):
            return kiwi . Name ( v . string )
        self._reset(mark)
        return None

    @memoize
    def WORD_(self) -> Optional[Any]:
        # WORD_: ((NUMBER | NAME))+
        mark = self._mark()
        if (
            (v := self._loop1_33())
        ):
            return kiwi . Word ( '' . join ( list ( map ( str , v ) ) ) )
        self._reset(mark)
        return None

    @memoize
    def STRING_(self) -> Optional[Any]:
        # STRING_: STRING+
        mark = self._mark()
        if (
            (v := self._loop1_34())
        ):
            return kiwi . String ( '' . join ( map ( lambda x : x . string , v ) ) )
        self._reset(mark)
        return None

    @memoize
    def SELECTOR_(self) -> Optional[Any]:
        # SELECTOR_: '@' NAME
        mark = self._mark()
        if (
            (literal := self.expect('@'))
            and
            (v := self.name())
        ):
            return kiwi . Selector ( v . string )
        self._reset(mark)
        return None

    @memoize
    def _loop1_1(self) -> Optional[Any]:
        # _loop1_1: (import_stmt | from_import_stmt)
        mark = self._mark()
        children = []
        while (
            (_tmp_35 := self._tmp_35())
        ):
            children.append(_tmp_35)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop1_2(self) -> Optional[Any]:
        # _loop1_2: (NEWLINE | ';')
        mark = self._mark()
        children = []
        while (
            (_tmp_36 := self._tmp_36())
        ):
            children.append(_tmp_36)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop0_4(self) -> Optional[Any]:
        # _loop0_4: ',' dotted_as_name
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self.dotted_as_name())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_3(self) -> Optional[Any]:
        # _gather_3: dotted_as_name _loop0_4
        mark = self._mark()
        if (
            (elem := self.dotted_as_name())
            is not None
            and
            (seq := self._loop0_4())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _loop1_5(self) -> Optional[Any]:
        # _loop1_5: statement
        mark = self._mark()
        children = []
        while (
            (statement := self.statement())
        ):
            children.append(statement)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop1_6(self) -> Optional[Any]:
        # _loop1_6: (NEWLINE | ';')
        mark = self._mark()
        children = []
        while (
            (_tmp_37 := self._tmp_37())
        ):
            children.append(_tmp_37)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop1_7(self) -> Optional[Any]:
        # _loop1_7: (NEWLINE)
        mark = self._mark()
        children = []
        while (
            (_newline := self.expect('NEWLINE'))
        ):
            children.append(_newline)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop0_9(self) -> Optional[Any]:
        # _loop0_9: ',' expression
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self.expression())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_8(self) -> Optional[Any]:
        # _gather_8: expression _loop0_9
        mark = self._mark()
        if (
            (elem := self.expression())
            is not None
            and
            (seq := self._loop0_9())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _loop0_11(self) -> Optional[Any]:
        # _loop0_11: ',' expression
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self.expression())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_10(self) -> Optional[Any]:
        # _gather_10: expression _loop0_11
        mark = self._mark()
        if (
            (elem := self.expression())
            is not None
            and
            (seq := self._loop0_11())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _loop0_13(self) -> Optional[Any]:
        # _loop0_13: ',' expression
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self.expression())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_12(self) -> Optional[Any]:
        # _gather_12: expression _loop0_13
        mark = self._mark()
        if (
            (elem := self.expression())
            is not None
            and
            (seq := self._loop0_13())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _loop0_15(self) -> Optional[Any]:
        # _loop0_15: ',' expression
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self.expression())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_14(self) -> Optional[Any]:
        # _gather_14: expression _loop0_15
        mark = self._mark()
        if (
            (elem := self.expression())
            is not None
            and
            (seq := self._loop0_15())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _loop0_17(self) -> Optional[Any]:
        # _loop0_17: ',' expression
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self.expression())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_16(self) -> Optional[Any]:
        # _gather_16: expression _loop0_17
        mark = self._mark()
        if (
            (elem := self.expression())
            is not None
            and
            (seq := self._loop0_17())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _loop0_18(self) -> Optional[Any]:
        # _loop0_18: expression
        mark = self._mark()
        children = []
        while (
            (expression := self.expression())
        ):
            children.append(expression)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop0_20(self) -> Optional[Any]:
        # _loop0_20: ',' expression
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self.expression())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_19(self) -> Optional[Any]:
        # _gather_19: expression _loop0_20
        mark = self._mark()
        if (
            (elem := self.expression())
            is not None
            and
            (seq := self._loop0_20())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _loop0_21(self) -> Optional[Any]:
        # _loop0_21: expression
        mark = self._mark()
        children = []
        while (
            (expression := self.expression())
        ):
            children.append(expression)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop0_22(self) -> Optional[Any]:
        # _loop0_22: param_no_default
        mark = self._mark()
        children = []
        while (
            (param_no_default := self.param_no_default())
        ):
            children.append(param_no_default)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop0_23(self) -> Optional[Any]:
        # _loop0_23: param_with_default
        mark = self._mark()
        children = []
        while (
            (param_with_default := self.param_with_default())
        ):
            children.append(param_with_default)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop0_25(self) -> Optional[Any]:
        # _loop0_25: (',' NEWLINE*) case
        mark = self._mark()
        children = []
        while (
            (_tmp_38 := self._tmp_38())
            and
            (elem := self.case())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_24(self) -> Optional[Any]:
        # _gather_24: case _loop0_25
        mark = self._mark()
        if (
            (elem := self.case())
            is not None
            and
            (seq := self._loop0_25())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _loop0_27(self) -> Optional[Any]:
        # _loop0_27: ',' lambda_param
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self.lambda_param())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_26(self) -> Optional[Any]:
        # _gather_26: lambda_param _loop0_27
        mark = self._mark()
        if (
            (elem := self.lambda_param())
            is not None
            and
            (seq := self._loop0_27())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _loop1_28(self) -> Optional[Any]:
        # _loop1_28: compare_op_sum_pair
        mark = self._mark()
        children = []
        while (
            (compare_op_sum_pair := self.compare_op_sum_pair())
        ):
            children.append(compare_op_sum_pair)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop0_30(self) -> Optional[Any]:
        # _loop0_30: ',' expression
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self.expression())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_29(self) -> Optional[Any]:
        # _gather_29: expression _loop0_30
        mark = self._mark()
        if (
            (elem := self.expression())
            is not None
            and
            (seq := self._loop0_30())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _loop0_32(self) -> Optional[Any]:
        # _loop0_32: (',' NEWLINE*) match_key
        mark = self._mark()
        children = []
        while (
            (_tmp_39 := self._tmp_39())
            and
            (elem := self.match_key())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_31(self) -> Optional[Any]:
        # _gather_31: match_key _loop0_32
        mark = self._mark()
        if (
            (elem := self.match_key())
            is not None
            and
            (seq := self._loop0_32())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _loop1_33(self) -> Optional[Any]:
        # _loop1_33: (NUMBER | NAME)
        mark = self._mark()
        children = []
        while (
            (_tmp_40 := self._tmp_40())
        ):
            children.append(_tmp_40)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop1_34(self) -> Optional[Any]:
        # _loop1_34: STRING
        mark = self._mark()
        children = []
        while (
            (string := self.string())
        ):
            children.append(string)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _tmp_35(self) -> Optional[Any]:
        # _tmp_35: import_stmt | from_import_stmt
        mark = self._mark()
        if (
            (import_stmt := self.import_stmt())
        ):
            return import_stmt
        self._reset(mark)
        if (
            (from_import_stmt := self.from_import_stmt())
        ):
            return from_import_stmt
        self._reset(mark)
        return None

    @memoize
    def _tmp_36(self) -> Optional[Any]:
        # _tmp_36: NEWLINE | ';'
        mark = self._mark()
        if (
            (_newline := self.expect('NEWLINE'))
        ):
            return _newline
        self._reset(mark)
        if (
            (literal := self.expect(';'))
        ):
            return literal
        self._reset(mark)
        return None

    @memoize
    def _tmp_37(self) -> Optional[Any]:
        # _tmp_37: NEWLINE | ';'
        mark = self._mark()
        if (
            (_newline := self.expect('NEWLINE'))
        ):
            return _newline
        self._reset(mark)
        if (
            (literal := self.expect(';'))
        ):
            return literal
        self._reset(mark)
        return None

    @memoize
    def _tmp_38(self) -> Optional[Any]:
        # _tmp_38: ',' NEWLINE*
        mark = self._mark()
        if (
            (literal := self.expect(','))
            and
            (_loop0_41 := self._loop0_41(),)
        ):
            return [literal, _loop0_41]
        self._reset(mark)
        return None

    @memoize
    def _tmp_39(self) -> Optional[Any]:
        # _tmp_39: ',' NEWLINE*
        mark = self._mark()
        if (
            (literal := self.expect(','))
            and
            (_loop0_42 := self._loop0_42(),)
        ):
            return [literal, _loop0_42]
        self._reset(mark)
        return None

    @memoize
    def _tmp_40(self) -> Optional[Any]:
        # _tmp_40: NUMBER | NAME
        mark = self._mark()
        if (
            (number := self.number())
        ):
            return number
        self._reset(mark)
        if (
            (name := self.name())
        ):
            return name
        self._reset(mark)
        return None

    @memoize
    def _loop0_41(self) -> Optional[Any]:
        # _loop0_41: NEWLINE
        mark = self._mark()
        children = []
        while (
            (_newline := self.expect('NEWLINE'))
        ):
            children.append(_newline)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop0_42(self) -> Optional[Any]:
        # _loop0_42: NEWLINE
        mark = self._mark()
        children = []
        while (
            (_newline := self.expect('NEWLINE'))
        ):
            children.append(_newline)
            mark = self._mark()
        self._reset(mark)
        return children

    KEYWORDS = ('private', 'false', 'namespace', 'pass', 'function', 'public', 'promise', 'true', 'continue', 'if', 'while', 'else', 'break', 'none', 'return')
    SOFT_KEYWORDS = ('import', 'from', 'to', 'as', 'lambda', 'match', 'case', 'default')


if __name__ == '__main__':
    from pegen.parser import simple_parser_main
    simple_parser_main(KiwiParser)
