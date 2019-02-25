//
// Created by whj on 7/10/18.
//

#include "Code_Tree_Node.h"
#include "common.h"

namespace le
{
    const string enter_block = "{";
    const string leave_block = "}";
    
    volatile size_t node_index = 0;
    
    size_t get_node_index()
    {
        node_index++;
        return node_index;
    }
    
    bool Code_Tree_Node::is_leaf_node() const
    {
        return (if_node == nullptr && else_node == nullptr && next_tree_root == nullptr);
    }
    
    bool Code_Tree_Node::need_to_print_klee_out() const
    {
        return (if_node == nullptr && else_node == nullptr);
    }
    
    vector<shared_ptr<Code_Tree_Node>> Code_Tree_Node::get_all_leaves_ptr()
    {
        vector<shared_ptr<Code_Tree_Node>> ret;
        vector<shared_ptr<Code_Tree_Node>> stack;
        stack.push_back(shared_from_this());
        while (!stack.empty())
        {
            if (stack.back()->is_leaf_node())
            {
                ret.push_back(stack.back());
                stack.pop_back();
            }
            else
            {
                auto tmp = stack.back();
                stack.pop_back();
                if (tmp->if_node != nullptr)
                {
                    stack.push_back(tmp->if_node);
                }
                if (tmp->else_node != nullptr)
                {
                    stack.push_back(tmp->else_node);
                }
                if (tmp->next_tree_root != nullptr)
                {
                    stack.push_back(tmp->next_tree_root);
                }
            }
        }
        return ret;
    }
    
    vector<shared_ptr<Code_Tree_Node>> Code_Tree_Node::get_all_no_end_leaves_ptr()
    {
        vector<shared_ptr<Code_Tree_Node>> ret;
        vector<shared_ptr<Code_Tree_Node>> stack;
        stack.push_back(shared_from_this());
        while (!stack.empty())
        {
            if (stack.back()->is_leaf_node() && stack.back()->can_add_stmt())
            {
                ret.push_back(stack.back());
                stack.pop_back();
            }
            else
            {
                auto tmp = stack.back();
                stack.pop_back();
                if (tmp->if_node != nullptr)
                {
                    stack.push_back(tmp->if_node);
                }
                if (tmp->else_node != nullptr)
                {
                    stack.push_back(tmp->else_node);
                }
                if (tmp->next_tree_root != nullptr)
                {
                    stack.push_back(tmp->next_tree_root);
                }
            }
        }
        return ret;
    }
    
    void Code_Tree_Node::initial_if_else_branch(SgExpression *condition)
    {
        assert(next_tree_root == nullptr && loop == nullptr);
        this->condition = condition;
        // input variables table and left value table are inherited from father
        if_node = make_shared<Code_Tree_Node>();
        if_node->input_vars = input_vars + declared_vars;
        if_node->lvars = this->lvars;
        else_node = make_shared<Code_Tree_Node>();
        else_node->input_vars = input_vars + declared_vars;
        else_node->lvars = this->lvars;
    }
    
    bool Code_Tree_Node::has_if_else_branches() const
    {
        return (condition != nullptr && if_node != nullptr && else_node != nullptr);
    }
    
    void Code_Tree_Node::initial_make_symbolics(const VariableTable &input)
    {
        input_vars = input;
        for (auto &v : input_vars.T)
        {
            add_str(v.second.to_klee_make_symbolic());
        }
    }
    
    bool Code_Tree_Node::end_with_loop() const
    {
        return (loop != nullptr && next_tree_root != nullptr);
    }
    
    Code_Tree_Node::Code_Tree_Node() :
            has_returned(false),
            has_broken(false),
            has_continued(false),
            if_node(nullptr),
            else_node(nullptr),
            condition(nullptr),
            next_tree_root(nullptr),
            loop(nullptr)
    {
        ID = get_node_index();
    }
    
    void Code_Tree_Node::add_stmt(const SgStatement *stmt)
    {
        if (!can_add_stmt()) return;
        if (next_tree_root != nullptr)
        {
            next_tree_root->add_stmt(stmt);
        }
        else if (condition != nullptr)
        {
            if_node->add_stmt(stmt);
            else_node->add_stmt(stmt);
        }
        else
        {
            code_lines.push_back(stmt->unparseToString());
        }
    }
    
    void Code_Tree_Node::add_str_4_forloop_increment(const string &str)
    {
        if (has_returned || has_broken) return;
        if (next_tree_root != nullptr)
        {
            next_tree_root->add_str_4_forloop_increment(str);
        }
        else if (condition != nullptr)
        {
            if_node->add_str_4_forloop_increment(str);
            else_node->add_str_4_forloop_increment(str);
        }
        else
        {
            code_lines.push_back(str);
        }
    }
    
    void Code_Tree_Node::add_str(const string &str)
    {
        if (!can_add_stmt()) return;
        if (next_tree_root != nullptr)
        {
            next_tree_root->add_str(str);
        }
        else if (condition != nullptr)
        {
            if_node->add_str(str);
            else_node->add_str(str);
        }
        else
        {
            code_lines.push_back(str);
        }
    }
    
    void Code_Tree_Node::set_returned()
    {
        if (!can_add_stmt()) return;
        if (next_tree_root != nullptr)
        {
            next_tree_root->set_returned();
        }
        else if (condition != nullptr)
        {
            if_node->set_returned();
            else_node->set_returned();
        }
        else
        {
//            add_str("return;");
            has_returned = true;
        }
    }
    
    void Code_Tree_Node::set_broke()
    {
        if (!can_add_stmt()) return;
        if (next_tree_root != nullptr)
        {
            next_tree_root->set_broke();
        }
        else if (condition != nullptr)
        {
            if_node->set_broke();
            else_node->set_broke();
        }
        else
        {
            add_str("// break;");
            add_str("int __break__ = 0;");
            add_str(generate_klee_output_stmt("__break__", "__break__"));
//            add_str("return;");
            has_broken = true;
        }
    }
    
    void Code_Tree_Node::set_continued()
    {
        if (!can_add_stmt()) return;
        if (next_tree_root != nullptr)
        {
            next_tree_root->set_continued();
        }
        else if (condition != nullptr)
        {
            if_node->set_continued();
            else_node->set_continued();
        }
        else
        {
            add_str("// continue;");
            add_str("int __continue__ = 0;");
            add_str(generate_klee_output_stmt("__continue__", "__continue__"));
//            add_str("return;");
            has_continued = true;
        }
    }
    
    void Code_Tree_Node::handle_block_statement(SgBasicBlock *block)
    {
        SgStatementPtrList &stmt_list = block->get_statements();
        for (auto s : stmt_list)
        {
            handle_statement(s);
        }
    }
    
    void Code_Tree_Node::handle_statement(SgStatement *stmt)
    {
        cout << stmt->unparseToString() << ", " << stmt->class_name() << endl;
        if (auto s = dynamic_cast<SgBasicBlock *>(stmt))
        {
            handle_block_statement(s);
        }
        else if (auto s = dynamic_cast<SgForStatement *>(stmt))
        {
            handle_for_statement(s);
        }
        else if (auto s = dynamic_cast<SgWhileStmt *>(stmt))
        {
            handle_while_statement(s);
        }
//        else if (auto s = dynamic_cast<SgDoWhileStmt *>(stmt))
//        {
//            handle_dowhile_statement(s);
//        }
        else if (auto s = dynamic_cast<SgIfStmt *>(stmt))
        {
            handle_if_statement(s);
        }
        else if (auto s = dynamic_cast<SgReturnStmt *>(stmt))
        {
            handle_return_statement(s);
        }
        else if (auto s = dynamic_cast<SgBreakStmt *>(stmt))
        {
            handle_break_statement(s);
        }
        else if (auto s = dynamic_cast<SgContinueStmt *>(stmt))
        {
            handle_continue_statement(s);
        }
        else
        {
            add_stmt(stmt);
            if (auto s = dynamic_cast<SgVariableDeclaration *>(stmt))
            {
                handle_var_declaration(s);
            }
            else if (auto s = dynamic_cast<SgExprStatement *>(stmt))
            {
                SgExpression *expr = s->get_expression();
                handle_expression(expr);
            }
        }
    }
    
    void Code_Tree_Node::handle_return_statement(SgReturnStmt *return_stmt)
    {
        SgExpression *expr = return_stmt->get_expression();
        if (expr != nullptr)
        {
            // declare __return__ as the expression of return statement
            string declare_return_value = "class iRRAM::REAL __return__ = ";
            declare_return_value += expr->unparseToString() + ";";
            add_str(declare_return_value);
            // then set __return__ as klee_output
            add_str("klee_output(\"__return__\", __return__.value);");
        }
        set_returned();
    }
    
    void Code_Tree_Node::handle_break_statement(SgBreakStmt *break_stmt)
    {
        set_broke();
    }
    
    void Code_Tree_Node::handle_continue_statement(SgContinueStmt *continue_stmt)
    {
        set_continued();
    }
    
    void Code_Tree_Node::handle_if_statement(SgIfStmt *if_stmt)
    {
        if (!can_add_stmt()) return;
        SgStatement *condition_stmt = if_stmt->get_conditional();
        if (auto *expr_stmt = dynamic_cast<SgExprStatement *>(condition_stmt))
        {
            SgExpression *condition = expr_stmt->get_expression();
            auto leaf_nodes = this->get_all_no_end_leaves_ptr();
            for (auto ptr : leaf_nodes)
            {
                ptr->initial_if_else_branch(condition);
                
                string true_stmt = string("if(") + condition->unparseToString() + ")";
                
                auto true_body = dynamic_cast<SgBasicBlock *>(if_stmt->get_true_body());
                auto false_body = dynamic_cast<SgBasicBlock *>(if_stmt->get_false_body());
                auto else_if_body = dynamic_cast<SgIfStmt *>(if_stmt->get_false_body());
                
                if (true_body != nullptr)
                {
                    ptr->if_node->handle_block_statement(true_body);
                }
                
                if (else_if_body != nullptr)
                {
                    ptr->else_node->handle_statement(else_if_body);
                }
                else if (false_body != nullptr)
                {
                    ptr->else_node->handle_block_statement(false_body);
                }
            }
        }
    }
    
    void Code_Tree_Node::initial_next_root_node(shared_ptr<Loop> _l)
    {
        assert(condition == nullptr && if_node == nullptr && else_node == nullptr);
        this->loop = _l;
        this->next_tree_root = make_shared<Code_Tree_Node>();
        this->next_tree_root->initial_make_symbolics(input_vars + declared_vars);
        // left value table is a new empty table
    }
    
    void Code_Tree_Node::handle_for_statement(SgForStatement *for_stmt)
    {
        auto leaf_nodes = get_all_no_end_leaves_ptr();
        shared_ptr<Loop> tmp_loop = make_shared<Loop>();
        tmp_loop->init_for_initializer(for_stmt);
        tmp_loop->initial_out_loop_variables(input_vars + declared_vars);
        tmp_loop->init_for_statement(for_stmt);
        for (auto &ptr : leaf_nodes)
        {
            ptr->initial_next_root_node(tmp_loop);
        }
    }
    
    void Code_Tree_Node::handle_while_statement(SgWhileStmt *while_stmt)
    {
        auto leaf_nodes = get_all_no_end_leaves_ptr();
        shared_ptr<Loop> tmp_loop = make_shared<Loop>();
        tmp_loop->initial_out_loop_variables(input_vars + declared_vars);
        tmp_loop->init_while_statement(while_stmt);
        for (auto &ptr : leaf_nodes)
        {
            ptr->initial_next_root_node(tmp_loop);
        }
    }
    
    void Code_Tree_Node::add_left_value(const le::Variable &var)
    {
        if (lvars.has_variable(var.var_name) && is_leaf_node()) return;
        auto no_ends = get_all_no_end_leaves_ptr();
        for (auto &ptr : no_ends)
        {
            ptr->lvars.add_variable(var);
        }
        lvars.add_variable(var);
//        this->add_str(var.to_klee_out_string());
    }
    
    void Code_Tree_Node::add_left_value(const string &var_name)
    {
        if (!can_add_stmt()) return;
        if (this->input_vars.has_variable(var_name))
        {
            this->add_left_value(input_vars.find(var_name));
            return;
        }
        if (this->declared_vars.has_variable(var_name))
        {
            this->add_left_value(declared_vars.find(var_name));
            return;
        }
        assert(false);
    }
    
    void Code_Tree_Node::add_declaretion(const le::Variable &var)
    {
        assert(!input_vars.has_variable(var.var_name));
        assert(!lvars.has_variable(var.var_name));
        assert(!declared_vars.has_variable(var.var_name));
        // use declared_vars as the record of the usable variables table
        // we just create a loop for all branches, rather than create a loop for every branch that can execute the loop
        // if a node can execute the loop, we assign the loop_ptr to the node's loop_ptr
        this->declared_vars.add_variable(var);
        if (has_if_else_branches())
        {
            if_node->add_declaretion(var);
            else_node->add_declaretion(var);
        }
        else if (end_with_loop())
        {
            next_tree_root->add_declaretion(var);
        }
    }
    
    void Code_Tree_Node::handle_var_declaration(SgVariableDeclaration *decl)
    {
        SgInitializedNamePtrList &list = decl->get_variables();
        for (SgInitializedName *n : list)
        {
            SgType *type = n->get_type();
            string var_name = n->get_name();
            // check type must be iRRAM::REAL, do no process on basic type now!
//            if(type->get_mangled() != REAL_MANGLED)
//                return;
            if (auto initializer = dynamic_cast<SgConstructorInitializer *>(n->get_initptr()))
            {
                // for iRRAM::REAL type, initializer with constructor, rather than SgAssignInitializer
                // REAL constructor with 1 parameter
                Variable var(var_name, type, nullptr);
                this->add_declaretion(var);
                this->add_left_value(var);
            }
            else if (auto initializer = dynamic_cast<SgAssignInitializer *>(n->get_initptr()))
            {
                // basic type initializer
                Variable var(var_name, type, initializer->get_operand());
                this->add_declaretion(var);
                this->add_left_value(var);
            }
            else
            {
                // no assign expression. do not regard as left value
                Variable var(var_name, type);
                this->add_declaretion(var);
            }
        }
    }
    
    void Code_Tree_Node::handle_expression(SgExpression *expr)
    {
        if (auto func_call = dynamic_cast<SgFunctionCallExp *>(expr))
        {
            string func_decl_str = func_call->getAssociatedFunctionDeclaration()->unparseToString();
            if (find_in_member_func_set(func_decl_str))
            {
                SgExpressionPtrList expr_list = get_func_parameters(func_call);
                SgMemberFunctionRefExp *ref_exp = get_member_func_refExp(func_call);
                if (ref_exp->unparseToString() == "=")
                {// now only has assign value operator= in member function set
                    SgExpression *caller = get_member_func_caller(func_call);
                    this->add_left_value(caller->unparseToString());
                    handle_expression(expr_list[0]);
                }
            }
            else if (find_in_relative_func_set(func_decl_str))
            {
                SgExpressionPtrList expr_list = get_func_parameters(func_call);
                SgFunctionRefExp *ref_exp = get_relative_func_refExp(func_call);
                if (ref_exp->unparseToString() == "+" ||
                    ref_exp->unparseToString() == "-" ||
                    ref_exp->unparseToString() == "*" ||
                    ref_exp->unparseToString() == "/")
                {
                    for (auto e : expr_list)
                    {
                        handle_expression(e);
                    }
                }
                else if (ref_exp->unparseToString() == "+=" ||
                         ref_exp->unparseToString() == "-=" ||
                         ref_exp->unparseToString() == "*=" ||
                         ref_exp->unparseToString() == "/=")
                {
                    this->add_left_value(expr_list[0]->unparseToString());
                    handle_expression(expr_list[1]);
                }
            }
            else
            {
                // unknown function call
                // do nothing
            }
        }
        else
        {
            if (auto assign_op = dynamic_cast<SgAssignOp *>(expr))
            {
                SgExpression *ref = assign_op->get_lhs_operand();
                SgExpression *value = assign_op->get_rhs_operand();
                add_left_value(ref->unparseToString());
                handle_expression(value);
            }
            else if (auto compound_op = dynamic_cast<SgCompoundAssignOp *>(expr))
            {
                SgExpression *ref = compound_op->get_lhs_operand();
                add_left_value(ref->unparseToString());
                handle_expression(compound_op->get_rhs_operand());
            }
            else if (auto pp_op = dynamic_cast<SgPlusPlusOp *>(expr))
            {
                SgExpression *ref = pp_op->get_operand_i();
                add_left_value(ref->unparseToString());
                handle_expression(ref);
            }
            else if (auto mm_op = dynamic_cast<SgMinusMinusOp *>(expr))
            {
                SgExpression *ref = pp_op->get_operand_i();
                add_left_value(ref->unparseToString());
                handle_expression(ref);
            }
        }
    }
    
    void Code_Tree_Node::handle_forloop_increment(SgExpression *expr, VariableTable &forloop_initializer)
    {
        this->add_str_4_forloop_increment(expr->unparseToString() + ";");
    }
    
    void Code_Tree_Node::write_code_to_ss(stringstream &ss, unsigned int tab_num) const
    {
        string tab1 = generate_tab(tab_num);
        ss << tab1 << enter_block << endl;
        string tab2 = generate_tab(tab_num + 1);
        for (const auto &stmt : code_lines)
        {
            ss << tab2 << stmt << endl;
        }
        if (need_to_print_klee_out())
        {
            ss << lvars.to_make_real_klee_output_code(tab_num + 1);
        }
        if (condition != nullptr)
        {
            ss << tab2 << "if(" << condition->unparseToString() << ")" << endl;
            if_node->write_code_to_ss(ss, tab_num + 1);
            ss << tab2 << "else" << endl;
            else_node->write_code_to_ss(ss, tab_num + 1);
        }
        if (next_tree_root != nullptr)
        {
            string loop_name = loop->get_loop_func_name();
            ss << tab2 << "int " << loop_name << " = 0;" << endl;
            ss << tab2 << generate_klee_output_stmt(loop_name, loop_name) << endl;
            string node_name = next_tree_root->get_node_func_name();
            ss << tab2 << "int " << node_name << " = 0;" << endl;
            ss << tab2 << generate_klee_output_stmt(node_name, node_name) << endl;
        }
        if (!can_add_stmt())
        {
            ss << tab2 << "return;" << endl;
        }
        ss << tab1 << leave_block << endl;
    }
    
    void Code_Tree_Node::write_node_function_to_ss(stringstream &ss) const
    {
        ss << "void " << get_node_func_name() << input_vars.to_parameterlist() << endl;
        write_code_to_ss(ss, 0);
        ss << endl;
    }
    
    void Code_Tree_Node::write_node_correspond_main_func(stringstream &ss) const
    {
        string tab = generate_tab(1);
        ss << "int main()" << endl;
        ss << "{" << endl;
        ss << input_vars.to_declaration_code(1);
        ss << tab << get_node_func_name() << input_vars.to_variables_reference_list() << ";" << endl;
        ss << tab << "return 0;" << endl;
        ss << "}" << endl;
    }
    
    string Code_Tree_Node::get_node_func_name() const
    {
        stringstream ss;
        ss << "node" << ID;
        return ss.str();
    }
    
    void Code_Tree_Node::get_all_nodes_need_to_be_printed(set<shared_ptr<Code_Tree_Node>> &nodes,
                                                          set<shared_ptr<Loop>> &loops) const
    {
        if (this->is_leaf_node()) return;
        if (this->next_tree_root != nullptr)
        {
            nodes.insert(this->next_tree_root);
            loops.insert(this->loop);
            this->next_tree_root->get_all_nodes_need_to_be_printed(nodes, loops);
        }
        if (this->condition != nullptr)
        {
            this->if_node->get_all_nodes_need_to_be_printed(nodes, loops);
            this->else_node->get_all_nodes_need_to_be_printed(nodes, loops);
        }
    }
    
    VariableTable Code_Tree_Node::get_all_declared_variables() const
    {
        VariableTable ret = declared_vars;
        if (has_if_else_branches())
        {
            ret = ret + if_node->get_all_declared_variables();
            ret = ret + else_node->get_all_declared_variables();
        }
        else if (end_with_loop())
        {
            ret = ret + next_tree_root->get_all_declared_variables();
        }
        return ret;
    }
    
    Code_Tree_Node::~Code_Tree_Node()
    {
    
    }
    
}