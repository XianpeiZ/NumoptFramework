//
// Created by whj on 6/11/18.
//

#include "Variable.h"
#include "common.h"

namespace le
{
    using namespace std;
    
    const int T_REAL = 10001;
    
    const string REAL_MANGLED = "iRRAM__scope__class_REAL";
    
    Variable::Variable(const string &_var_name, SgType *_type_node, SgExpression *_initExpr) :
            var_name(_var_name), type_node(_type_node), initExpr(_initExpr)
    {
        type_T = type_node->variantT();
        if (type_T == T_CLASS && type_node->get_mangled() == REAL_MANGLED)
        {
            type_T = T_REAL;
        }
    }
    
    string Variable::to_klee_make_symbolic() const
    {
        string res = string("klee_make_symbolic(&") + var_name + ", sizeof(" + var_name + "), \"" + var_name + "\");";
        return res;
    }
    
    string Variable::to_klee_out_string() const
    {
        string res = string("klee_output(\"") + var_name + "\", ";
        if (type_T == T_REAL)
        {
            res += var_name + ".value);";
        }
        else
        {
            res += var_name + ");";
        }
        return res;
    }
    
    string VariableTable::to_string() const
    {
        stringstream ss;
        size_t size = T.size();
        size_t count = 1;
        ss << "{";
        for (const auto &v : T)
        {
            v.second.add_to_stringstream(ss);
            if (count < size)
            {
                ss << ", ";
            }
            ++count;
        }
        ss << "}";
        return ss.str();
    }
    
    string VariableTable::to_parameterlist() const
    {
        if (T.empty()) return "()";
        stringstream ss;
        ss << "(";
        unsigned long idx = 0;
        unsigned long last_idx = T.size() - 1;
        for (const auto &v : T)
        {
            ss << v.second.type_node->unparseToString() << " " << v.second.var_name;
            if (idx == last_idx) break;
            idx++;
            ss << ", ";
        }
        ss << ")";
        return ss.str();
    }
    
    string VariableTable::to_make_real_klee_symbolic_code(unsigned int tab_num) const
    {
        stringstream ss;
        string tab = generate_tab(tab_num);
        for (const auto &v : T)
        {
            const string &name = v.second.var_name;
            if (v.second.is_real_type())
            {
                ss << tab << "klee_make_symbolic(&" << name << ".value," << "sizeof(" << name << ".value)," << "\""
                   << name << "\");" << endl;
            }
        }
        return ss.str();
    }
    
    string VariableTable::to_make_real_klee_output_code(unsigned int tab_num) const
    {
        stringstream ss;
        string tab = generate_tab(tab_num);
        for (const auto &v : T)
        {
            const string &name = v.second.var_name;
            ss << tab << v.second.to_klee_out_string() << endl;
        }
        return ss.str();
    }
    
    string VariableTable::to_declaration_code(unsigned int tab_num) const
    {
        stringstream ss;
        string tab = generate_tab(tab_num);
        for (const auto &v : T)
        {
            ss << tab << v.second.to_declaration() << endl;
        }
        return ss.str();
    }
    
    string VariableTable::to_variables_reference_list() const
    {
        stringstream ss;
        ss << "(";
        unsigned long idx = 0;
        unsigned long last_idx = T.size() - 1;
        for (const auto &v : T)
        {
            ss << v.second.var_name;
            if (idx == last_idx) break;
            idx++;
            ss << ", ";
        }
        ss << ")";
        return ss.str();
    }
    
    VariableTable VariableTable::operator+(const le::VariableTable &t) const
    {
        VariableTable res;
        res.T = T;
        res.T.insert(t.T.begin(), t.T.end());
        return res;
    }
}

