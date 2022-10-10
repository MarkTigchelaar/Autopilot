class StatementListExternalArgList
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
        @ExternalArgs = Array.new()
        @current = 0
    end

    def reset()
        @ExternalArgs = Array.new()
        @current = 0
    end

    def addItem(errMsg, token, role)
        arg = ExternalArgument.new(token, errMsg, role)
        @ExternalArgs.append(arg)
    end

    def hasItems()
        @current < @ExternalArgs.length - 1
    end

    def nextItem()
        arg = @ExternalArgs[@current]
        @current += 1
        arg
    end

    def isDefined(token)
        for arg in @ExternalArgs
            if arg.getName() == token.getText()
                make_and_send_error(token, arg.getErrorMessage())
            end
        end
    end

    def make_and_send_error(field_one, message)
        err = Hash.new()
        err["file"] = field_one.getFilename()
        err["tokenLiteral"] = field_one.getText()
        err["lineNumber"] = field_one.getLine()
        err["message"] = message
        @main_analyzer.add_semantic_error(err)
    end
end

class ExternalArgument
    def initialize(errMsg, token, role)
        @errorMessage = errMsg
        @token = token
        @roleOfToken = role
    end

    def getName()
        @token.getText()
    end

    def getType()
        @token.getType()
    end

    def getRole()
        @roleOfToken
    end

    def getErrorMessage()
        @errorMessage
    end
end
