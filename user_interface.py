class UserInterface:
    """
    一个简单的命令行用户界面类，用于接收用户的输入并呈现结果。
    """
    def __init__(self):
        """
        初始化 UserInterface 类的一个实例。
        """
        self.running = True

    def prompt_for_signal(self):
        """
        提示用户输入信号类型和信号数据。

        返回:
            signal_type (str): 用户输入的信号类型。
            signal_data (str): 用户输入的信号数据。
        """
        print("\n请输入信号类型:")
        signal_type = input()

        print("\n请输入信号数据:")
        signal_data = input()

        return signal_type, signal_data

    def display_results(self, signal_type, parameters, demodulated_signal):
        """
        显示信号类型、参数估计和解调信号。

        参数:
            signal_type (str): 信号类型。
            parameters (dict): 估计的信号参数。
            demodulated_signal (str): 解调后的信号。
        """
        print("\n信号类型:", signal_type)
        print("\n信号参数:")
        for param, value in parameters.items():
            print(f"{param}: {value}")
        print("\n解调后的信号:", demodulated_signal)

    def run(self):
        """
        运行用户界面。
        """
        while self.running:
            signal_type, signal_data = self.prompt_for_signal()
            # 这里假设我们有一个名为 `process_signal` 的函数来处理信号
            parameters, demodulated_signal = process_signal(signal_type, signal_data)
            self.display_results(signal_type, parameters, demodulated_signal)

            print("\n是否继续? (y/n)")
            continue_answer = input()
            if continue_answer.lower() != 'y':
                self.running = False

if __name__ == "__main__":
    ui = UserInterface()
    ui.run()
