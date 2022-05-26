

SUCCESS = "TEST CASE SUCCESSFUL,"
FAILURE = "TEST CASE FAILURE,"

def component_test(test_case, failurelog, tracker, msg, expected, result)
    if(result != expected)
        tracker.incFail()
        msg = FAILURE + "In #{test_case["file"]}: " + msg
        puts msg
        failurelog.write("In #{test_case["file"]}" + "\n")
        failurelog.write(msg + "\n\n")
    else
        tracker.incSuccess()
        puts SUCCESS + msg
    end
end

def get_tests_from_file(testfilename)
    jsonfile = File.open(testfilename)
    tests = JSON.parse(jsonfile.read())
    jsonfile.close()
    return tests
end

def getMsg(expect, actual)
    return " expected: \"#{expect}\", got \"#{actual}\""
end

def printErrors(reportedErrors)
    for err in reportedErrors do
        puts "file name: #{err["file"]}"
        puts "token literal: #{err["tokenLiteral"]}"
        puts "line number: #{err["lineNumber"]}"
        puts "message: #{err["message"]}"
    end
end

def error_test(test_case, parser, failurelog, tracker)
    reportedErrors = parser.getErrorList()
    numExpErrors = test_case["errors"].length
    numActualErrors = reportedErrors.length
    if(numExpErrors != numActualErrors)
        raise Exception.new(
           "mismatch of errors in #{test_case["file"]}, expected: #{numExpErrors}, got #{numActualErrors}"
        )
    else
        puts "NUMBER OF ERRORS MATCHES EXPECTED NUMBER OF ERRORS #{numActualErrors}, #{numExpErrors}"
    end
    for i in 0 .. numActualErrors-1 do
        testErr = test_case["errors"][i]
        actualErr = reportedErrors[i]
        msg = getMsg(
            "\"" + testErr["message"] + "\"", 
            "\"" + actualErr["message"] + "\""
        )
        component_test(
            test_case, 
            failurelog, 
            tracker, 
            msg, 
            testErr["message"], 
            actualErr["message"]
        )

        msg = getMsg(
            testErr["lineNumber"], 
            actualErr["lineNumber"]
        )
        
        component_test(
            test_case, 
            failurelog, 
            tracker, 
            msg, 
            testErr["lineNumber"], 
            actualErr["lineNumber"]
        )

        msg = getMsg(
            testErr["tokenLiteral"], 
            actualErr["tokenLiteral"]
        )
        component_test(
            test_case, 
            failurelog, 
            tracker, 
            msg, 
            testErr["tokenLiteral"], 
            actualErr["tokenLiteral"]
        )
    end
    
end

def generic_parser_tests(dummy, test_case, failurelog, tracker)
    if(test_case["errors"] == nil && dummy.hasErrors())
        puts "Errors detected, but did not expect errors!"
        printErrors(dummy.getErrorList())
        raise Exception.new("Errors detected, but did not expect errors!")
    elsif(test_case["errors"] == nil && !dummy.hasErrors())
        msg = getMsg(test_case["astString"], dummy.astString())
        component_test(
            test_case, 
            failurelog, 
            tracker, 
            msg, 
            test_case["astString"], 
            dummy.astString()
        )
        msg = getMsg(
            test_case["tokenTypeString"], 
            dummy.tokenTypeString()
        )
        component_test(
            test_case, 
            failurelog, 
            tracker, 
            msg, 
            dummy.tokenTypeString(), 
            test_case["tokenTypeString"]
        )
    else
        e = dummy.getErrorList()
        printErrors(e)
        error_test(test_case, dummy, failurelog, tracker)
    end
end