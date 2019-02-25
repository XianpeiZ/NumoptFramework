//
// Created by whj on 6/13/18.
//

#include "debug.h"

namespace le
{
    using namespace std;
    
    void print_statement(SgStatement *s)
    {
        cout << s->unparseToString() << endl;
    }
    
    void print_err_statement(SgStatement *stmt)
    {
        cout << "Unsupported statement: " << endl;
        cout << stmt->class_name() << " : " << stmt->unparseToString() << endl;
    }
    
    void print_whole_node(SgNode * s, stringstream & ss, unsigned int
    tab_num)
{
    if(s == nullptr) return;
    auto list = s->get_traversalSuccessorContainer();
    ss <<
    generate_tab(tab_num);
    ss << s->
    
    unparseToString()
    
    << " : " << s->
    
    class_name()
    
    <<
    endl;
    for(
    auto i
    : list)
{
    print_whole_node(i, ss, tab_num
    + 1);
}
}

void print_whole_node(SgNode * s)
{
    stringstream ss;
    print_whole_node(s, ss);
    cout << ss.str() << endl;
}

void print_warning_function_no_definition(SgFunctionDeclaration *decl)
{
    cout << decl->unparseToString() << " has no definition block!" << endl;
}

}
