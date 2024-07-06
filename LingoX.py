import sys
import re

# 模拟input()函数，接收用户输入
def simulate_input(prompt):
    return input(prompt)

# 模拟log输出函数，输出内容
def simulate_log(message):
    print(message)

# 解析.x文件并执行相应操作
def execute_lingo_x(filename):
    variables = {}  # 用于存储变量名和值的字典
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for idx, line in enumerate(lines):
                # 匹配并处理input函数调用
                if 'input(' in line:
                    prompt = re.search(r'input\("([^"]+)"\)', line).group(1)
                    user_input = simulate_input(prompt)
                    line = line.replace(f'input("{prompt}")', f'"{user_input}"')

                # 匹配并处理log函数调用
                log_match = re.search(r'log\("([^"]+)"\)', line)
                if log_match:
                    content = log_match.group(1)
                    # 替换表达式中的变量引用为实际值
                    content = re.sub(r'{([^}]*)}', lambda x: str(variables.get(x.group(1).strip(), x.group(0))), content)
                    simulate_log(content)
                    continue  # 继续下一行的处理

                # 处理变量赋值语句和表达式计算
                if '=' in line:
                    var_name, expr = line.split('=')
                    var_name = var_name.strip()
                    # 去掉值的外层大括号
                    var_value = expr.strip().replace('{', '').replace('}', '')
                    if var_value.startswith('"') and var_value.endswith('"'):
                        var_value = var_value[1:-1]
                    else:
                        # 替换变量引用为实际值
                        var_value = re.sub(r'{([^}]*)}', lambda x: str(variables.get(x.group(1).strip(), x.group(0))), var_value)
                        # 计算表达式中的加法运算
                        try:
                            var_value = eval(var_value, {}, variables)  # 使用eval函数计算表达式结果，传入当前变量字典
                        except Exception as e:
                            print(f"Error evaluating expression in line {idx + 1}: {e}")
                            continue

                    # 将变量名和值存入字典
                    variables[var_name] = var_value

    except FileNotFoundError:
        print(f"Error: Unable to open file {filename}")

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != '-run':
        print("Usage: python LingoX.py -run \"filename.x\"")
        sys.exit(1)

    filename = sys.argv[2]
    execute_lingo_x(filename)
