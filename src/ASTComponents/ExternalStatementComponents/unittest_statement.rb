
class UnittestStatement
    def initialize(name, statements)
        @test_name = name
        @statements = statements
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node_locally(self)
    end

    def toJSON()
        return {
            "type" => "unittest",
            "name" => {
                "literal" => @test_name.getText(),
                "type" => @test_name.getType(),
                "line_number" => @test_name.getLine()
            },
            "statements" => getStatementsJSON()
        }
    end

    def getName()
        @test_name
    end

    def getStatements()
        @statements
    end

    def getStatementsJSON()
        @statements.toJSON()
    end

    def _printLiteral
        l = Array.new
        if(@test_name != nil)
            l.append(@test_name.getText() + ' ')
        end
        l.append(@statements._printLiteral())
        return l.join("").rstrip()
    end

    def _printTokType(type_list)
        if(@test_name != nil)
            type_list.append(@test_name.getType())
        end
        @statements._printTokType(type_list)
    end
end
