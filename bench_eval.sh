TOP=`pwd`
# echo ${TOP}

cd ${TOP}/Source/backend
export LD_LIBRARY_PATH=${TOP}/Binary/iRRAM/lib:${LD_LIBRARY_PATH}
# echo ${LD_LIBRARY_PATH}
python3.6 main.py
python3.6 herbie_report.py
echo "Benchmark Optimization Complete"
