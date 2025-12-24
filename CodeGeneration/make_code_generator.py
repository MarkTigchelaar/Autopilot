from ASTComponents.AggregatedComponents.modules import RawModuleCollection

from CodeGeneration.code_generator import CodeGenerator
from CodeGeneration.go_code_generator import GoCodeGenerator

def make_code_generator(lanugage_name: str, raw_module_collection: RawModuleCollection) -> CodeGenerator:
    match lanugage_name:
        case "go":
            return GoCodeGenerator(raw_module_collection.get_raw_modules())
        case _:
            raise Exception(f"Language name for code generator type: '{lanugage_name}' not recognized")
            
# One use case is to generate intermediate code, in order to do global semantic analysis of types / attributes etc.
# Another is to go for it, and make bytecode, either for a custom interpreter, or someone elses, or even wasm