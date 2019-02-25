#include "points.h"

// 生成随机双精度浮点数
double generate_random_double() {

    std::random_device rd;
    std::default_random_engine generator(rd());    
    std::bernoulli_distribution distribution(0.5);

    uint64_t n = 0;
    for (uint64_t i = 0; i < 64; i++) {
        bool b = distribution(generator);
        if (!b) {
            n = n & ~((uint64_t)1 << i);
        }
        else {
            n = n | ((uint64_t)1 << i);
        }
    }

    double d = *(double *)(&n);

    if (d == d) {
        return d;
    }
    return generate_random_double(); 
}

// 统计[begin, end)之间双精度浮点数个数
uint64_t double_num_between(double begin, double end) {

    if (end == begin) return 0;
    if (end < begin) return double_num_between(end, begin);

    //uint64_t u_begin = *(uint64_t *)(&begin); 
    uint64_t u_end = *(uint64_t *)(&end);

    //uint64_t sign_mask = uint64_t(1) << 63;
    uint64_t frac_mask = 0;
    for (int i = 0; i < 52; ++i) {
        frac_mask |= uint64_t(1) << i; 
    }
    uint64_t exp_mask = 0;
    for (int i = 52; i < 63; ++i) {
        exp_mask |= uint64_t(1) << i;
    }

    //std::cout << "sign mask:" << std::bitset<64>(sign_mask) << std::endl;
    //std::cout << "exp  mask:" << std::bitset<64>(exp_mask) << std::endl;
    //std::cout << "frac mask:" << std::bitset<64>(frac_mask) << std::endl;

    //std::cout << std::bitset<64>(u_begin) << std::endl;
    //std::cout << std::bitset<64>(u_end) << std::endl;

    if (begin  == 0.0) {
        return (u_end&exp_mask)+(u_end&frac_mask); 
    }
    if (begin < 0 && 0 < end) {
        return double_num_between(0.0, -begin)+double_num_between(0.0, end); 
    }
    if (0 < begin) {
        return double_num_between(0.0, end)-double_num_between(0.0, begin);
    }
    if (end <= 0) {
        return double_num_between(0.0, -begin)-double_num_between(0.0, -end); 
    }
    return  std::numeric_limits<std::uint64_t>::max()-1;
}

// 生成双精度浮点数d后面第offset个浮点数
double generate_double_by_offset(double d, uint64_t offset) {
    
    if (d == 0.0) {
        return *(double *)(&offset);
    }
    
   if (d > 0) {
        return generate_double_by_offset(0.0, offset+double_num_between(0.0, d));
   }

   if (d < 0) {
        if (offset >= double_num_between(d, 0.0)) {
            return generate_double_by_offset(0.0, offset-double_num_between(d, 0.0));
        } else {
            return -generate_double_by_offset(0.0,double_num_between(0.0, -d)-offset);
        }
   }
    return 0;
}

// 生成[begin, end)之间随机的双精度浮点数
double generate_random_double(double begin, double end) {

    if (begin >= end) {
        std::cerr << "Can't sample a double between [" <<  begin << ", " << end <<  "]" << std::endl; 
        return 0;
    }

    uint64_t distance = double_num_between(begin, end);
    std::random_device rd;   
    std::mt19937_64 generator(rd());
    std::uniform_int_distribution<uint64_t> distribution(0, distance);

    uint64_t offset = distribution(generator);
    return generate_double_by_offset(begin, offset);      
}

// 将一个长度为64的01字符串转为double
double binary2double(std::string str) {
    std::bitset<64> bitset64(str);
    uint64_t u = bitset64.to_ulong();
    return *(double *)(&u);
}

// 将一个double转换为64位长的01字符串
std::string double2binary(double d) {
    uint64_t u = *(uint64_t *)(&d);
    std::bitset<64> bitset64(u);
    return bitset64.to_string();
}

// 将一个长度为32位的01字符串转换为int
int binary2int(std::string str) {
    std::bitset<32> bitset32(str);
    return (int)(bitset32.to_ulong());
}

// 将一个int转换为32位长的01字符串
std::string int2binary(int i) {
    uint32_t u = *(uint32_t *)(&i);
    std::bitset<32> bitset32(u);
    return bitset32.to_string();
}

// 计算两个以二进制表示的双精度浮点数的相对误差
double relative_error(std::string irram_res, std::string herbie_res) {
    double irram = binary2double(irram_res);
    double herbie = binary2double(herbie_res);
    if (std::isnan(herbie) || std::isnan(irram)) {
        return std::numeric_limits<double>::infinity();
    }
    if (irram == 0) {
        if (herbie == 0) {
            return 0;
        }
        return std::numeric_limits<double>::infinity();
    }
    return std::abs((irram-herbie)/irram);
}

int log2_64(uint64_t value) {
    std::bitset<64> b(value); 
    std::string s = b.to_string();
    for (unsigned i = 0; i < b.size(); ++i) {
        if (s[i] == '1') {
            return 63 - i; 
        }
    }
    return 0;
}

// Herbie定义的两个浮点数的误差
int herbie_error(std::string irram_res, std::string herbie_res) {
    uint64_t u = double_num_between(binary2double(irram_res), binary2double(herbie_res));
    return log2_64(u+1);
}

// 对一个字符转以特定分隔符进行分割
template<typename Out>
void split(const std::string &s, char delim, Out result) {
    std::stringstream ss(s);
    std::string item;
    while (std::getline(ss, item, delim)) {
        *(result++) = item;
    }
}

std::vector<std::string> split(const std::string &s, char delim) {
    std::vector<std::string> elems;
    split(s, delim, std::back_inserter(elems));
    return elems;
}



