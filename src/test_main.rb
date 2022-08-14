require 'json'
require './TestingComponents/phase_one_tests.rb'
require './TestingComponents/phase_two_tests.rb'

TEST_MANIFEST_ONE = "../TestFiles/tokenizer_parser_test_manifest.json"
TEST_MANIFEST_TWO = "../TestFiles/semantic_analysis_test_manifest.json"

def main()
    failurelog = File.open("./failed_tests.txt", 'w')
    tracker = ProgressTracker.new()

    test_json = get_test_listing(TEST_MANIFEST_ONE)
    phase_one_tests(failurelog, tracker, test_json)

    #test_json = get_test_listing(TEST_MANIFEST_TWO)
    #phase_two_tests(failurelog, tracker, test_json)

    failurelog.close()
    puts tracker.getResults()
    if(tracker.noFailures())
        File.delete("./failed_tests.txt")
    end
end

def get_test_listing(manifest)
    jsonfile = File.open(manifest)
    json = JSON.parse(jsonfile.read())
    jsonfile.close()
    return json
end

class ProgressTracker
    def initialize
        @total = 0
        @passed = 0
        @failed = 0
    end

    def incSuccess
        @total += 1
        @passed += 1
    end

    def incFail
        @total += 1
        @failed += 1
    end

    def getResults
        return "Tests passed: #{@passed}/#{@total}, tests failed: #{@failed}/#{@total}"
    end

    def noFailures
        return @failed == 0
    end
end

main()
