from Parsing.ExternalStatementParsing.enum_parsing import parse_enum as p_enum
from Parsing.ExternalStatementParsing.union_parsing import parse_union as p_union
from Parsing.ExternalStatementParsing.error_parsing import parse_error as p_error
from Parsing.ExternalStatementParsing.import_parsing import parse_import as p_import
from Parsing.ExternalStatementParsing.module_parsing import parse_module as p_module
from Parsing.ExternalStatementParsing.define_parsing import parse_define as p_define
from Parsing.ExternalStatementParsing.interface_parsing import parse_interface as p_interface
from Parsing.ExternalStatementParsing.function_parsing import parse_function as p_function
from Parsing.ExternalStatementParsing.unittest_parsing import parse_unittest as p_unittest
from Parsing.ExternalStatementParsing.struct_parsing import parse_struct as p_struct

from SemanticAnalysis.LocalAnalysis.ExternalStatementAnalyzers.local_enum_analysis import analyze_enum
from SemanticAnalysis.LocalAnalysis.ExternalStatementAnalyzers.local_error_analysis import analyze_error
from SemanticAnalysis.LocalAnalysis.ExternalStatementAnalyzers.local_union_analysis import analyze_union
from SemanticAnalysis.LocalAnalysis.ExternalStatementAnalyzers.local_import_analysis import analyze_import
from SemanticAnalysis.LocalAnalysis.ExternalStatementAnalyzers.local_interface_analysis import analyze_interface
from SemanticAnalysis.LocalAnalysis.ExternalStatementAnalyzers.local_module_analysis import analyze_module
from SemanticAnalysis.LocalAnalysis.ExternalStatementAnalyzers.local_define_analysis import analyze_define
from SemanticAnalysis.LocalAnalysis.ExternalStatementAnalyzers.local_unittest_analysis import analyze_unittest

def temp(analyzer, ast_node):
    return

# these functions should make the rows and columns
# for what ever table(s) are needed for each type
# then return a tree or list of these objects which insert themselves
# into the correct tables, and refer back to the ast as well.
def save_fn(analyzer, ast_node):
    return

def parse_enum(driver):
    ast = p_enum(driver)
    driver.analyze_locally(analyze_enum, save_fn, ast)
    return ast

def parse_union(driver):
    ast = p_union(driver)
    driver.analyze_locally(analyze_union, save_fn, ast)
    return ast

def parse_error(driver):
    ast = p_error(driver)
    driver.analyze_locally(analyze_error, save_fn, ast)
    return ast

def parse_import(driver):
    ast = p_import(driver)
    driver.analyze_locally(analyze_import, save_fn, ast)
    return ast

def parse_module(driver):
    ast = p_module(driver)
    driver.analyze_locally(analyze_module, save_fn, ast)
    return ast

def parse_define(driver):
    ast = p_define(driver)
    driver.analyze_locally(analyze_define, save_fn, ast)
    return ast

def parse_interface(driver):
    ast = p_interface(driver)
    driver.analyze_locally(analyze_interface, save_fn, ast)
    return ast

def parse_unittest(driver):
    ast = p_unittest(driver)
    driver.analyze_locally(analyze_unittest, save_fn, ast)
    return ast

def parse_function(driver):
    ast = p_function(driver)
    driver.analyze_locally(temp, save_fn, ast)
    return ast

def parse_struct(driver):
    ast = p_struct(driver)
    driver.analyze_locally(temp, save_fn, ast)
    return ast
