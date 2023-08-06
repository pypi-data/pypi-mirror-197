import os
import argparse
import json
from pathlib import Path

from template_generator import template

parser = argparse.ArgumentParser()
parser.add_argument("--input", type=str, default=None, help="输入资源")
parser.add_argument("--template_path", type=str, default=None, help="模板地址")
parser.add_argument("--params", type=str, default=None, help="参数")
parser.add_argument("--output_path", type=str, default=None, help="输出文件地址")
cmd_opts = parser.parse_args()

def main():
    input = cmd_opts.input
    if input == None:
        print("args fail!")
        return
    
    inputFiles = []
    template_path = None
    params = {}
    output_path = None
    try:
        if os.path.isfile(input):
            with open(input, 'r') as f:
                data = json.load(f)
        inputFiles = data["input"]
        template_path = data["template"]
        params = data["params"]
        output_path = data["output"]
    except:
        inputFiles = cmd_opts.input
        template_path = cmd_opts.template_path
        output_path = cmd_opts.output_path
    if inputFiles == None or template_path == None or output_path == None:
        print("args fail!")
        return
    
    template.executeTemplate(inputFiles, template_path, params, output_path)
        
if __name__ == '__main__':
        main()
