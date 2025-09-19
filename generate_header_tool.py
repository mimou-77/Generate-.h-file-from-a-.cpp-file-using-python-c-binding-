#!/usr/bin/python3

import sys # to use command tools, terminal tools, paths tools 
import clang.cindex # to use libclang index (<=> iterator)
import os # to manipulate paths, recursively iterate directories, manipulate env variables 



clang.cindex.Config.set_library_path("/usr/lib/llvm-19/lib/") 



# cpp_file_path has the format: 'my_file.cpp' or '/home/mariem/my_file.cpp'
def generate_header_from_cpp(cpp_file_path):
    
    # quit if cpp_file doesnt exist
    if not os.path.exists(cpp_file_path):
        print(f"error: the file '{cpp_file_path}' does not exist")
        return

    # if the my_file.h already exists: overwrite it
    # header_file_path = 'my_file.h' or '/home/mariem/my_file.h'
    header_file_path = os.path.splitext(cpp_file_path)[0] + '.h' # splitext(cpp_file_path)[0] = part of the path that's before the last '.'
    if os.path.exists(header_file_path):
        print(f"warning: the header file '{header_file_path}' exists already. Overwiting it.")
    

    try:
        # index <=> iterator
        index = clang.cindex.Index.create()

        # SRC_FILE > preprocessor > PREPROCESSED_SRC_FILE > parser > TRANSLATION_UNIT
        # translation unit = output of the parser ; tu = AST + other things (AST + )
        tu = index.parse(cpp_file_path, args = ['-x', 'c++', '-std=c++17', '-I/usr/include/x86_64-linux-gnu/bits', '-I/home/mariem/esp-matter/components/esp_matter'])
        # ↑ to resolve non std types (like uint16_t and esp_matter_attr_val_t), we must add include paths:
        # '-I/usr/include/x86_64-linux-gnu/bits' (for uint16_t, ...) and '-I/home/mariem/esp-matter/components/esp_matter' (for esp_matter_attr_val_t)


        # open the .h file in mode W ; file will be created if it doesnt exist
        # with ___ as _ : will close the file after the indented block of code is executed
        with open(header_file_path, 'w') as header_file:
            print(f"generating the .h file: {header_file_path}")

            # base_name = last component of a path
            # = 'my_file.h' (gotten from 'my_file.h' or '/home/mariem/my_file.h')
            base_name = os.path.basename(header_file_path)


            ##########################################################
            #   include_guard : 'MY_FILE_H_' PART_1
            ##########################################################
            include_guard = f"_{base_name.replace('.', '_').upper()}_"
            # write = append to file
            header_file.write(f"#ifndef {include_guard}\n")
            header_file.write(f"#define {include_guard}\n\n")


            #######################################################################
            #   collect all includes from my_file.cpp and write them in my_file.h
            #######################################################################
            inc_files_list = [] # example: [ "esp_matter.h", "esp_log.h"]
            # collect all includes from the .cpp file and store them inside inc_files_list
            with open(cpp_file_path, 'r') as cpp_file:
                for line in cpp_file:
                    stripped_line = line.strip() # remove \t, \r, \n
                    if stripped_line.startswith("#include"):
                        inc_file = stripped_line.split(" ", 1)[1].strip().replace("\"", "").replace("<", "").replace(">", "")
                        inc_files_list.append(inc_file)
                        print(f"include found : {inc_file}")
            # write inc_files_list inside the .h file
            for inc in inc_files_list:
                header_file.write(f"#include \"{inc}\" \n")
            header_file.write("\n")

            #################################################################################
            #   collect functions declarations from my_file.cpp and write them in my_file.h
            #################################################################################
            # tu.cursor == the .cpp file
            # tu.cursor.get_children() returns a set of cursors: a cursor for each AST element 
            # example: 
            #          - for a .cpp file that includes 2 classes, 3 fucntions, and 3 global variables: 
            #          tu.cursor.get_children() will return:
            #               2 cursors with type CursorKind.CLASS_DECL
            #               3 cursors with type CursorKind.FUNCTION_DECL
            #               4 cursors with type CursorKind.VAR_DEC
            for cursor in tu.cursor.get_children():
                
                # if function declaration
                if cursor.kind == clang.cindex.CursorKind.FUNCTION_DECL and cursor.is_definition():
                    
                    return_type = cursor.result_type.spelling
                    function_name = cursor.spelling
                    params = []

                    for arg in cursor.get_arguments():

                        params.append(arg.type.spelling + " " + arg.spelling)
                    
                    # prototype = elemets of the array params separated by ','
                    prototype = f"{return_type} {function_name}({','.join(params)});\n"

                    header_file.write(prototype)


            ########################################################################
            #   include_guard : 'MY_FILE_H_' PART_2
            ########################################################################
            #end 'for cursor in...' # we finished traversing all file cursors
            header_file.write(f"\n#endif // {include_guard}\n")


        # end 'with' # we finished opening, processing and closing (auto) the file
        print("Header file generated successfully!")



    # try except : if try block executed without errors => ignore except block
    #              if there is an error in the try block => go to except block to handle the error
    except clang.cindex.LibclangError as e: # error at import: clang.cindex 
        print(f"Error: Failed to load libclang. Check your CLANG installation and path. {e}")

    except Exception as e: # another error
        print(f"An unexpected error occurred: {e}")

    except json.JSONDecodeError:
        print(f"Error: The file '{json_file_path}' is not a valid JSON file.")
    
    except IndexError:
        print("Error: (in the .json file) : The 'configurations' list or 'includePath' list is empty.")
    
    except KeyError as e:
        print(f"Error: (in the .json file) : A required key was not found: {e}")




# __name__ : name of the module that's currently being executed ;
#            <=> the current instruction is from what file 
#            - example: - script is being executed and we are at a line inside it: __name__ = "__main__"
#                       - script is being executed and we are at a line that uses a function from another 
#                       module : __name__ = "my_module"
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_header_tool.py <source_file.cpp> \n or (if sym link ): generate_header_tool <source_file.cpp>")
    else:
        cpp_file = sys.argv[1]
        generate_header_from_cpp(cpp_file)
