require_relative './testingutilities.rb'

# enums, unions, and errors cannot have duplicate named fields
# enums and unions cannot have duplicate values
# enums cannot have user defined types, only primitives
def phase_two_tests(failurelog, tracker, json)
    puts "\n\n\n Semantic Analysis Tests:\n"
    test_config = TestingConfiguration.new()
    analyzer = SemanticAnalyzer.new(test_config)
    parser = Parser.new(analyzer)
    parser.enable_semantics()
    for test in json
        tests = get_tests_from_file(test["test_manifest_file"])
        general_component = test['general_component']
        unless general_component == "generated_function_return_paths"
            next
        end
        semantic_test(tests, failurelog, tracker, parser, analyzer, general_component)
    end
end

def semantic_test(tests, failurelog, tracker, parser, analyzer, general_component)
    puts "Testing component #{general_component}...\n\n"
    for test_case in tests
        puts "Testing component on file #{test_case["file"]}"
        parser.reset()
        analyzer.reset()
        parser.parse(test_case["file"])
        generic_tests(parser, test_case, failurelog, tracker, true)
        parser.reset()
    end
    puts "Done testing component #{general_component}\n\n"
end


class TestingConfiguration
    def initialize()
        @module_name = "main"
    end

    def module_name()
        @module_name
    end
end