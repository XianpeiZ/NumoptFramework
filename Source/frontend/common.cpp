//
// Created by whj on 6/13/18.
//


#include "common.h"

namespace le
{
    const std::string TAB = "    ";
    
    const std::string klee_code_file_includes = "#include \"include/REAL.h\"\n"
                                                "#include \"klee.h\"\n"
                                                "#include \"include/klee_expression.h\"\n"
                                                "using namespace iRRAM;\n\n";
    
    const std::string klee_output_dir = "/home/whj/Programs/numopt_preprocess/klee_output/";
    const std::string source_code_file_postfix = ".cpp";
    
    std::map<VariantT, std::string> operator_str_map;
    
    void init_operator_str_map()
    {
        operator_str_map[V_SgEqualityOp] = "==";
        operator_str_map[V_SgLessThanOp] = "<";
        operator_str_map[V_SgGreaterThanOp] = ">";
        operator_str_map[V_SgNotEqualOp] = "!=";
        operator_str_map[V_SgLessOrEqualOp] = "<=";
        operator_str_map[V_SgGreaterOrEqualOp] = ">=";
        operator_str_map[V_SgAddOp] = "+";
        operator_str_map[V_SgSubtractOp] = "-";
        operator_str_map[V_SgMultiplyOp] = "*";
        operator_str_map[V_SgDivideOp] = "/";
        operator_str_map[V_SgIntegerDivideOp] = "/";
        operator_str_map[V_SgModOp] = "%";
        operator_str_map[V_SgAndOp] = "&&";
        operator_str_map[V_SgOrOp] = "||";
        operator_str_map[V_SgBitXorOp] = "^";
        operator_str_map[V_SgBitAndOp] = "&";
        operator_str_map[V_SgBitOrOp] = "|";
        operator_str_map[V_SgCommaOpExp] = ",";
        operator_str_map[V_SgLshiftOp] = "<<";
        operator_str_map[V_SgRshiftOp] = ">>";
        operator_str_map[V_SgNotOp] = "!";
        operator_str_map[V_SgAssignOp] = "=";
        operator_str_map[V_SgPointerDerefExp] = "*";
        operator_str_map[V_SgAddressOfOp] = "&";
        operator_str_map[V_SgPlusAssignOp] = "+=";
        operator_str_map[V_SgMinusAssignOp] = "-=";
        operator_str_map[V_SgAndAssignOp] = "&&=";
        operator_str_map[V_SgIorAssignOp] = "||=";
        operator_str_map[V_SgMultAssignOp] = "*=";
        operator_str_map[V_SgDivAssignOp] = "/=";
        operator_str_map[V_SgModAssignOp] = "%=";
        operator_str_map[V_SgXorAssignOp] = "^=";
        operator_str_map[V_SgLshiftAssignOp] = "<<=";
    }
    
    std::string get_operator_str(VariantT type)
    {
        auto op = operator_str_map.find(type);
        assert(op != operator_str_map.end());
        return op->second;
    }
    
    SgVarRefExp *get_func_call_lhs(SgFunctionCallExp *func_call)
    {
        auto suc_list = func_call->get_traversalSuccessorContainer();
        for (auto n : suc_list)
        {
            if (auto dot_exp = dynamic_cast<SgDotExp *>(n))
            {
                SgExpression *left = dot_exp->get_lhs_operand();
                return dynamic_cast<SgVarRefExp *>(left);
            }
        }
        return nullptr;
    }
    
    bool write_stream_to_file(std::string out_file, std::stringstream &ss)
    {
        std::ofstream out;
        out.open(out_file, std::ofstream::out);
        if (out)
        {
            out << ss.str();
            out.close();
            return true;
        }
        return false;
    }
    
    void expression_to_string_with_value_map(std::stringstream &ss, const SgExpression *expr,
                                             const std::map<std::string, std::string> &val_map)
    {
        if (auto func_call = dynamic_cast<const SgFunctionCallExp *>(expr))
        {
            ss << func_call->unparseToString();
        }
        else if (auto binary_op = dynamic_cast<const SgBinaryOp *>(expr))
        {
            SgExpression *left = binary_op->get_lhs_operand_i();
            SgExpression *right = binary_op->get_rhs_operand_i();
            expression_to_string_with_value_map(ss, left, val_map);
            ss << get_operator_str(binary_op->variantT());
            expression_to_string_with_value_map(ss, right, val_map);
        }
        else if (auto unary_op = dynamic_cast<const SgUnaryOp *>(expr))
        {
            if (auto cast_exp = dynamic_cast<const SgCastExp *>(unary_op))
            {
                ss << cast_exp->get_type()->unparseToString() << "(";
            }
            else
            {
                ss << get_operator_str(unary_op->variantT());
            }
            expression_to_string_with_value_map(ss, unary_op->get_operand(), val_map);
            if (auto cast_exp = dynamic_cast<const SgCastExp *>(unary_op))
            {
                ss << ")";
            }
        }
        else if (auto var_ref = dynamic_cast<const SgVarRefExp *>(expr))
        {
            std::string var_name = var_ref->get_symbol()->get_name().getString();
            if (val_map.find(var_name) != val_map.end())
            {
                ss << "(" << val_map.find(var_name)->second << ")";
            }
            else
            {
                ss << var_name;
            }
        }
        else if (auto value_exp = dynamic_cast<const SgValueExp *>(expr))
        {
            ss << value_exp->get_constant_folded_value_as_string();
        }
    }
    
    std::string
    expression_to_string_with_value_map(const SgExpression *expr, const std::map<std::string, std::string> &val_map)
    {
        std::stringstream ss;
        expression_to_string_with_value_map(ss, expr, val_map);
        return ss.str();
    }
    
    bool is_empty_block(SgBasicBlock *block)
    {
        if (block == nullptr) return true;
        SgStatementPtrList &stmt_list = block->get_statements();
        return stmt_list.empty();
    }
    
    std::map<std::string, int> real_member_func_set;
    std::map<std::string, int> real_relative_func_set;
    
    typedef std::pair<std::string, int> FUNC_PARANUM;
    
    void init_member_set()
    {
        real_member_func_set.clear();
        real_member_func_set.insert(FUNC_PARANUM("public: inline REAL &operator=(const class REAL &y);", 1));
    }
    
    void init_relative_set()
    {
        real_relative_func_set.clear();
        // +
        real_relative_func_set.insert(
                FUNC_PARANUM("public: friend inline class REAL operator+(const class REAL &x,const class REAL &y);",
                             2));
        real_relative_func_set.insert(
                FUNC_PARANUM("public: friend inline class REAL operator+(const int n,const class REAL &x);", 2));
        real_relative_func_set.insert(
                FUNC_PARANUM("public: friend inline class REAL operator+(const class REAL &x,const int n);", 2));
        real_relative_func_set.insert(
                FUNC_PARANUM("public: friend inline class REAL operator+(const double n,const class REAL &x);", 2));
        real_relative_func_set.insert(
                FUNC_PARANUM("public: friend inline class REAL operator+(const class REAL &x,const double n);", 2));
        // -
        real_relative_func_set.insert(
                FUNC_PARANUM("public: friend inline class REAL operator-(const class REAL &x,const class REAL &y);",
                             2));
        real_relative_func_set.insert(
                FUNC_PARANUM("public: friend inline class REAL operator-(const int n,const class REAL &x);", 2));
        real_relative_func_set.insert(
                FUNC_PARANUM("public: friend inline class REAL operator-(const class REAL &x,const int n);", 2));
        real_relative_func_set.insert(
                FUNC_PARANUM("public: friend inline class REAL operator-(const double n,const class REAL &x);", 2));
        real_relative_func_set.insert(
                FUNC_PARANUM("public: friend inline class REAL operator-(const class REAL &x,const double n);", 2));
        // *
        real_relative_func_set.insert(
                FUNC_PARANUM("public: friend inline class REAL operator*(const class REAL &x,const class REAL &y);",
                             2));
        real_relative_func_set.insert(
                FUNC_PARANUM("public: friend inline class REAL operator*(const int n,const class REAL &x);", 2));
        real_relative_func_set.insert(
                FUNC_PARANUM("public: friend inline class REAL operator*(const class REAL &x,const int n);", 2));
        real_relative_func_set.insert(
                FUNC_PARANUM("public: friend inline class REAL operator*(const double n,const class REAL &x);", 2));
        real_relative_func_set.insert(
                FUNC_PARANUM("public: friend inline class REAL operator*(const class REAL &x,const double n);", 2));
        // /
        real_relative_func_set.insert(
                FUNC_PARANUM("public: friend inline class REAL operator/(const class REAL &x,const class REAL &y);",
                             2));
        real_relative_func_set.insert(
                FUNC_PARANUM("public: friend inline class REAL operator/(const int n,const class REAL &x);", 2));
        real_relative_func_set.insert(
                FUNC_PARANUM("public: friend inline class REAL operator/(const class REAL &x,const int n);", 2));
        real_relative_func_set.insert(
                FUNC_PARANUM("public: friend inline class REAL operator/(const double n,const class REAL &x);", 2));
        real_relative_func_set.insert(
                FUNC_PARANUM("public: friend inline class REAL operator/(const class REAL &x,const double n);", 2));
        
        // +=, -=, *=, /=
        real_relative_func_set.insert(
                FUNC_PARANUM("public: friend inline class REAL &operator+=(class REAL &x,const class REAL &y);", 2));
        real_relative_func_set.insert(
                FUNC_PARANUM("public: friend inline class REAL &operator-=(class REAL &x,const class REAL &y);", 2));
        real_relative_func_set.insert(
                FUNC_PARANUM("public: friend inline class REAL &operator*=(class REAL &x,const class REAL &y);", 2));
        real_relative_func_set.insert(
                FUNC_PARANUM("public: friend inline class REAL &operator/=(class REAL &x,const class REAL &y);", 2));
    }
    
    SgDotExp *get_member_func_dotExp(SgFunctionCallExp *func_call)
    {
        auto suc_list = func_call->get_traversalSuccessorContainer();
        for (auto n : suc_list)
        {
            if (auto dot_exp = dynamic_cast<SgDotExp *>(n))
            {
                return dot_exp;
            }
        }
        return nullptr;
    }
    
    SgExpression *get_member_func_caller(SgFunctionCallExp *func_call)
    {
        SgDotExp *dot_exp = get_member_func_dotExp(func_call);
        if (dot_exp == nullptr) return nullptr;
        return dot_exp->get_lhs_operand();
    }
    
    SgMemberFunctionRefExp *get_member_func_refExp(SgFunctionCallExp *func_call)
    {
        SgDotExp *dot_exp = get_member_func_dotExp(func_call);
        if (dot_exp == nullptr) return nullptr;
        
        if (auto ref = dynamic_cast<SgMemberFunctionRefExp *>(dot_exp->get_rhs_operand()))
        {
            return ref;
        }
        auto suc_list = dot_exp->get_traversalSuccessorContainer();
        for (auto n : suc_list)
        {
            if (auto ref = dynamic_cast<SgMemberFunctionRefExp *>(n))
            {
                return ref;
            }
        }
        return nullptr;
    }
    
    SgFunctionRefExp *get_relative_func_refExp(SgFunctionCallExp *func_call)
    {
        auto suc_list = func_call->get_traversalSuccessorContainer();
        for (auto n : suc_list)
        {
            if (auto ref = dynamic_cast<SgFunctionRefExp *>(n))
            {
                return ref;
            }
        }
        return nullptr;
    }
    
    bool is_compound_assign_option(SgExpression *expr)
    {
        if (auto func_call = dynamic_cast<SgFunctionCallExp *>(expr))
        {
            std::string func_decl_str = func_call->getAssociatedFunctionDeclaration()->unparseToString();
            if (find_in_relative_func_set(func_decl_str))
            {
                const SgFunctionRefExp *ref_exp = get_relative_func_refExp(func_call);
                if (ref_exp->unparseToString() == "+=" ||
                    ref_exp->unparseToString() == "-=" ||
                    ref_exp->unparseToString() == "*=" ||
                    ref_exp->unparseToString() == "/=")
                {
                    return true;
                }
            }
        }
        else if (auto compound_op = dynamic_cast<SgCompoundAssignOp *>(expr))
        {
            return true;
        }
            // plusplus, minusminus put here temporarily
        else if (auto pp_op = dynamic_cast<SgPlusPlusOp *>(expr))
        {
            return true;
        }
        else if (auto mm_op = dynamic_cast<SgMinusMinusOp *>(expr))
        {
            return true;
        }
        return false;
    }
    
    std::string get_compound_assign_option_str(SgExpression *expr)
    {
        if (auto func_call = dynamic_cast<SgFunctionCallExp *>(expr))
        {
            std::string func_decl_str = func_call->getAssociatedFunctionDeclaration()->unparseToString();
            if (find_in_relative_func_set(func_decl_str))
            {
                SgFunctionRefExp *ref_exp = get_relative_func_refExp(func_call);
                std::string op = ref_exp->unparseToString();
                if (op == "+=" ||
                    op == "-=" ||
                    op == "*=" ||
                    op == "/=")
                {
                    SgExpressionPtrList expr_list = get_func_parameters(func_call);
                    return expr_list[0]->unparseToString() + op.substr(0, 1) + expr_list[1]->unparseToString();
                }
            }
        }
        else if (auto compound_op = dynamic_cast<SgCompoundAssignOp *>(expr))
        {
            std::string tmp = compound_op->unparseToString();
            auto iter = tmp.find('=');
            tmp = tmp.erase(iter, 1);
            return tmp;
        }
            // plusplus, minusminus are put here temporarily
        else if (auto pp_op = dynamic_cast<SgPlusPlusOp *>(expr))
        {
            SgExpression *ref = pp_op->get_operand_i();
            return ref->unparseToString() + " + 1";
        }
        else if (auto mm_op = dynamic_cast<SgMinusMinusOp *>(expr))
        {
            SgExpression *ref = mm_op->get_operand_i();
            return ref->unparseToString() + " - 1";
        }
        return expr->unparseToString();
    }
    
    template<class T>
    T *create_binary_option(SgExpression *lhs, SgExpression *rhs, SgType *type)
    {
        return new T(lhs, rhs, type);
    }
    
    SgBinaryOp *create_relative_binaryOp(SgExpression *expr)
    {
        if (auto func_call = dynamic_cast<SgFunctionCallExp *>(expr))
        {
            std::string func_decl_str = func_call->getAssociatedFunctionDeclaration()->unparseToString();
            if (find_in_relative_func_set(func_decl_str))
            {
                const SgFunctionRefExp *ref_exp = get_relative_func_refExp(func_call);
                SgExpressionPtrList expr_list = get_func_parameters(func_call);
                if (ref_exp->unparseToString() == "+=")
                {
                    return create_binary_option<SgAddOp>(expr_list[0], expr_list[1], ref_exp->get_type());
                }
                else if (ref_exp->unparseToString() == "-=")
                {
                    return create_binary_option<SgSubtractOp>(expr_list[0], expr_list[1], ref_exp->get_type());
                }
                else if (ref_exp->unparseToString() == "*=")
                {
                    return create_binary_option<SgMultiplyOp>(expr_list[0], expr_list[1], ref_exp->get_type());
                }
                else if (ref_exp->unparseToString() == "/=")
                {
                    return create_binary_option<SgDivideOp>(expr_list[0], expr_list[1], ref_exp->get_type());
                }
            }
        }
        else if (auto compound_op = dynamic_cast<SgCompoundAssignOp *>(expr))
        {
            if (compound_op->variantT() == V_SgPlusAssignOp)
            {
                return create_binary_option<SgAddOp>(compound_op->get_lhs_operand(), compound_op->get_rhs_operand(),
                                                     compound_op->get_type());
            }
            else if (compound_op->variantT() == V_SgMinusAssignOp)
            {
                return create_binary_option<SgSubtractOp>(compound_op->get_lhs_operand(),
                                                          compound_op->get_rhs_operand(), compound_op->get_type());
            }
        }
        return nullptr;
    }
}
