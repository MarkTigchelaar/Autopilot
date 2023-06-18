#import symbols
from ErrorHandling.semantic_error_messages import *
#from keywords import is_key_value_collection_type, is_linear_collection_type

"""
unittest test do
  let stuff = 4
end
"""
def analyze_unittest(analyzer, ast_node):
    from InternalStatementAnalyzers.local_statement_analysis import analyze_statements
    analyzer.begin_local_analysis()
    analyze_statements(analyzer, ast_node.statements)
    analyzer.finish_local_analysis()
