//
// Created by whj on 6/11/18.
//

#ifndef CODE_ANALYSE_PROGRAM_H
#define CODE_ANALYSE_PROGRAM_H

#include <vector>
#include <iostream>
#include <string>
#include <set>
#include "rose.h"
#include "Function.h"
#include "common.h"

namespace le
{
    
    using namespace std;
    
    class Program
    {
    public:
        string name;
        vector<Function> func_list;
        SgGlobal *global;
        
        Program(const string &_name, SgGlobal *_global) : name(_name), global(_global)
        {}
        
        void run();
        
        void add_function(Function &f)
        {
            func_list.push_back(f);
        }
        
        string to_string();
        
        string to_codes_block();
        
        void to_klee_code_functions();
    };
    
    
    extern SgProject *project;
    extern set<string> src_file_set;
    extern vector<Program> program_list;
    
    void run_project(int, char **);
    
    inline bool is_node_in_src(SgLocatedNode *node)
    {
        if (node == nullptr)
        {
            return false;
        }
        return src_file_set.find(node->getFilenameString()) != src_file_set.end();
    }
}


#endif //CODE_ANALYSE_PROGRAM_H
