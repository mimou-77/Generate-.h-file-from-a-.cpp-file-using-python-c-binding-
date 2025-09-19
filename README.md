
# Header generator (uses python)

This tool generates a .h file from a .cpp file.

__How it works:__

This tool uses :
- a C/C++ library: `libclang` : contains __clang compiler__ tools to parse and analyse C/C++ code.
- a Python package: `clang` : contains Python bindings for the __libclang__ library = Python tools that call __libclang__ C/C++ tools ; Language bidinding allows us to use low-level code capapilities (example: C code) from a high-level code like Python, which makes it very easy and simple.

1. The .cpp file is passed as an argument to the Python script.
2. The file is parsed into a __translation unit__ (a description of the src file)
3. This translation unit is traversed to find functions declarations
4. For each fucntion declaration: extract return type, function name, parameters (parameter name + parameter type) and create the prototype as a string that has the format: __"return_type function_name(parameter_1_type parameter_1_name, parameter_2_type parameter_2_name);\n"__
5. A .h file is created with the same name as the .cpp file;
   
   The .h file contains :
   - a header guard at the beginning and at the end (top of the file: #ifndef __MY_FILE_H_ #define __MY_FILE_H_ ... bottom of the file : #endif) 
   - all the functions prototypes for the functions defined in the .cpp file
   - the #includes copied from the .cpp file

> [!IMPORTANT]
> Linux Ubuntu

---

### I. Install Prerequisites:

1. Clone this repository

        git clone https://github.com/mimou-77/Generate-.h-file-from-a-.cpp-file-using-python-c-binding-

2. Install python3

        sudo apt install python3

3. Install __`libclang`__ (Clang development libraries) :
   
    These are APIs (written in C language) for the __Clang__ compiler.

    They allow us to use tools to parse and analyse C/C++ code.

        sudo apt-get install libclang-19-dev

4. Install the __Python bindings package : `clang`__ :
   
   These are Python libraries that execute C libraries, specifically libclang libraries.

   Language bidinding allows us to use low-level code capapilities (example: C code) from a high-level code like Python.

        sudo apt-get install python3-clang-19     

---

### II. Test on a file:

Go to where you cloned this repository, it contains the file __f1.cpp__ we can use as a test example.

    cd ~/header_generator_python ;

        
We will generate the __f1.h__ file from the __f1.cpp__ file:

    /usr/bin/python3 ./generate_header_tool_p.py f1.cpp


>[!Note]
> We can create a symbolic link to use this tool from any place:
>
>       sudo ln -s ~/header_generator_cpp_python/generate_header_tool.py /usr/local/bin/generate_header_tool
>
> Now from any place (example: ~/) you can use the tool:
>
>       cd ;       
>       generate_header_tool my_cpp_file.cpp


