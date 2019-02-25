//
// Created by whj on 6/12/18.
//

#ifndef CODE_ANALYSE_DEBUG_H
#define CODE_ANALYSE_DEBUG_H

#include <iostream>
#include <string>
#include <sstream>
#include "rose.h"
#include "common.h"

namespace le
{
    using namespace std;
    
    void print_statement(SgStatement *s);
    
    void print_err_statement(SgStatement *stmt);
    
    void print_whole_node(SgNode * s, stringstream & ss, unsigned int
    tab_num = 0
    );
    
    void print_whole_node(SgNode * s);
    
    void print_warning_function_no_definition(SgFunctionDeclaration *decl);
}

#endif //CODE_ANALYSE_DEBUG_H
