require 'set.rb'
require './tokentype.rb'
require_relative './parserutilities.rb'
require_relative '../Tokenization/scanner.rb'

require_relative './expparser.rb'
require_relative './modparser.rb'
require_relative './importparser.rb'
require_relative './defineparser.rb'
require_relative './enumparser.rb'
require_relative './errorparser.rb'
require_relative './functionparser.rb'
require_relative './interfaceparser.rb'
require_relative './structparser.rb'
require_relative './unionparser.rb'
require_relative './unittestparser.rb'
require_relative './StatementParsers/statementparser.rb'

class Parser
    def initialize
        @expression_parser = ExpressionParser.new
        @tokenizer = Scanner.new
        @expression_parser.loadTokenizer(@tokenizer)
        @ast = nil
        @errorList = Array.new
        @shouldSync = false
        @seen_module = false
        @import_and_define_not_allowed = false

        @module_parser = ModuleParser.new
        @import_parser = ImportParser.new
        @define_parser = DefineParser.new

        @statement_parser = StatementParser.new(@expression_parser)

        @function_parser = FunctionParser.new(@statement_parser)
        @struct_parser = StructParser.new(@function_parser)
        @interface_parser = InterfaceParser.new(@function_parser)

        @enum_parser = EnumParser.new
        @union_parser = UnionParser.new
        @error_parser = ErrorParser.new
        @unittest_parser = UnittestParser.new(@statement_parser)
    end

    def toJSON()
        astJSON = Array.new()
        if( @ast != nil)
            for node in @ast
                astJSON.append(node.toJSON())
            end
        end
        return astJSON
    end

    def parse(filename)
        @tokenizer.loadSource(filename)
        @ast = _parse()
        @tokenizer.closeSource()
    end

    def _parse()
        reset()
        ast = Array.new
        while(!match(EOF))
            type  = type_declarations()
            if(type != nil)
                ast.append(type)
            end
            if(@shouldSync)
                return
                externalSynchronize(self)
                syncOff()
            end
        end
        return ast
    end

    def type_declarations()
        if(match(MODULE))
            parse_module()
        elsif(match(DEFINE))
            parse_define()
        elsif(match(IMPORT))
            parse_import()
        elsif(match(ACYCLIC))
            parse_acyclic_type()
        elsif(match(INLINE))
            parse_inline_type()
        elsif(match(PUB))
            parse_public_type()
        elsif(match(UNITTEST))
            parse_unittest()
        else
            other_type()
        end
    end

    def parse_module()
        if(@seen_module)
            mod_not_allowed_error()
            return nil
        end
        @seen_module = true
        return @module_parser.parse(self)
    end

    def parse_define()
        @seen_module = true
        if(@import_and_define_not_allowed)
            define_not_allowed_error()
            return nil
        end
        return @define_parser.parse(self)
    end

    def parse_import()
        @seen_module = true
        if(@import_and_define_not_allowed)
            import_not_allowed_error()
            return nil
        end
        return @import_parser.parse(self)
    end

    def parse_acyclic_type
        @import_and_define_not_allowed = true
        @seen_module = true
        discard()
        is_public = false
        if(match(PUB))
            is_public = true
            discard()
        end

        if(match(INTERFACE))
            i = @interface_parser.parse(self)
            i.setAsAcyclic()
            if(is_public)
                i.setAsPublic()
            end
            return i
        elsif(match(STRUCT))
            s = @struct_parser.parse(self)
            s.setAsAcyclic()
            if(is_public)
                s.setAsPublic()
            end
            return s
        elsif(match(FUN))
            f = @function_parser.parse(self)
            f.setAsAcyclic()
            if(is_public)
                f.setAsPublic()
            end
            return f
        else
            unexpectedToken(self)
        end
    end

    def parse_inline_type()
        @import_and_define_not_allowed = true
        @seen_module = true
        discard()
        is_public = false
        if(match(PUB))
            is_public = true
            discard()
        end

        if(match(STRUCT))
            s = @struct_parser.parse(self)
            s.setAsInline()
            if(is_public)
                s.setAsPublic()
            end
            return s
        elsif(match(FUN))
            f = @function_parser.parse(self)
            f.setAsInline()
            if(is_public)
                f.setAsPublic()
            end
            return f
        else
            unexpectedToken(self)
        end
    end

    def parse_public_type()
        discard()
        t = other_type()
        t.setAsPublic()
        return t
    end

    def parse_unittest()
        @import_and_define_not_allowed = true
        return @unittest_parser.parse(self)
    end

    def other_type()
        @import_and_define_not_allowed = true
        @seen_module = true
        if(match(STRUCT))
            return @struct_parser.parse(self)
        elsif(match(FUN))
            return @function_parser.parse(self)
        elsif(match(INTERFACE))
            return @interface_parser.parse(self)
        elsif(match(ENUM))
            return @enum_parser.parse(self)
        elsif(match(UNION))
            return @union_parser.parse(self)
        elsif(match(ERROR))
            return @error_parser.parse(self)
        else
            unexpectedToken(self)
            return nil
        end
    end

    def noErrors()
        return !hasErrors()
    end

    def hasErrors()
        return @errorList.length > 0
    end

    def errorCount()
        return @errorList.length()
    end

    def getErrorList()
        dup_indicies = Set.new
        for i in (@errorList.length - 1).downto(0) do
            for j in (i - 1).downto(0) do
                if(i == j)
                    next
                end
                b = @errorList[j]
                same_file = @errorList[i]["file"] == b["file"]
                same_lit = @errorList[i]["tokenLiteral"] == b["tokenLiteral"]
                same_line = @errorList[i]["lineNumber"] == b["lineNumber"]
                same_msg = @errorList[i]["message"] == b["message"]
                is_eof = b["message"] == "End of file reached."
                if(same_file and same_lit and same_line and same_msg and is_eof)
                    dup_indicies.add(i)
                end
            end
        end
        for i in (@errorList.length - 1).downto(0) do
            if dup_indicies.include?(i)
                @errorList.delete_at(i)
            end
        end
        return @errorList
    end

    def setToSync()
        @shouldSync = true
    end

    def syncOff()
        @shouldSync = false
    end

    def peek()
        return @tokenizer.peekToken()
    end

    def peekToken()
        return peek()
    end

    def nextToken()
        return @tokenizer.nextToken()
    end

    def match(tokenType)
        tok = peek()
        if(tok.getType() == tokenType)
            return true
        end
        return false
    end

    def discard()
        @tokenizer.nextToken()
    end

    def addError(token, message)
        err = Hash.new()
        err["file"] = token.getFilename()
        err["tokenLiteral"] = token.getText()
        err["lineNumber"] = token.getLine()
        err["message"] = message
        @errorList.append(err)
    end

    def reset
        @ast = nil
        @errorList = Array.new
        @shouldSync = false
        @seen_module = false
        @import_and_define_not_allowed = false
    end

    def mod_not_allowed_error()
        msg = "module cannot be declared after any other statement type"
        tok = nextToken()
        addError(tok, msg)
    end

    def define_not_allowed_error()
        msg = define_or_import_err_msg("define")
        tok = nextToken()
        addError(tok, msg)
    end

    def import_not_allowed_error()
        msg = define_or_import_err_msg("import")
        tok = nextToken()
        addError(tok, msg)
    end

    def define_or_import_err_msg(name)
        return name + " cannot be declared after struct, function, interface, enum, union, error, or unittest statement types"
    end


    def astString()
        astStr = ""
        for stmt in @ast
            astStr += stmt._printLiteral()
        end
        return astStr
    end

    def tokenTypeString()
        type_list = Array.new()
        for stmt in @ast
            stmt._printTokType(type_list)
        end
        str = type_list.join(" ")
        str = str.strip()
        str = str.squeeze(" ")
        return str
    end
end