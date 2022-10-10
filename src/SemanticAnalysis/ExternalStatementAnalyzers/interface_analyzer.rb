class InterfaceAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node_locally(ast_node)
        check_fields(ast_node)
    end

    def check_fields(ast_node)
        name = ast_node.get_name().getText()
        function_defs = ast_node.get_functions()
        for i in (0 .. function_defs.length - 1) do
            for j in (0 .. function_defs.length - 1) do
                if i == j
                    next
                elsif j < i
                    next
                end
                check_fns_for_duplicate_names(function_defs[i], function_defs[j])
            end
            check_fn_args_for_duplicate_names(function_defs[i])
            check_fn_for_interface_name(name, function_defs[i])
            check_fn_args_for_interface_and_fn_name(name, function_defs[i])
        end
    end

    def check_fn_for_interface_name(interface_name, function_def)
        fn_name = function_def.get_name()
        if(interface_name == fn_name.getText())
            msg = "Name collision, function name matches interface name"
            make_and_send_error(fn_name, msg)
        end
    end

    def check_fn_args_for_interface_and_fn_name(interface_name, function_defs)
        fn_name = function_def.get_name()
        args = function_def.get_args()
        for i in (0 .. args.length - 1) do
            arg_name = args[i].get_name()
            if(arg_name.getText() == fn_name.getText())
                msg = "Name collision, function argument name matches function name"
                make_and_send_error(arg_name, msg)
            end
            if(interface_name == arg_name.getText())
                msg = "Name collision, function argument name matches interface name"
                make_and_send_error(arg_name, msg)
            end
        end
    end

    def check_fn_args_for_duplicate_names(function_def)
        args = function_def.get_args()
        for i in (0 .. args.length - 1) do
            arg_name_one = args[i].get_name()
            for j in (0 .. args.length - 1) do
                if i == j
                    next
                elsif j < i
                    next
                end
                arg_name_two = args[j].get_name()
                if(arg_name_one.getText() == arg_name_two.getText())
                    msg = "Name collision, function argument name matches second function argument name"
                    make_and_send_error(arg_name, msg)
                end
            end
        end
    end

    def check_fns_for_duplicate_names(function_def_one, function_def_two)
        if(function_def_one.getText() == function_def_two.getText())
            msg = "Name collision, function name matches second function name"
            make_and_send_error(function_def_one, msg)
        end
    end

    def make_and_send_error(field, message)
        err = Hash.new()
        err["file"] = field.getFilename()
        err["tokenLiteral"] = field.getName()
        err["lineNumber"] = field.getLine()
        err["message"] = message
        @main_analyzer.add_semantic_error(err)
    end
end
