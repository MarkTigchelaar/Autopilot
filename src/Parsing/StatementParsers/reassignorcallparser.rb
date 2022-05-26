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
        if(isEOF(peekTok))
            eofReached(parser)
        elsif(peekTok.getType() == EQUAL)
            @var_name = name
            equalStep(parser)
        elsif(peekTok.getType() == LEFT_PAREN)
            callFuncStep(parser, name)
        elsif(peekTok.getType() == DOT)
            @var_name = name
            dotStep(parser)
        else
            unexpectedToken(parser)
        end
        r = ReassignmentOrCallStatement.new(@var_name, @expression_ast, @functions)
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
        else
            parseAssignExpression(parser)
        end
    end

    def parseAssignExpression(parser)
        @expression_parser.loadTokenizer(parser)
        @expression_ast = @expression_parser.parse_expression()
    end

    def callFuncStep(parser, name)
        parser.discard()
        peekTok = parser.peek()
        if(isEOF(peekTok))
            eofReached(parser)
            return
        elsif(peekTok.getType() != RIGHT_PAREN and !isValidIdentifier(peekTok))
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
    def initialize(var_name, expression_ast, functions)
        @var_name = var_name
        @expression_ast = expression_ast
        @functions = functions
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
                "literal" => @var_name.getText(),
                "type" => @var_name.getType(),
                "line_number" => @var_name.getLine()
            },
            "functions" => funcs,
            "rvalue" => @expression_ast != nil ? @expression_ast.toJSON() : nil
        }
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