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
        #compatabilityList.append(STRING) # remove substrings
    when PLUS
        compatabilityList.append(INT)
        compatabilityList.append(LONG)
        compatabilityList.append(FLOAT)
        compatabilityList.append(DOUBLE)
        compatabilityList.append(STRING) # append strings
        compatabilityList.append(CHAR) # results in string
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
    when LESS
        compatabilityList.append(INT)
        compatabilityList.append(LONG)
        compatabilityList.append(FLOAT)
        compatabilityList.append(DOUBLE)
        compatabilityList.append(CHAR)
        compatabilityList.append(STRING)
    when LESS_EQUAL
        compatabilityList.append(INT)
        compatabilityList.append(LONG)
        compatabilityList.append(FLOAT)
        compatabilityList.append(DOUBLE)
        compatabilityList.append(CHAR)
        compatabilityList.append(STRING)
    when EQUAL_EQUAL
        compatabilityList.append(INT)
        compatabilityList.append(LONG)
        compatabilityList.append(FLOAT)
        compatabilityList.append(DOUBLE)
        compatabilityList.append(CHAR)
        compatabilityList.append(STRING)
        compatabilityList.append(BOOL)
    when GREATER
        compatabilityList.append(INT)
        compatabilityList.append(LONG)
        compatabilityList.append(FLOAT)
        compatabilityList.append(DOUBLE)
        compatabilityList.append(CHAR)
        compatabilityList.append(STRING)
    when GREATER_EQUAL
        compatabilityList.append(INT)
        compatabilityList.append(LONG)
        compatabilityList.append(FLOAT)
        compatabilityList.append(DOUBLE)
        compatabilityList.append(CHAR)
        compatabilityList.append(STRING)
    when BANG_EQUAL
        compatabilityList.append(INT)
        compatabilityList.append(LONG)
        compatabilityList.append(FLOAT)
        compatabilityList.append(DOUBLE)
        compatabilityList.append(CHAR)
        compatabilityList.append(STRING)
        compatabilityList.append(BOOL)
    when AND
        compatabilityList.append(BOOL)
    when NAND
        compatabilityList.append(BOOL)
    when OR
        compatabilityList.append(BOOL)
    when NOR
        compatabilityList.append(BOOL)
    when XOR
        compatabilityList.append(BOOL)
    when NOT
        compatabilityList.append(BOOL)
    #when PLUS_EQUALS, LESS_EQUALS, OR, AND, NAND, NOW, NOT etc.
    else
        raise Exception.new("INTERNAL ERROR: Unexpected type while testing for operator compatability: #{type}")
    end
    return compatabilityList
end

def get_compatability_list_for_combined_assignment(operator_token)
    compatabilityList = Array.new()


    return compatabilityList
end