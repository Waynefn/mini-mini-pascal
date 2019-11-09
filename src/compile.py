from src.syntax import syntax_analysis
from src.lex import lex_analysis
from src.coding import generating_analysis
from src.machine import Machine


def pcompile(filename):
    code = []
    try:
        tokens = lex_analysis(filename)
    except SyntaxError as e:
        print("LEX stage error happens. Reason:{}".format(e.msg))
    except IndexError:
        print("LEX stage error happens. Reason:IndexError")
    else:
        try:
            syntax = syntax_analysis(tokens)
        except SyntaxError as e:
            print("SYN stage error happens. Reason:{}".format(e.msg))
        except IndexError:
            print("SYN stage error happens. Reason:StackError")
        except TypeError:
            print("SYN stage error happens. Reason:Wrong token type")
        else:
            try:
                code = generating_analysis(syntax)
            except SyntaxError as e:
                print("OBJ stage error happens. Reason:{}".format(e.msg))
            except IndexError:
                print("OBJ stage error happens. Reason:IndexError")
            except KeyError:
                print("OBJ stage error happens. Reason:Wrong expression")
    return code


def pcompile_and_run(filename):
    code = pcompile(filename)
    if len(code) == 0:
        return 1
    try:
        m = Machine(code)
    except Exception:
        print("Cannot initialize Machine")
    try:
        m.run()
    except SyntaxError as e:
        print("Machine runtime error. Reason:{}".format(e.msg))
    except IndexError:
        print("Machine runtime error. Reason:StackError")
    except ZeroDivisionError:
        print("Machine runtime error. Reason:ZeroDivisionError")
