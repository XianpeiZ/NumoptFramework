//
// Created by whj on 6/11/18.
//

#ifndef CODE_ANALYSE_VARIABLE_H
#define CODE_ANALYSE_VARIABLE_H

#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include "rose.h"

namespace le
{
    
    using namespace std;
    
    extern const int T_REAL;
    
    extern const string REAL_MANGLED;
    
    class Variable
    {
    public:
        string var_name;
        SgType *type_node;
        SgExpression *initExpr;
        int type_T;
        
        Variable(const string &_var_name, SgType *_type_node, SgExpression *_initExpr = nullptr);
        
        inline bool is_real_type() const
        {
            return type_T == T_REAL;
        }
        
        inline void add_to_stringstream(stringstream &ss) const
        {
            ss << "\"" << var_name << "\": " << type_node->get_mangled() << "";
        }
        
        inline string to_declaration() const
        {
            return type_node->unparseToString() + " " + var_name + ";";
        }
    
        string to_klee_make_symbolic() const;
    
        string to_klee_out_string() const;
    };
    
    class VariableTable
    {
    public:
        map<string, Variable> T;
        
        VariableTable()
        {}
        
        inline bool has_variable(const string &name) const
        {
            return T.find(name) != T.end();
        }
        
        inline void add_variable(const Variable &v)
        {
            if (has_variable(v.var_name)) return;
            T.insert(pair<string, Variable>(v.var_name, v));
        }
        
        inline const Variable &find(const string &name)
        {
            return T.find(name)->second;
        }
        
        string to_string() const;
        
        string to_parameterlist() const;
        
        string to_make_real_klee_symbolic_code(unsigned int tab_num = 0) const;
    
        string to_make_real_klee_output_code(unsigned int tab_num = 0) const;
        
        string to_declaration_code(unsigned int tab_num = 0) const;
        
        string to_variables_reference_list() const;
    
        VariableTable operator+(const VariableTable &t) const;
    };
    
}
#endif //CODE_ANALYSE_VARIABLE_H
