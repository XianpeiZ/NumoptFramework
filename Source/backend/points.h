#ifndef POINTS_H
#define POINTS_H

#include <bitset>
#include <cstdint>
#include <fstream>
#include <random>
#include <iostream>
#include <iomanip>
#include <iterator>
#include <sstream>
#include <string>
#include <vector>


// 生成随机双精度浮点数
double generate_random_double(); 

// 生成[begin, end)之间随机的双精度浮点数
double generate_random_double(double begin, double end);

// 统计[begin, end)之间双精度浮点数个数
uint64_t double_num_between(double begin, double end); 

// 生成双精度浮点数d后面第offset个浮点数
double generate_double_by_offset(double d, uint64_t offset);

// 将一个长度为64的01字符串转为double
double binary2double(std::string str);

// 将一个double转换为64位长的01字符串
std::string double2binary(double d);

// 将一个长度为32位的01字符串转换为int
int binary2int(std::string str);

// 将一个int转换为32位长的01字符串
std::string int2binary(int i);

// 计算两个以二进制表示的双精度浮点数的相对误差
double relative_error(std::string irram_res, std::string herbie_res);

// Herbie定义的两个浮点数的误差
int herbie_error(std::string irram_res, std::string herbie_res);

// 对一个字符转以特定分隔符进行分割
template<typename Out>
void split(const std::string &s, char delim, Out result);

std::vector<std::string> split(const std::string &s, char delim);

#endif
