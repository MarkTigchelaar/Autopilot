require_relative '../parserutilities.rb'
require_relative '../../tokentype.rb'
require_relative '../../keywords.rb'


class ReassignOrCallParser
    def initialize(expression_parser)
        @expression_parser = expression_parser
        @var_name = nil
        @expression_ast = nil
        @functions = Array.new
    end

    def parse(parser)
        errCount = parser.errorCount()
        reset()
        name = parser.nextToken()
        enforceIdentifier(name)
        peekTok = parser.peek()
        assignment_type_token = nil
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(
            [
                EQUAL, PLUS_EQUAL, 
                MINUS_EQUAL, STAR_EQUAL, 
                SLASH_EQUAL, CARROT_EQUAL, MOD_EQUAL
            ].include?(peekTok.getType())
            )
            @var_name = name
            assignment_type_token = peekTok
            equalStep(parser)
        elsif(peekTok.getType() == LEFT_PAREN)
            callFuncStep(parser, name)
        elsif(peekTok.getType() == DOT)
            @var_name = name
            dotStep(parser)
        else
            unexpectedToken(parser)
        end
        r = ReassignmentOrCallStatement.new(@var_name, assignment_type_token, @expression_ast, @functions)
        reset()
        if(errCount < parser.errorCount())
            internalSynchronize(parser)
        end
        return r
    end

    def equalStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok) or is_valid_r_value_keyword(peekTok))
            parseExpression(parser)
        elsif(isInt(peekTok) or isFloat(peekTok))
            parseExpression(parser)
        elsif(is_string_or_char(peekTok))
            parseExpression(parser)
        else
            unexpectedToken(parser)
        end
    end

    def parseExpression(parser)
        @expression_parser.loadTokenizer(parser)
        @expression_ast = @expression_parser.parse_expression()
    end

    def callFuncStep(parser, name)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
            return
        elsif(peekTok.getType() != RIGHT_PAREN and !isValidIdentifier(peekTok) and peekTok.getType() != STRING and peekTok.getType() != CHAR)
            unexpectedToken(parser)
            return
        end
        args = Array.new
        @expression_parser.loadTokenizer(parser)
        while(!isEOF(peekTok) and peekTok.getType() != RIGHT_PAREN)
            ast = @expression_parser.parse_expression()
            args.append(ast)
            peekTok = parser.peek()
            if(isEOF(peekTok))
                eofReached(parser)
                return
            elsif(peekTok.getType() == COMMA)
                parser.discard()
                peekTok = parser.peek()
            elsif(peekTok.getType() == RIGHT_PAREN)
                break
            else
                unexpectedToken(parser)
                return
            end
        end
        @functions.append(FuncCall.new(name, args))
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == RIGHT_PAREN)
            callEndStep(parser)
        else
            unexpectedToken(parser)
        end
    end

    def callEndStep(parser)
        parser.discard()
        peekTok = parser.peek()
        if(peekTok.getType() == DOT)
            dotStep(parser)
        end
    end

    def dotStep(parser)
        parser.discard()
        peekTok = parser.peek()
        # name for "method call"
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(isValidIdentifier(peekTok))
            funcNameStep(parser, peekTok)
        else
            unexpectedToken(parser)
        end
    end

    def funcNameStep(parser, name)
        parser.discard()
        peekTok = parser.peek()
        # name for "method call"
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == LEFT_PAREN)
            callFuncStep(parser, name)
        else
            unexpectedToken(parser)
        end
    end

    def reset
        @var_name = nil
        @expression_ast = nil
        @functions = Array.new
        @expression_parser.reset()
    end

    def enforceIdentifier(token)
        if(!isValidIdentifier(token))
            throw Exception.new("Did not enounter \"valid identifier\" in file " + token.getFilename() + ", got #{token.getText()}")
        end
    end
end

class FuncCall
    def initialize(name, args)
        @name = name
        @args = args
    end

    def toJSON()
        return {
            "name" => @name.getText(),
            "args" => getArgsJSON()
        }
    end

    def getArgsJSON()
        argsJSON = Array.new()
        for arg in @args
            argsJSON.append(arg.toJSON())
        end
        return argsJSON
    end

    def _printLiteral(l)
        l.append("fn:" + @name.getText())
        for arg in @args
            arg._printLiteral(l)
        end
    end

    def _printTokType(type_list)
        type_list.append(@name.getType())
        type_list.append(' ')
        for arg in @args
            type_list.append('|')
            arg._printTokType(type_list)
            
            type_list.append(' ')
        end

    end
end

class ReassignmentOrCallStatement
    def initialize(var_name, assignment_type_token, expression_ast, functions)
        @var_name = var_name
        @expression_ast = expression_ast
        @functions = functions
        @assignment_type_token = assignment_type_token
    end

    def toJSON()
        funcs = Array.new()
        if(@functions != nil)
            for func in @functions
                funcs.append(func.toJSON())
            end
        end
        return {
            "type" => "reassign_or_call",
            "token" => {
                "literal" => getVarNameText(),
                "type" => getVarNameType(),
                "line_number" => getVarNameLine()
            },
            "assignment_type_token" => {
                "literal" => getAssignTypeText(),
                "type" => getAssignType(),
                "line_number" => getLineNumber()
            },
            "functions" => funcs,
            "rvalue" => @expression_ast != nil ? @expression_ast.toJSON() : nil
        }
    end

    

    def getVarNameText()
        name = ""
        name = @var_name.getText() if @var_name
        return name
    end

    def getVarNameType()
        type = ""
        type = @var_name.getType() if @var_name
        return type
    end

    def getVarNameLine()
        line = ""
        line = @var_name.getLine() if @var_name
        return line
    end

    def getAssignTypeText()
        text = ""
        text = @assignment_type_token.getText() if @assignment_type_token
        return text
    end

    def getAssignType()
        type = ""
        type = @assignment_type_token.getType() if @assignment_type_token
        return type
    end

    def getLineNumber()
        line = ""
        line = @assignment_type_token.getLine() if @assignment_type_token
        return line
    end

    def _printTokType(type_list)
        if(@var_name != nil)
            type_list.append(@var_name.getType())
        else
            type_list.append("NONE")
        end
        
        if(@expression_ast != nil)
            type_list.append("|")
            @expression_ast._printTokType(type_list)
        end
        for func in @functions
            type_list.append("|")
            func._printTokType(type_list)
        end
    end

    def _printLiteral()
        if(@functions.length() > 0 and @expression_ast != nil)
            raise Exception.new("can be reassign and call tpye statement.")
        end
        f = Array.new
        str = Array.new
        for func in @functions
            f = Array.new
            func._printLiteral(f)
            for s in f
                str.append(s + "|")
            end
        end
        str = str.join("")

        l = Array.new
        str2 = ""
        if(@expression_ast != nil)
            @expression_ast._printLiteral(l)
        end
        for s in l
            str2 += s + "|"
        end
        var_name = if @var_name then @var_name.getText() else "NONAME" end
        return "|name:#{var_name}|#{str}#{str2}"
    end
end