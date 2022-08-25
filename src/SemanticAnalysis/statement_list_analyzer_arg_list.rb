class StatementListExternalArgList
    def initialize()
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

    def hasItems(token)
        @current < @ExternalArgs.length - 1
    end

    def nextItem()
        arg = @ExternalArgs[@current]
        @current += 1
        arg
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
