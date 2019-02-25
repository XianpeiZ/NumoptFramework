//
// Created by whj on 6/11/18.
//

#include <sstream>
#include <iostream>
#include "Program.h"

namespace le
{
    using namespace std;
    
    SgProject *project;
    set<string> src_file_set;
    vector<Program> program_list;
    
    void Program::run()
    {
        std::vector<SgNode *> decls = global->get_traversalSuccessorContainer();
        for (auto decl : decls)
        {
            if (!is_node_in_src(dynamic_cast<SgLocatedNode *>(decl)))
            {
                continue;
            }
            if (auto *funcDecl = dynamic_cast<SgFunctionDeclaration *>(decl))
            {
                Function f(funcDecl->get_name().getString(), funcDecl, name);
                add_function(f);
            }
        }
    }
    
    string Program::to_string()
    {
        stringstream ss;
        ss << "{" << endl;
        ss << "\"program_name\": " << "\"" << name << "\"" << endl;
        for (const auto &f : func_list)
        {
            ss << f.to_string() << endl;
        }
        ss << "}" << endl;
        return ss.str();
    }
    
    string Program::to_codes_block()
    {
        stringstream ss;
        ss << "{" << endl;
        ss << "\"program_name\": " << "\"" << name << "\"" << endl;
        for (const auto &f : func_list)
        {
            ss << f.to_code() << endl;
        }
        ss << "}" << endl;
        return ss.str();
    }
    
    void Program::to_klee_code_functions()
    {
        
        for (auto &f : func_list)
        {
            f.to_klee_code_functions();
            f.write_simple_json_file();
        }
    }
    
    void run_project(int argc, char **argv)
    {
        init_operator_str_map();
        init_member_set();
        init_relative_set();
        
        project = frontend(argc, argv);
        vector<SgNode *> nodes = project->get_fileList_ptr()->get_traversalSuccessorContainer();
        for (auto n : nodes)
        {
            if (auto src = dynamic_cast<SgSourceFile *>(n))
            {
                src_file_set.insert(src->getFileName());
                Program program(src->getFileName(), src->get_globalScope());
                program.run();
                program_list.push_back(program);
            }
        }
    
        for (auto &p : program_list)
        {
            cout << p.to_string();
        }
//
//        for (auto &p : program_list)
//        {
//            cout << p.to_codes_block();
//        }
    
        for (auto &p : program_list)
        {
            p.to_klee_code_functions();
        }
    }
}