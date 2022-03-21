require_relative './testingutilities.rb'


def scanner_tests(scanner, test, failurelog, tracker)
    
    filename = test["file"]

    
    #tokens = Array.new()
    scanner.loadSource(filename)

    # Assumption is made that each "test" 
    # result array is the same length.
    expected = test['expected_literal']
    lines = test["line_numbers"]
    token_types = test["token_types"]

    
    i = 0
    while scanner.hasTokens() && i < expected.length
        token = scanner.nextToken()

        msg = " Scanner test for: \"literal\" " + getMsg(expected[i], token.getText())
        component_test(test, failurelog, tracker, msg, expected[i], token.getText())
        
        msg = " Scanner test for: \"filename\" " + getMsg(filename, token.getFilename())
        component_test(test, failurelog, tracker, msg, filename, token.getFilename())
        
        msg = " Scanner test for: \"line number\" " + getMsg(lines[i], token.getLine().to_s())
        component_test(test, failurelog, tracker, msg, lines[i], token.getLine().to_s())
        
        msg = " Scanner test for: \"token type\" " + getMsg(token_types[i], token.getType())
        component_test(test, failurelog, tracker, msg, expected[i], token.getText())

        i += 1
    end
    scanner.closeSource()
end