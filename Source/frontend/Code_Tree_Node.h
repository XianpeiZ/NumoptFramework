//
// Created by whj on 7/10/18.
//

#ifndef CODE_ANALYSE_CODE_TREE_NODE_H
#define CODE_ANALYSE_CODE_TREE_NODE_H

#include <vector>
#include <set>
#include <string>
#include <sstream>
#include <iostream>
#include "rose.h"
#include "Loop.h"
#include "Variable.h"

namespace le
{
    using namespace std;
    
    class Loop;
    
    class Code_Tree_Node : public enable_shared_from_this<Code_Tree_Node>
    {
        vector<shared_ptr<Code_Tree_Node>> get_all_leaves_ptr();
    
        vector<shared_ptr<Code_Tree_Node>> get_all_no_end_leaves_ptr();
        
        bool is_leaf_node() const;
    
        bool need_to_print_klee_out() const;
    
        void add_left_value(const Variable &var);
    
        void add_left_value(const string &var_name);
    
        void add_declaretion(const Variable &var);
    
    public:
        size_t ID;
        VariableTable input_vars;
        VariableTable lvars; // store variable that be used as left value
        VariableTable declared_vars;
        vector<string> code_lines;
        bool has_returned;
        bool has_broken;
        bool has_continued;
        shared_ptr<Code_Tree_Node> if_node;
        shared_ptr<Code_Tree_Node> else_node;
        shared_ptr<Code_Tree_Node> next_tree_root;
        shared_ptr<Loop> loop;
        SgExpression *condition;
        
        Code_Tree_Node();
    
        void initial_if_else_branch(SgExpression *condition);
    
        bool has_if_else_branches() const;
    
        void initial_next_root_node(shared_ptr<Loop> _l);
    
        bool end_with_loop() const;
    
        void initial_make_symbolics(const VariableTable &input);
        
        void add_stmt(const SgStatement *stmt);
    
        void add_str_4_forloop_increment(const string &str);
        
        void add_str(const string &str);
        
        void set_returned();
    
        void set_broke();
    
        void set_continued();
        
        void handle_statement(SgStatement *stmt);
        
        void handle_block_statement(SgBasicBlock *block);
        
        void handle_if_statement(SgIfStmt *if_stmt);
        
        void handle_return_statement(SgReturnStmt *return_stmt);
    
        void handle_break_statement(SgBreakStmt *break_stmt);
    
        void handle_continue_statement(SgContinueStmt *continue_stmt);
    
        void handle_for_statement(SgForStatement *for_stmt);
    
        void handle_while_statement(SgWhileStmt *while_stmt);
    
        void handle_var_declaration(SgVariableDeclaration *decl);
    
        void handle_expression(SgExpression *expr);
    
        void handle_forloop_increment(SgExpression *expr, VariableTable &forloop_initializer);
        
        void write_code_to_ss(stringstream &ss, unsigned int tab_num) const;
    
        void write_node_function_to_ss(stringstream &ss) const;
    
        void write_node_correspond_main_func(stringstream &ss) const;
    
        string get_node_func_name() const;
    
        void
        get_all_nodes_need_to_be_printed(set<shared_ptr<Code_Tree_Node>> &nodes, set<shared_ptr<Loop>> &loops) const;
        
        bool can_add_stmt() const
        { return !has_returned && !has_broken && !has_continued; }
    
        VariableTable get_all_declared_variables() const;
        
        ~Code_Tree_Node();
    
        friend class Loop;
    };
}

#endif //CODE_ANALYSE_CODE_TREE_NODE_H
