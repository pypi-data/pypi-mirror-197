# -*- coding: utf-8 -*-
import json
import requests
import re
from time import time, sleep
import random
import datetime
import numpy as np
import sys
from os.path import dirname, abspath

project_path = dirname(abspath(__file__))
sys.path.append(project_path+r'/qasmtoqcis')


from qasm_to_qcis import QasmToQcis


class QcisCheck():

    def __init__(self, circuit=None):
        self.circuit = circuit

    def circuit_regular(self):
        regular_exp_map = {
            'X': r'^X(?:\s(?:Q(?:[1-5][0-9]|60|[1-9]))){1}$',
            'Y': r'^Y(?:\s(?:Q(?:[1-5][0-9]|60|[1-9]))){1}$',
            'Z': r'^Z(?:\s(?:Q(?:[1-5][0-9]|60|[1-9]))){1}$',
            'X2P': r'^X2P(?:\s+(?:Q(?:[1-5][0-9]|60|[1-9]))){1}$',
            'X2M': r'^X2M(?:\s+(?:Q(?:[1-5][0-9]|60|[1-9]))){1}$',
            'Y2P': r'^Y2P(?:\s+(?:Q(?:[1-5][0-9]|60|[1-9]))){1}$',
            'Y2M': r'^Y2M(?:\s+(?:Q(?:[1-5][0-9]|60|[1-9]))){1}$',
            'H': r'^H(?:\s+(?:Q(?:[1-5][0-9]|60|[1-9]))){1}$',
            'S': r'^S(?:\s+(?:Q(?:[1-5][0-9]|60|[1-9]))){1}$',
            'SD': r'^SD(?:\s+(?:Q(?:[1-5][0-9]|60|[1-9]))){1}$',
            'T': r'^T(?:\s+(?:Q(?:[1-5][0-9]|60|[1-9]))){1}$',
            'TD': r'^TD(?:\s+(?:Q(?:[1-5][0-9]|60|[1-9]))){1}$',
            'CZ': r'^CZ(?:\s+(?:Q(?:[1-5][0-9]|60|[1-9]))){2}$',
            'RX': r'^RX\s(?:Q(?:[1-5][0-9]|60|[1-9]))\s([+-]?([0-9]*[.])?([0-9]+|[0-9]+[E][+-]?[0-9]+))$',
            'RY': r'^RY\s(?:Q(?:[1-5][0-9]|60|[1-9]))\s([+-]?([0-9]*[.])?([0-9]+|[0-9]+[E][+-]?[0-9]+))$',
            'RZ': r'^RZ\s(?:Q(?:[1-5][0-9]|60|[1-9]))\s([+-]?([0-9]*[.])?([0-9]+|[0-9]+[E][+-]?[0-9]+))$',
            'RXY': r'^RXY\s(?:Q(?:[1-5][0-9]|60|[1-9]))\s([+-]?([0-9]*[.])?([0-9]+|[0-9]+[E][+-]?[0-9]+))\s([+-]?([0-9]*[.])?([0-9]+|[0-9]+[E][+-]?[0-9]+))$',
            'M': r'^M(?:\s+(?:Q(?:[1-5][0-9]|60|[1-9])))+$'
        }
        self.circuit = self.circuit.upper()
        circuit_list = self.circuit.strip().split('\n')
        measure_list = []  # 所有的M门，M门不能为空，并且所有的qubit不能重复
        new_circuit_list = circuit_list.copy()
        for index, circuit in enumerate(circuit_list):
            circuit = circuit.strip()
            cir = re.sub(' + ', ' ', circuit)  # 去掉中间多余的空格
            gate = cir.split(' ')[0]
            if gate in regular_exp_map.keys():
                # 判断是否符合基本的正则
                pattern = re.compile(regular_exp_map[gate], re.I)
                result = pattern.match(cir)
                if result is None:
                    return False
            else:
                return False
            if gate == 'M':
                # M后面不能存在相同的qubit
                qubit_list = cir.split(' ')[1:]
                measure_list.extend(qubit_list)
                after_measure_list = circuit_list[index:]
                for after_cir in after_measure_list:
                    after_cir = after_cir.strip()
                    if after_cir.startswith('M'):
                        continue
                    # 判断M之后的指令是否有M中的qubit
                    is_correct = [False if qubit in after_cir else True
                                  for qubit in qubit_list]
                    if not all(is_correct):
                        return False
            # if gate == 'CZ':
            #     # CZ指令需要两个qubit相减必须等于1，必须相邻qubit
            #     qubit_list = cir.split(' ')[1:]
            #     qubit0 = int(re.findall(r'\d+', qubit_list[0])[0])
            #     qubit1 = int(re.findall(r'\d+', qubit_list[1])[0])
            #     if abs(qubit1 - qubit0) != 1:
            #         return False
            if gate.startswith('R'):  # RX RY RZ RXY
                gate_qubit = cir.split(' ')[:2]
                gate_params = cir.split(' ')[2]
                for gate_param in gate_params:
                    if abs(float(gate_param)) > np.pi:
                        return False
                # 匹配出指令中的小数，不包含科学计数法
                r_result = re.findall(r'([+-]*?[0-9]\.\d*(?!E|e)[0-9])', cir)
                n_result = []
                for r in r_result:
                    num_list = r.split('.')
                    before = ''.join(num_list[0])
                    after = num_list[1]
                    if float(r) > 0 and len(after) > 2:
                        n_r = before + '.' + ''.join(after[:2])
                        n_result.append(n_r)
                    elif float(r) < 0 and len(after) > 20:
                        n_r = before + '.' + ''.join(after[:20])
                        n_result.append(n_r)
                if n_result:
                    new_cir = [*gate_qubit, *n_result]
                    new_circuit_list[index] = ' '.join(new_cir)
        if len(measure_list) == 0 or \
           len(measure_list) != len(set(measure_list)):
            return False
        new_circuit = '\n'.join(
            [circuit.strip() for circuit in new_circuit_list])
        return new_circuit


class Account():

    def __init__(self, login_key=None, machine_name=None):
        self.qcis_check = QcisCheck()
        self.qasmtoqcis = QasmToQcis()
        self.login_key = login_key
        self.token = None
        self.machine_name = machine_name
        # self.base_url = 'http://123.60.151.159:32384/agency/'  # 测试环境url
        # self.base_login_url = 'http://123.60.151.159:32384/api-uaa/oauth/token' # 测试环境登录url
        self.base_url = 'https://quantumctek-cloud.com/agency/'  # 生产环境url
        self.base_login_url = 'https://quantumctek-cloud.com/api-uaa/oauth/token' # 生产环境登录url
        self.login = self.log_in()
        if self.login == 0:
            raise Exception('登录失败')
        else:
            print('登录成功')

    def log_in(self):
        """
        Authenticate username and password and return user credit

        Returns
        -------
        log in state, 0 means pass authentication, 1 means failed

        """
        data = {
            'grant_type': 'openId',
            'openId': self.login_key,
            'account_type': 'member'
        }
        headers = {"Authorization": "Basic d2ViQXBwOndlYkFwcA=="}
        res = requests.post(url=self.base_login_url, headers=headers, data=data)
        status_code = res.status_code
        print(status_code)
        if status_code != 200:
            print('登录接口请求失败')
            return 0
        result = json.loads(res.text)
        code = result.get('code', -1)
        msg = result.get('msg', '登录失败')
        if code != 0:
            print(f'登录失败：{msg}')
            return 0
        token = result.get('data').get('access_token')
        self.token = token
        return 1

    def create_experiment(self, exp_name, remark='测试'):
        """create experiment

        Args:
            url (string): request the address

        Returns:
            0--失败, 非0成功
        """
        url = f'{self.base_url}/service/sdk/api/experiment/save'
        data = {"name": exp_name,
                "remark": remark}
        headers = {"basicToken": self.token, "Authorization": f'Bearer {self.token}'}
        res = requests.post(url, json=data, headers=headers)
        status_code = res.status_code
        if status_code != 200:
            print(f'创建实验接口请求失败, code:{status_code}')
            return 0
        result = json.loads(res.text)
        code = result.get('code', -1)
        msg = result.get('message', '创建实验失败')
        if code != 0:
            print(f'创建实验失败：{msg}')
            return 0
        lab_id = result.get('data').get('lab_id')
        return lab_id

    def save_experiment(self, lab_id, exp_data, name='detailtest', language='qcis'):
        """save experiment

        Args:
            url (string): request the addresslab_id

        Returns:
            0--失败, 非0成功

        12比特异常情况：
            1.保存实验返回的结果-->{'code':500, 'msg': XXX}
            2.保存实验返回的结果-->  (多进程同时请求可能出现的情况)
            3.保存实验返回的结果-->exp_id,当前实验已保存
            4.保存实验返回的结果-->量子线路指令输入错误，请检查你的输入
        正常情况：
            1.保存实验返回的结果-->exp_id
        """
        language_list = ['isq', 'quingo', 'qcis']
        if language not in language_list:
            print(f'保存实验失败, 量子语言只能在{language_list}中选择')
        exp_data = self.get_experiment_data(exp_data.upper())
        url = self.base_url + '/service/sdk/api/experiment/detail/save'
        data = {
            "inputCode": exp_data, "lab_id": lab_id,
            "languageCode": language, "name": name,
            "source": "SDK", "computerCode": self.machine_name
        }
        headers = {"basicToken": self.token, "Authorization": f'Bearer {self.token}'}
        res = requests.post(url, json=data, headers=headers)
        status_code = res.status_code
        if status_code != 200:
            print('保存实验接口请求失败')
            return 0
        result = json.loads(res.text)
        code = result.get('code', -1)
        msg = result.get('message', '保存实验失败')
        if code != 0:
            print(f'保存实验失败：{msg}')
            return 0
        save_result = result.get('data').get('exp_id')
        return save_result

    def run_experiment(self, exp_id, num_shots=12000):
        """run experiment

        Args:
            url (string): request the address

        Returns:
            0--失败, 非0成功
        """
        data = {"exp_id": exp_id, "shots": num_shots}
        return self.handler_run_experiment_result(data)

    def handler_run_experiment_result(self, data):
        url = self.base_url + '/service/sdk/api/experiment/temporary/save'
        headers = {"basicToken": self.token, "Authorization": f'Bearer {self.token}'}
        res = requests.post(url, json=data, headers=headers)
        status_code = res.status_code
        if status_code != 200:
            print('运行实验接口请求失败')
            return 0
        result = json.loads(res.text)
        code = result.get('code', -1)
        msg = result.get('message', '运行实验失败')
        if code != 0:
            print(f'运行实验失败：{msg}')
            return 0
        run_result = result.get('data').get('query_id')
        return run_result

    def submit_job(
            self, circuit=None, exp_name="exp0",
            parameters=None, values=None, num_shots=12000,
            lab_id=None, exp_id=None, version="version01"):
        if circuit:
            circuit = self.assign_parameters(
                circuit.upper(), parameters, values)
            print(circuit)
            if not circuit:
                print('无法为线路赋值，请检查线路，参数和参数值之后重试')
                return 0
        data = {
            "exp_id": exp_id,
            "lab_id": lab_id,
            "inputCode": circuit,
            "languageCode": "qcis",
            "name": exp_name,
            "shots": num_shots,
            "source": "SDK",
            "computerCode": self.machine_name,
            "experimentDetailName": version
        }
        return self.handler_run_experiment_result(data)

    def query_experiment(self, query_id, max_wait_time=60):
        """query experiment

        Args:
            query_id (int): 查询id
            max_wait_time(int): 最大等待时间

        Returns:
            0--失败, 非0成功
        """
        t0 = time()
        while time()-t0 < max_wait_time:
            try:
                url = f'{self.base_url}/service/sdk/api/experiment/result/find/{query_id}'
                headers = {"basicToken": self.token, "Authorization": f'Bearer {self.token}'}
                res = requests.get(url, headers=headers)
                status_code = res.status_code
                if status_code != 200:
                    print('查询接口请求失败')
                    return 0
                result = json.loads(res.text)
                code = result.get('code', -1)
                msg = result.get('message', '查询实验失败')
                if code != 0:
                    print(f'查询实验失败：{msg}')
                    # return 0
                query_exp = result.get('data')
                if query_exp:
                    return query_exp
            except:
                continue
            sleep_time = random.randint(
                0, 15)*0.3+round(random.uniform(0, 1.5), 2)
            print(f'查询实验结果请等待: {{:.2f}}秒'.format(sleep_time))
            sleep(sleep_time)
        print(f'查询实验结果失败')
        return 0

    def assign_parameters(self, circuit, parameters, values):
        """
        Check if the number of parameters, values match the circuit definition

        Parameters
        ----------
        circuit : string, QCIS circuit definition with or without parameter place holder
        parameters : list or ndarray of strings, parameters to be filled
        values : list or ndarray of floats, values to be assigned

        Returns
        -------
        circuit : circuit with parameters replaced by values or empty string
            empty string occurs when errors prevents parameters to be assigned
        """
        p = re.compile(r'\{(\w+)\}')
        circuit_parameters = p.findall(circuit)
        if circuit_parameters:

            # 如果values为整数或浮点数，改为列表格式##########################################################
            if isinstance(values, (float, int)):
                values = [values]
            # 如果parameters为字符格式，改为列表格式#########################################################
            if isinstance(parameters, str):
                parameters = [parameters]
            # 将所有parameter变为大写， 否则set(parameters) != set(circuit_parameters) 不通过 ###############
            parameters = [p.upper() for p in parameters]

            if not values:
                error_message = f'线路含有参数{circuit_parameters}, 请提供相应的参数值'
                print(error_message)
                return ''

            else:
                if len(circuit_parameters) != len(values):
                    error_message = f'线路含有{len(circuit_parameters)}个参数, 您提供了{len(values)}个参数值'
                    print(error_message)
                    return ''

                elif parameters and len(circuit_parameters) != len(parameters):
                    error_message = f'线路含有{len(circuit_parameters)}个参数, 您提供了{len(parameters)}个参数'
                    print(error_message)
                    return ''

                elif set(parameters) != set(circuit_parameters):
                    error_message = '线路中的参数与您输入的参数名称不符'
                    print(error_message)
                else:
                    param_dic = {}
                    ############################# 这个转化可以删了 #########################################
                    #parameters_upper = [p.upper() for p in parameters]
                    for p, v in zip(parameters, values):
                        param_dic[p] = v
                    expData = circuit.format(**param_dic)
                    return expData

        elif parameters or values:
            error_message = '线路定义中不含有参数，无法接受您输入的参数或参数值'
            print(error_message)
            return ''
        else:
            expData = circuit
            return expData

    def get_experiment_data(self, circuit):
        """
        Parse circuit description and generate 
        experiment script and extract number
        of measured qubits

        Parameters
        ----------
        circuit : string, QCIS circuit

        Returns
        -------
        expData : string, transformed circuit

        """
        # get gates from circuit
        gates_list = circuit.split('\n')
        gates_list_strip = [g.strip() for g in gates_list if g]
        gates_list_strip = [g for g in gates_list_strip if g]

        # transform circuit from QCIS to expData
        expData = '\n'.join(gates_list_strip)
        return expData

    def set_machine(self, machine_name):
        url = f'{self.base_url}/sdk/api/multiple/experiment/find/quantum/computer'
        data = {
            "experimentClipId": "",
            "machineName": machine_name,
            "name": "",
            "source": "SDK"
        }
        headers = {"basicToken": self.token, "Authorization": f'Bearer {self.token}'}
        res = requests.post(url, json=data, headers=headers)
        status_code = res.status_code
        if status_code != 200:
            return 0
        result = json.loads(res.text)
        code = result.get('code', -1)
        msg = result.get('message', '设置机器名失败')
        if code != 0:
            print(f'设置机器名失败：{msg}')
            return 0
        self.machine_name = machine_name

    def download_config(self):
        url = f'{self.base_url}/service/sdk/api/experiment/download/config/{self.machine_name}'
        headers = {"basicToken": self.token, "Authorization": f'Bearer {self.token}'}
        res = requests.get(url, headers=headers)
        status_code = res.status_code
        if status_code != 200:
            return 0
        result = json.loads(res.text)
        code = result.get('code')
        if code != 0:
            msg = result.get('msg', '下载实验参数失败')
            print(f'下载实验参数失败:{msg}')
            return 0
        data = result.get('data')
        cur_time = self.current_time()
        with open(f'./{self.machine_name}_config_param_{cur_time}.json', 'w') as f:
            f.write(json.dumps(data))
        return data

    def convert_qasm_to_qcis(self, qasm):
        qcis_raw = self.qasmtoqcis.convert_qasm_to_qcis(qasm)
        simplity_qcis = self.qasmtoqcis.simplify(qcis_raw)
        return simplity_qcis

    def convert_qasm_to_qcis_from_file(self, qasm_file):
        qcis_raw = self.qasmtoqcis.convert_qasm_to_qcis_from_file(qasm_file)
        simplity_qcis = self.qasmtoqcis.simplify(qcis_raw)
        return simplity_qcis

    def qcis_check_regular(self, qcis_raw):
        self.qcis_check.circuit = qcis_raw
        res = self.qcis_check.circuit_regular()
        if isinstance(res, bool):
            print('量子线路指令输入错误，请检查你的输入')
            return 0
        return res

    def simplify(self, qcis_raw):
        new_qcis_raw = self.qcis_check_regular(qcis_raw)
        simplity_qcis = self.qasmtoqcis.simplify(new_qcis_raw)
        return simplity_qcis
    
    def current_time(self):
        timestamp = datetime.datetime.fromtimestamp(time())
        str_time = timestamp.strftime('%Y%m%d%H%M%S')
        return str_time

