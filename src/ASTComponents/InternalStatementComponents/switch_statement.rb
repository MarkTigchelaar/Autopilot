
class SwitchStatement
    def initialize(test_case, case_statements, default_case)
        @test_case = test_case
        @case_statements = case_statements
        @default_case = default_case
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node_locally(self)
    end

    def toJSON()
        return {
            "type" => "switch",
            "test_case" => {
                "literal" => @test_case.getText(),
                "type" => @test_case.getType(),
                "line_number" => @test_case.getLine()
            },
            "cases" => getCasesJSON()
        }
    end

    def getCasesJSON()
        cases = Array.new()
        for _case in @case_statements
            cases.append(_case.toJSON())
        end
        if(@default_case)
            cases.append(@default_case.toJSON())
        end
        return cases
    end

    def _printLiteral
        l = Array.new
        if(@test_case != nil)
            l.append(@test_case.getText() + ' ')
        end
        for stmt in @case_statements
            l.append(stmt._printLiteral())
        end
        if(@default_case != nil)
            l.append(@default_case._printLiteral())
        end
        str = l.join("").rstrip()
        return str
    end

    def _printTokType(type_list)
        if(@test_case != nil)
            type_list.append(@test_case.getType())
        end
        for stmt in @case_statements
            stmt._printTokType(type_list)
        end
        if(@default_case != nil)
            @default_case._printTokType(type_list)
        end
    end
end




class CaseStatement
    def initialize(values, statements)
        @values = values
        @statements = statements
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node_locally(self)
    end

    def toJSON()
        vals = Array.new()
        for v in @values
            vals.append({
                "literal" => v.getText(),
                "type" => v.getType(),
                "line_number" => v.getLine()
            })
        end
        stmts = @statements.toJSON()
        return {
            "values" => vals,
            "statements" => stmts
        }
    end

    def _printLiteral
        l = Array.new
        for val in @values
            l.append(val.getText() + ' ')
        end
        l.append(@statements._printLiteral() + ' ')
        return l.join("")
    end

    def _printTokType(type_list)
        for val in @values
            type_list.append(val.getType())
        end
        @statements._printTokType(type_list)
    end
end
