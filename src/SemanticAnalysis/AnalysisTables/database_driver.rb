

class DataBaseDriver
    def initialize()
        @object_definitions = ObjectDefTable.new()
        @relationships = RelationshipsTable.new()
        @access_modifier_table = AccessModifiersTable.new()
        @tokens_table = TokensTable.new()
    end

end