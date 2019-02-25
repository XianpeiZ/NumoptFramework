//
// Created by whj on 6/13/18.
//

#ifndef CODE_ANALYSE_COMMON_H
#define CODE_ANALYSE_COMMON_H

#include <string>
#include <sstream>
#include <fstream>
#include "rose.h"

namespace le
{
    extern const std::string TAB;
    
    extern const std::string klee_code_file_includes;
    extern const std::string klee_output_dir;
    extern const std::string source_code_file_postfix;
    
    extern std::map<VariantT, std::string> operator_str_map;
    
    void init_operator_str_map();
    
    inline std::string generate_tab(unsigned int tab_num)
    {
        std::stringstream ss;
        for (int i = 0; i < tab_num; ++i) ss << TAB;
        return ss.str();
    }
    
    inline std::string int_to_str(const int a)
    {
        std::stringstream ss;
        ss << a;
        return ss.str();
    }
    
    template<class T>
    T *clone(SgNode * node)
    {
        if (node == nullptr) return nullptr;
        SgTreeCopy copy;
        return dynamic_cast<T *>(copy.copyAst(dynamic_cast<SgNode *>(node)));
    }
    
    SgVarRefExp *get_func_call_lhs(SgFunctionCallExp *func_call);
    
    inline bool isAtomStatement(const SgStatement *stmt)
    {
        return dynamic_cast<const SgForStatement *>(stmt) ||
               dynamic_cast<const SgWhileStmt *>(stmt) ||
               dynamic_cast<const SgDoWhileStmt *>(stmt) ||
               dynamic_cast<const SgIfStmt *>(stmt) ||
               dynamic_cast<const SgSwitchStatement *>(stmt);
    }
    
    inline std::string generate_klee_output_stmt(const std::string &name, const std::string &value)
    {
        std::stringstream ss;
        ss << "klee_output(\"" << name << "\", " << value << ");";
        return ss.str();
    }
    
    bool write_stream_to_file(std::string out_file, std::stringstream &ss);
    
    std::string
    expression_to_string_with_value_map(const SgExpression *expr, const std::map<std::string, std::string> &val_map);
    
    bool is_empty_block(SgBasicBlock *block);
    
    extern std::map<std::string, int> real_member_func_set;
    extern std::map<std::string, int> real_relative_func_set;
    
    void init_member_set();
    
    void init_relative_set();
    
    inline bool find_in_member_func_set(const std::string &func_decl)
    {
        return (real_member_func_set.find(func_decl) != real_member_func_set.end());
    }
    
    inline bool find_in_relative_func_set(const std::string &func_decl)
    {
        return (real_relative_func_set.find(func_decl) != real_relative_func_set.end());
    }
    
    SgDotExp *get_member_func_dotExp(SgFunctionCallExp *func_call);
    
    SgExpression *get_member_func_caller(SgFunctionCallExp *func_call);
    
    SgMemberFunctionRefExp *get_member_func_refExp(SgFunctionCallExp *func_call);
    
    SgFunctionRefExp *get_relative_func_refExp(SgFunctionCallExp *func_call);
    
    inline SgExpressionPtrList get_func_parameters(SgFunctionCallExp *func_call)
    {
        return func_call->get_args()->get_expressions();
    }
    
    bool is_compound_assign_option(SgExpression *expr);
    
    std::string get_compound_assign_option_str(SgExpression *expr);
    
    SgBinaryOp *create_relative_binaryOp(SgExpression *expr);
}

#endif //CODE_ANALYSE_COMMON_H
