//
// Created by whj on 6/11/18.
//

#ifndef CODE_ANALYSE_FUNCTION_H
#define CODE_ANALYSE_FUNCTION_H

#include <iostream>
#include <vector>
#include <string>
#include "common.h"
#include "Variable.h"
#include "Code_Tree_Node.h"

namespace le
{
    
    using namespace std;
    
    bool isAtomStatement(const SgStatement *stmt);
    
    class Function
    {
    private:
        void add_input_parameter(const Variable &v);
        
        void add_input_parameterlist();
    
        void write_function_correspond_main_func(stringstream &ss) const;
    
        VariableTable get_variables_declared_in_function() const;
    
    public:
        string program_name;
        string func_name;
        SgFunctionDeclaration *decl;
        VariableTable input_parameters;
        vector<string> input_parameters_list; // we need to record the order of input parameters
        shared_ptr<Code_Tree_Node> root;
    
        Function(const string &_func_name, SgFunctionDeclaration *_decl, const string &_program_name);

//        VariableTable collect_all_var_tbl();
        
        string to_string() const;
        
        string to_code() const;
        
        void write_simple_json_file() const;
        
        void to_klee_code_functions() const;
    };
    
}
#endif //CODE_ANALYSE_FUNCTION_H
