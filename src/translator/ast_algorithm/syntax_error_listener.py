from antlr4.error.ErrorListener import ErrorListener
from ANTLR_JavaELParser.JavaELParser import JavaELParser
from ANTLR_FEELParser.feelParser import feelParser
from loguru import logger

logger.opt(colors=True)


class ANTLRBaseException(Exception):
    pass


class JavaELSyntaxError(ANTLRBaseException):
    pass


class FEELSyntaxError(ANTLRBaseException):
    pass


class JavaELSyntaxErrorMixin:
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        if not isinstance(recognizer, JavaELParser):
            return
        else:
            error_msg = f"JavaEL synatax error: unexpected symbol {offendingSymbol}"
            logger.error(error_msg)
            super(JavaELSyntaxErrorMixin, self).syntaxError(recognizer, offendingSymbol, line, column, msg, e)
            raise JavaELSyntaxError(error_msg)


class FEELSyntaxErrorMixin:
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        if not isinstance(recognizer, feelParser):
            return
        else:
            error_msg = f"FEEL synatax error: unexpected symbol {offendingSymbol}"
            logger.error(error_msg)
            super(FEELSyntaxErrorMixin, self).syntaxError(recognizer, offendingSymbol, line, column, msg, e)
            raise FEELSyntaxError(error_msg)


class JavaELSyntaxErrorHandler(JavaELSyntaxErrorMixin, ErrorListener):
    pass


class FEELSyntaxErrorHandler(FEELSyntaxErrorMixin, ErrorListener):
    pass
