require_relative '../tokentype.rb'


def getCompatabilityListForOperator(token)
    compatabilityList = Array.new()
    type = token.getType()
    case type
    when MINUS
        compatabilityList.append(INT)
        compatabilityList.append(LONG)
        compatabilityList.append(FLOAT)
        compatabilityList.append(DOUBLE)
        compatabilityList.append(STRING) # remove substrings
    when PLUS
        compatabilityList.append(INT)
        compatabilityList.append(LONG)
        compatabilityList.append(FLOAT)
        compatabilityList.append(DOUBLE)
        compatabilityList.append(STRING) # append strings
    when STAR
        compatabilityList.append(INT)
        compatabilityList.append(LONG)
        compatabilityList.append(FLOAT)
        compatabilityList.append(DOUBLE)
    when SLASH
        compatabilityList.append(INT)
        compatabilityList.append(LONG)
        compatabilityList.append(FLOAT)
        compatabilityList.append(DOUBLE)
    when CARROT
        compatabilityList.append(INT)
        compatabilityList.append(LONG)
        compatabilityList.append(FLOAT)
        compatabilityList.append(DOUBLE)
    when MOD
        compatabilityList.append(INT)
        compatabilityList.append(LONG)
        compatabilityList.append(FLOAT)
        compatabilityList.append(DOUBLE)
    else
        raise Exception.new("Unexpected type while testing for operator compatability: #{type}")
    end
    return compatabilityList
end