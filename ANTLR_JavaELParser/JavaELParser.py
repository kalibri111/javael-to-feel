# Generated from src/JavaEL_lex/JavaELParser.g4 by ANTLR 4.9
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\"")
        buf.write("~\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\4\t\t\t\4\n\t\n\4\13\t\13\3\2\3\2\3\2\3\2\3\2\3\2")
        buf.write("\3\2\5\2\36\n\2\3\3\3\3\3\3\7\3#\n\3\f\3\16\3&\13\3\3")
        buf.write("\4\3\4\3\4\7\4+\n\4\f\4\16\4.\13\4\3\5\3\5\3\5\3\5\5\5")
        buf.write("\64\n\5\3\6\3\6\3\6\3\6\3\6\3\6\5\6<\n\6\3\6\3\6\3\6\3")
        buf.write("\6\5\6B\n\6\3\7\3\7\3\7\7\7G\n\7\f\7\16\7J\13\7\3\b\3")
        buf.write("\b\3\b\7\bO\n\b\f\b\16\bR\13\b\3\t\6\tU\n\t\r\t\16\tV")
        buf.write("\3\t\3\t\5\t[\n\t\3\n\3\n\3\n\3\n\3\n\3\n\3\n\7\nd\n\n")
        buf.write("\f\n\16\ng\13\n\3\13\3\13\3\13\3\13\3\13\3\13\5\13o\n")
        buf.write("\13\3\13\3\13\3\13\3\13\3\13\3\13\3\13\3\13\7\13y\n\13")
        buf.write("\f\13\16\13|\13\13\3\13\2\3\24\f\2\4\6\b\n\f\16\20\22")
        buf.write("\24\2\5\3\2\27\30\3\2\31\33\5\2\t\t\30\30\34\34\2\u0089")
        buf.write("\2\35\3\2\2\2\4\37\3\2\2\2\6\'\3\2\2\2\b/\3\2\2\2\nA\3")
        buf.write("\2\2\2\fC\3\2\2\2\16K\3\2\2\2\20Z\3\2\2\2\22\\\3\2\2\2")
        buf.write("\24n\3\2\2\2\26\27\5\4\3\2\27\30\7\25\2\2\30\31\5\2\2")
        buf.write("\2\31\32\7\26\2\2\32\33\5\2\2\2\33\36\3\2\2\2\34\36\5")
        buf.write("\4\3\2\35\26\3\2\2\2\35\34\3\2\2\2\36\3\3\2\2\2\37$\5")
        buf.write("\6\4\2 !\7\b\2\2!#\5\6\4\2\" \3\2\2\2#&\3\2\2\2$\"\3\2")
        buf.write("\2\2$%\3\2\2\2%\5\3\2\2\2&$\3\2\2\2\',\5\b\5\2()\7\7\2")
        buf.write("\2)+\5\b\5\2*(\3\2\2\2+.\3\2\2\2,*\3\2\2\2,-\3\2\2\2-")
        buf.write("\7\3\2\2\2.,\3\2\2\2/\63\5\n\6\2\60\64\7\r\2\2\61\62\7")
        buf.write("\16\2\2\62\64\5\n\6\2\63\60\3\2\2\2\63\61\3\2\2\2\63\64")
        buf.write("\3\2\2\2\64\t\3\2\2\2\65;\5\f\7\2\66<\7\17\2\2\67<\7\20")
        buf.write("\2\28<\7\21\2\29:\7\22\2\2:<\5\f\7\2;\66\3\2\2\2;\67\3")
        buf.write("\2\2\2;8\3\2\2\2;9\3\2\2\2;<\3\2\2\2<B\3\2\2\2=>\7\3\2")
        buf.write("\2>?\5\2\2\2?@\7\4\2\2@B\3\2\2\2A\65\3\2\2\2A=\3\2\2\2")
        buf.write("B\13\3\2\2\2CH\5\16\b\2DE\t\2\2\2EG\5\16\b\2FD\3\2\2\2")
        buf.write("GJ\3\2\2\2HF\3\2\2\2HI\3\2\2\2I\r\3\2\2\2JH\3\2\2\2KP")
        buf.write("\5\20\t\2LM\t\3\2\2MO\5\20\t\2NL\3\2\2\2OR\3\2\2\2PN\3")
        buf.write("\2\2\2PQ\3\2\2\2Q\17\3\2\2\2RP\3\2\2\2SU\t\4\2\2TS\3\2")
        buf.write("\2\2UV\3\2\2\2VT\3\2\2\2VW\3\2\2\2WX\3\2\2\2X[\5\4\3\2")
        buf.write("Y[\5\22\n\2ZT\3\2\2\2ZY\3\2\2\2[\21\3\2\2\2\\e\5\24\13")
        buf.write("\2]^\7\23\2\2^d\5\24\13\2_`\7\5\2\2`a\5\24\13\2ab\7\6")
        buf.write("\2\2bd\3\2\2\2c]\3\2\2\2c_\3\2\2\2dg\3\2\2\2ec\3\2\2\2")
        buf.write("ef\3\2\2\2f\23\3\2\2\2ge\3\2\2\2hi\b\13\1\2io\7\37\2\2")
        buf.write("jo\7\35\2\2ko\7\36\2\2lo\7 \2\2mo\7\"\2\2nh\3\2\2\2nj")
        buf.write("\3\2\2\2nk\3\2\2\2nl\3\2\2\2nm\3\2\2\2oz\3\2\2\2pq\f\5")
        buf.write("\2\2qr\7\3\2\2rs\5\22\n\2st\7\4\2\2ty\3\2\2\2uv\f\4\2")
        buf.write("\2vw\7\3\2\2wy\7\4\2\2xp\3\2\2\2xu\3\2\2\2y|\3\2\2\2z")
        buf.write("x\3\2\2\2z{\3\2\2\2{\25\3\2\2\2|z\3\2\2\2\21\35$,\63;")
        buf.write("AHPVZcenxz")
        return buf.getvalue()


class JavaELParser ( Parser ):

    grammarFileName = "JavaELParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "')'", "'['", "']'", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "'.'", "','", 
                     "'?'", "':'", "'+'", "'-'", "'*'", "<INVALID>", "<INVALID>", 
                     "'empty'", "<INVALID>", "'null'" ]

    symbolicNames = [ "<INVALID>", "OpenParen", "CloseParen", "OpenBracket", 
                      "CloseBracket", "And", "Or", "Not", "Equality", "Relation", 
                      "Logical", "Equal", "NotEqual", "Greater", "Less", 
                      "GreaterEqual", "LessEqual", "Dot", "Comma", "Question", 
                      "DoubleDots", "Plus", "Minus", "Mul", "Div", "Mod", 
                      "Empty", "BooleanLiteral", "NullLiteral", "StringLiteral", 
                      "IntegerLiteral", "WS", "Identifyer" ]

    RULE_ternary = 0
    RULE_expression = 1
    RULE_term = 2
    RULE_equality = 3
    RULE_relation = 4
    RULE_algebraic = 5
    RULE_member = 6
    RULE_base = 7
    RULE_value = 8
    RULE_primitive = 9

    ruleNames =  [ "ternary", "expression", "term", "equality", "relation", 
                   "algebraic", "member", "base", "value", "primitive" ]

    EOF = Token.EOF
    OpenParen=1
    CloseParen=2
    OpenBracket=3
    CloseBracket=4
    And=5
    Or=6
    Not=7
    Equality=8
    Relation=9
    Logical=10
    Equal=11
    NotEqual=12
    Greater=13
    Less=14
    GreaterEqual=15
    LessEqual=16
    Dot=17
    Comma=18
    Question=19
    DoubleDots=20
    Plus=21
    Minus=22
    Mul=23
    Div=24
    Mod=25
    Empty=26
    BooleanLiteral=27
    NullLiteral=28
    StringLiteral=29
    IntegerLiteral=30
    WS=31
    Identifyer=32

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class TernaryContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self):
            return self.getTypedRuleContext(JavaELParser.ExpressionContext,0)


        def Question(self):
            return self.getToken(JavaELParser.Question, 0)

        def ternary(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JavaELParser.TernaryContext)
            else:
                return self.getTypedRuleContext(JavaELParser.TernaryContext,i)


        def DoubleDots(self):
            return self.getToken(JavaELParser.DoubleDots, 0)

        def getRuleIndex(self):
            return JavaELParser.RULE_ternary

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTernary" ):
                listener.enterTernary(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTernary" ):
                listener.exitTernary(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTernary" ):
                return visitor.visitTernary(self)
            else:
                return visitor.visitChildren(self)




    def ternary(self):

        localctx = JavaELParser.TernaryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_ternary)
        try:
            self.state = 27
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 20
                self.expression()
                self.state = 21
                self.match(JavaELParser.Question)
                self.state = 22
                self.ternary()
                self.state = 23
                self.match(JavaELParser.DoubleDots)
                self.state = 24
                self.ternary()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 26
                self.expression()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def term(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JavaELParser.TermContext)
            else:
                return self.getTypedRuleContext(JavaELParser.TermContext,i)


        def Or(self, i:int=None):
            if i is None:
                return self.getTokens(JavaELParser.Or)
            else:
                return self.getToken(JavaELParser.Or, i)

        def getRuleIndex(self):
            return JavaELParser.RULE_expression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression" ):
                listener.enterExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression" ):
                listener.exitExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpression" ):
                return visitor.visitExpression(self)
            else:
                return visitor.visitChildren(self)




    def expression(self):

        localctx = JavaELParser.ExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_expression)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 29
            self.term()
            self.state = 34
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,1,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 30
                    self.match(JavaELParser.Or)
                    self.state = 31
                    self.term() 
                self.state = 36
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,1,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TermContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def equality(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JavaELParser.EqualityContext)
            else:
                return self.getTypedRuleContext(JavaELParser.EqualityContext,i)


        def And(self, i:int=None):
            if i is None:
                return self.getTokens(JavaELParser.And)
            else:
                return self.getToken(JavaELParser.And, i)

        def getRuleIndex(self):
            return JavaELParser.RULE_term

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTerm" ):
                listener.enterTerm(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTerm" ):
                listener.exitTerm(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTerm" ):
                return visitor.visitTerm(self)
            else:
                return visitor.visitChildren(self)




    def term(self):

        localctx = JavaELParser.TermContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_term)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 37
            self.equality()
            self.state = 42
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 38
                    self.match(JavaELParser.And)
                    self.state = 39
                    self.equality() 
                self.state = 44
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class EqualityContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def relation(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JavaELParser.RelationContext)
            else:
                return self.getTypedRuleContext(JavaELParser.RelationContext,i)


        def Equal(self):
            return self.getToken(JavaELParser.Equal, 0)

        def NotEqual(self):
            return self.getToken(JavaELParser.NotEqual, 0)

        def getRuleIndex(self):
            return JavaELParser.RULE_equality

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEquality" ):
                listener.enterEquality(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEquality" ):
                listener.exitEquality(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEquality" ):
                return visitor.visitEquality(self)
            else:
                return visitor.visitChildren(self)




    def equality(self):

        localctx = JavaELParser.EqualityContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_equality)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 45
            self.relation()
            self.state = 49
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                self.state = 46
                self.match(JavaELParser.Equal)

            elif la_ == 2:
                self.state = 47
                self.match(JavaELParser.NotEqual)
                self.state = 48
                self.relation()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RelationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def algebraic(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JavaELParser.AlgebraicContext)
            else:
                return self.getTypedRuleContext(JavaELParser.AlgebraicContext,i)


        def Greater(self):
            return self.getToken(JavaELParser.Greater, 0)

        def Less(self):
            return self.getToken(JavaELParser.Less, 0)

        def GreaterEqual(self):
            return self.getToken(JavaELParser.GreaterEqual, 0)

        def LessEqual(self):
            return self.getToken(JavaELParser.LessEqual, 0)

        def OpenParen(self):
            return self.getToken(JavaELParser.OpenParen, 0)

        def ternary(self):
            return self.getTypedRuleContext(JavaELParser.TernaryContext,0)


        def CloseParen(self):
            return self.getToken(JavaELParser.CloseParen, 0)

        def getRuleIndex(self):
            return JavaELParser.RULE_relation

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRelation" ):
                listener.enterRelation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRelation" ):
                listener.exitRelation(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRelation" ):
                return visitor.visitRelation(self)
            else:
                return visitor.visitChildren(self)




    def relation(self):

        localctx = JavaELParser.RelationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_relation)
        try:
            self.state = 63
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [JavaELParser.Not, JavaELParser.Minus, JavaELParser.Empty, JavaELParser.BooleanLiteral, JavaELParser.NullLiteral, JavaELParser.StringLiteral, JavaELParser.IntegerLiteral, JavaELParser.Identifyer]:
                self.enterOuterAlt(localctx, 1)
                self.state = 51
                self.algebraic()
                self.state = 57
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
                if la_ == 1:
                    self.state = 52
                    self.match(JavaELParser.Greater)

                elif la_ == 2:
                    self.state = 53
                    self.match(JavaELParser.Less)

                elif la_ == 3:
                    self.state = 54
                    self.match(JavaELParser.GreaterEqual)

                elif la_ == 4:
                    self.state = 55
                    self.match(JavaELParser.LessEqual)
                    self.state = 56
                    self.algebraic()


                pass
            elif token in [JavaELParser.OpenParen]:
                self.enterOuterAlt(localctx, 2)
                self.state = 59
                self.match(JavaELParser.OpenParen)
                self.state = 60
                self.ternary()
                self.state = 61
                self.match(JavaELParser.CloseParen)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AlgebraicContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def member(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JavaELParser.MemberContext)
            else:
                return self.getTypedRuleContext(JavaELParser.MemberContext,i)


        def Plus(self, i:int=None):
            if i is None:
                return self.getTokens(JavaELParser.Plus)
            else:
                return self.getToken(JavaELParser.Plus, i)

        def Minus(self, i:int=None):
            if i is None:
                return self.getTokens(JavaELParser.Minus)
            else:
                return self.getToken(JavaELParser.Minus, i)

        def getRuleIndex(self):
            return JavaELParser.RULE_algebraic

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAlgebraic" ):
                listener.enterAlgebraic(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAlgebraic" ):
                listener.exitAlgebraic(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAlgebraic" ):
                return visitor.visitAlgebraic(self)
            else:
                return visitor.visitChildren(self)




    def algebraic(self):

        localctx = JavaELParser.AlgebraicContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_algebraic)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 65
            self.member()
            self.state = 70
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,6,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 66
                    _la = self._input.LA(1)
                    if not(_la==JavaELParser.Plus or _la==JavaELParser.Minus):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 67
                    self.member() 
                self.state = 72
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,6,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MemberContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def base(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JavaELParser.BaseContext)
            else:
                return self.getTypedRuleContext(JavaELParser.BaseContext,i)


        def Mul(self, i:int=None):
            if i is None:
                return self.getTokens(JavaELParser.Mul)
            else:
                return self.getToken(JavaELParser.Mul, i)

        def Div(self, i:int=None):
            if i is None:
                return self.getTokens(JavaELParser.Div)
            else:
                return self.getToken(JavaELParser.Div, i)

        def Mod(self, i:int=None):
            if i is None:
                return self.getTokens(JavaELParser.Mod)
            else:
                return self.getToken(JavaELParser.Mod, i)

        def getRuleIndex(self):
            return JavaELParser.RULE_member

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMember" ):
                listener.enterMember(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMember" ):
                listener.exitMember(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMember" ):
                return visitor.visitMember(self)
            else:
                return visitor.visitChildren(self)




    def member(self):

        localctx = JavaELParser.MemberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_member)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 73
            self.base()
            self.state = 78
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,7,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 74
                    _la = self._input.LA(1)
                    if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << JavaELParser.Mul) | (1 << JavaELParser.Div) | (1 << JavaELParser.Mod))) != 0)):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 75
                    self.base() 
                self.state = 80
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,7,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BaseContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self):
            return self.getTypedRuleContext(JavaELParser.ExpressionContext,0)


        def Empty(self, i:int=None):
            if i is None:
                return self.getTokens(JavaELParser.Empty)
            else:
                return self.getToken(JavaELParser.Empty, i)

        def Not(self, i:int=None):
            if i is None:
                return self.getTokens(JavaELParser.Not)
            else:
                return self.getToken(JavaELParser.Not, i)

        def Minus(self, i:int=None):
            if i is None:
                return self.getTokens(JavaELParser.Minus)
            else:
                return self.getToken(JavaELParser.Minus, i)

        def value(self):
            return self.getTypedRuleContext(JavaELParser.ValueContext,0)


        def getRuleIndex(self):
            return JavaELParser.RULE_base

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBase" ):
                listener.enterBase(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBase" ):
                listener.exitBase(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBase" ):
                return visitor.visitBase(self)
            else:
                return visitor.visitChildren(self)




    def base(self):

        localctx = JavaELParser.BaseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_base)
        self._la = 0 # Token type
        try:
            self.state = 88
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [JavaELParser.Not, JavaELParser.Minus, JavaELParser.Empty]:
                self.enterOuterAlt(localctx, 1)
                self.state = 82 
                self._errHandler.sync(self)
                _alt = 1
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt == 1:
                        self.state = 81
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << JavaELParser.Not) | (1 << JavaELParser.Minus) | (1 << JavaELParser.Empty))) != 0)):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()

                    else:
                        raise NoViableAltException(self)
                    self.state = 84 
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,8,self._ctx)

                self.state = 86
                self.expression()
                pass
            elif token in [JavaELParser.BooleanLiteral, JavaELParser.NullLiteral, JavaELParser.StringLiteral, JavaELParser.IntegerLiteral, JavaELParser.Identifyer]:
                self.enterOuterAlt(localctx, 2)
                self.state = 87
                self.value()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ValueContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def primitive(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JavaELParser.PrimitiveContext)
            else:
                return self.getTypedRuleContext(JavaELParser.PrimitiveContext,i)


        def Dot(self, i:int=None):
            if i is None:
                return self.getTokens(JavaELParser.Dot)
            else:
                return self.getToken(JavaELParser.Dot, i)

        def OpenBracket(self, i:int=None):
            if i is None:
                return self.getTokens(JavaELParser.OpenBracket)
            else:
                return self.getToken(JavaELParser.OpenBracket, i)

        def CloseBracket(self, i:int=None):
            if i is None:
                return self.getTokens(JavaELParser.CloseBracket)
            else:
                return self.getToken(JavaELParser.CloseBracket, i)

        def getRuleIndex(self):
            return JavaELParser.RULE_value

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterValue" ):
                listener.enterValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitValue" ):
                listener.exitValue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitValue" ):
                return visitor.visitValue(self)
            else:
                return visitor.visitChildren(self)




    def value(self):

        localctx = JavaELParser.ValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_value)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 90
            self.primitive(0)
            self.state = 99
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==JavaELParser.OpenBracket or _la==JavaELParser.Dot:
                self.state = 97
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [JavaELParser.Dot]:
                    self.state = 91
                    self.match(JavaELParser.Dot)
                    self.state = 92
                    self.primitive(0)
                    pass
                elif token in [JavaELParser.OpenBracket]:
                    self.state = 93
                    self.match(JavaELParser.OpenBracket)
                    self.state = 94
                    self.primitive(0)
                    self.state = 95
                    self.match(JavaELParser.CloseBracket)
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 101
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrimitiveContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def StringLiteral(self):
            return self.getToken(JavaELParser.StringLiteral, 0)

        def BooleanLiteral(self):
            return self.getToken(JavaELParser.BooleanLiteral, 0)

        def NullLiteral(self):
            return self.getToken(JavaELParser.NullLiteral, 0)

        def IntegerLiteral(self):
            return self.getToken(JavaELParser.IntegerLiteral, 0)

        def Identifyer(self):
            return self.getToken(JavaELParser.Identifyer, 0)

        def primitive(self):
            return self.getTypedRuleContext(JavaELParser.PrimitiveContext,0)


        def OpenParen(self):
            return self.getToken(JavaELParser.OpenParen, 0)

        def CloseParen(self):
            return self.getToken(JavaELParser.CloseParen, 0)

        def value(self):
            return self.getTypedRuleContext(JavaELParser.ValueContext,0)


        def getRuleIndex(self):
            return JavaELParser.RULE_primitive

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrimitive" ):
                listener.enterPrimitive(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrimitive" ):
                listener.exitPrimitive(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrimitive" ):
                return visitor.visitPrimitive(self)
            else:
                return visitor.visitChildren(self)



    def primitive(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = JavaELParser.PrimitiveContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 18
        self.enterRecursionRule(localctx, 18, self.RULE_primitive, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 108
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [JavaELParser.StringLiteral]:
                self.state = 103
                self.match(JavaELParser.StringLiteral)
                pass
            elif token in [JavaELParser.BooleanLiteral]:
                self.state = 104
                self.match(JavaELParser.BooleanLiteral)
                pass
            elif token in [JavaELParser.NullLiteral]:
                self.state = 105
                self.match(JavaELParser.NullLiteral)
                pass
            elif token in [JavaELParser.IntegerLiteral]:
                self.state = 106
                self.match(JavaELParser.IntegerLiteral)
                pass
            elif token in [JavaELParser.Identifyer]:
                self.state = 107
                self.match(JavaELParser.Identifyer)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 120
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,14,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 118
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,13,self._ctx)
                    if la_ == 1:
                        localctx = JavaELParser.PrimitiveContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_primitive)
                        self.state = 110
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 111
                        self.match(JavaELParser.OpenParen)

                        self.state = 112
                        self.value()
                        self.state = 113
                        self.match(JavaELParser.CloseParen)
                        pass

                    elif la_ == 2:
                        localctx = JavaELParser.PrimitiveContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_primitive)
                        self.state = 115
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 116
                        self.match(JavaELParser.OpenParen)
                        self.state = 117
                        self.match(JavaELParser.CloseParen)
                        pass

             
                self.state = 122
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,14,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[9] = self.primitive_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def primitive_sempred(self, localctx:PrimitiveContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 2)
         




