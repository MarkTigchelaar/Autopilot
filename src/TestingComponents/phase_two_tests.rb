require_relative './testingutilities.rb'

# enums, unions, and errors cannot have duplicate named fields
# enums and unions cannot have duplicate values
# enums cannot have user defined types, only primitives
def phase_two_tests(failurelog, tracker, json)
    parser = Parser.new()
    for test in json
        parser.reset()
        tests = get_tests_from_file(test["test_manifest_file"])
        general_component = test['general_component']
        semantic_test(tests, failurelog, tracker, parser, general_component)
    end
end

def semantic_test(tests, failurelog, tracker, parser, general_component)
    puts "Testing component #{general_component}..."
    for test_case in tests
        puts "Testing component on file #{test_case["file"]}"
        parser.parse(test_case["file"])
        generic_tests(parser, test_case, failurelog, tracker, true)
    end
    puts "Done testing component #{general_component}\n"
end
