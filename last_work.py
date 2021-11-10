from matplotlib import pyplot as plt
import abc #利用abc模块实现抽象类
import copy


class Operation(metaclass=abc.ABCMeta):
    def __init__(self):
        self.record = True

    @abc.abstractmethod  # 定义抽象方法，无需实现功能
    def do(self, canvas, parameter):
        '子类必须定义名字功能'
        pass

    @abc.abstractmethod  # 定义抽象方法，无需实现功能
    def undo(self, canvas, parameter):
        '子类必须定义参数功能'
        pass


class Move(Operation):

    def do(self, canvas, parameter):
        '''
            parameters = "index datax datay"
        '''
        parameter = parameter.split(" ")

        canvas.graph_list[int(parameter[0])].Move([float(parameter[1]), float(parameter[2])])

    def undo(self, canvas, parameter):
        parameter = parameter.split(" ")
        canvas.graph_list[int(parameter[0])].Move([-1*float(parameter[1]), -1*float(parameter[2])])


class Copy(Operation):
    def do(self, canvas, parameter):
        '''
            parameters = "index"
        '''
        new_Graph = canvas.graph_list[int(parameter[0])].copy()
        canvas.graph_list.append(new_Graph)

    def undo(self, canvas, parameter):
        canvas.graph_list.pop()


class List(Operation):
    def __init__(self):
        super(List, self).__init__()
        self.record = False

    def do(self, canvas, parameter):
        '''
        parameter: None
        '''
        count = 0
        plt.figure(figsize=(6, 6))
        plt.xlim((-50, 50))
        plt.ylim((-50, 50))
        ax = plt.gca()  # 获取当前坐标的位置
        ax.spines['right'].set_color('None')
        ax.spines['top'].set_color('None')
        # 指定坐标的位置
        ax.xaxis.set_ticks_position('bottom')  # 设置bottom为x轴
        ax.yaxis.set_ticks_position('left')  # 设置left为x轴
        ax.spines['bottom'].set_position(('data', 0))  # 这个位置的括号要注意
        ax.spines['left'].set_position(('data', 0))
        # 设置x,y的坐标描述标签
        for graph in canvas.graph_list:
            graph.Show(count)
            count += 1
        plt.show()


    def undo(self, canvas, parameter):
        pass

class Remove(Operation):
    def do(self, canvas, parameter):
        '''
        parameter: "index"
        '''
        del canvas.graph_list[parameter[0]]

    def undo(self, canvas, parameter):
        pass

class Add(Operation):
    def do(self, canvas, parameter):
        '''
        parameter: "add name graph_parameters"
        '''
        graph = parameter
        graph_name = graph.split(" ")[0]
        graph_para = graph.split(graph_name + " ")[1]

        new = canvas.graph_lib[graph_name](graph_para)
        canvas.graph_list.append(new)

    def undo(self, canvas, parameter):
        canvas.graph_list.pop()
        print("cancel add")

class Undo(Operation):
    def __init__(self):
        super(Undo, self).__init__()
        self.record = False

    def do(self, canvas, parameter):
        '''
        parameter: None
        '''
        command = canvas.do_operation.pop()
        cmd_name = command.split(" ")[0]
        try:
            parameter = command.split(cmd_name + ' ')[1]
        except:
            parameter = None
        canvas.operation[cmd_name].undo(canvas, parameter)
        canvas.undo_operation.append(command)

    def undo(self, canvas, parameter):
        pass

class Redo(Operation):
    def __init__(self):
        super(Redo, self).__init__()
        self.record = False

    def do(self, canvas, parameter):
        '''
        parameter: None
        '''
        command = canvas.undo_operation.pop()
        canvas.Run_Command(command)

    def undo(self, canvas, parameter):
        pass

class Graph(metaclass=abc.ABCMeta):
    def __init__(self):
        self.name = ""
        self.parameter = ""

    def GetName(self):
        return self.name

    def copy(self):
        return copy.deepcopy(self)

    @abc.abstractmethod  # 定义抽象方法，无需实现功能
    def Move(self, parameter):
        pass

    @abc.abstractmethod  # 定义抽象方法，无需实现功能
    def Solve_Parameter(self):
        pass

    @abc.abstractmethod  # 定义抽象方法，无需实现功能
    def Show(self):
        pass

class Line(Graph):
    def __init__(self, parameter):
        '''
        parameter "startx starty endx endy"
        '''
        super(Line, self).__init__()
        self.name = "Line"
        self.parameter = parameter
        self.Solve_Parameter()

    def Solve_Parameter(self):
        parameter = self.parameter.split(" ")
        self.parameter = ([float(parameter[0]), float(parameter[2])],
                            [float(parameter[1]), float(parameter[3])])

    def Show(self, index):
        plt.plot(self.parameter[0], self.parameter[1])
        locx = (self.parameter[0][0] + self.parameter[0][1])/2.0
        locy = (self.parameter[1][0] + self.parameter[1][1])/2.0
        plt.text(locx, locy, str(index), ha='center', va='bottom', fontsize=7)

    def Move(self, parameter):
        '''
        :param parameter: [shift_x shift_y]
        '''
        self.parameter[0][0] += parameter[0]
        self.parameter[1][0] += parameter[0]
        self.parameter[0][1] += parameter[1]
        self.parameter[1][1] += parameter[1]

class Circle(Graph):
    def __init__(self, parameter):
        '''
        parameter: "centerx centery radis"
        '''
        super(Circle, self).__init__()
        self.name = "Circle"
        self.parameter = parameter
        self.Solve_Parameter()

    def Solve_Parameter(self):
        parameter = self.parameter.split(" ")
        self.parameter = ([float(parameter[0]), float(parameter[1])], float(parameter[2]))

    def Show(self, index):
        circle = plt.Circle(self.parameter[0], self.parameter[1],fill=None)
        plt.gcf().gca().add_artist(circle)
        loc = circle.get_center()
        plt.text(loc[0], loc[1], str(index), ha='center', va='bottom', fontsize=7)


    def Move(self, parameter):
        '''
        :param parameter: [shift_x shift_y]
        '''
        self.parameter[0][0] += parameter[0]
        self.parameter[0][1] += parameter[1]

class Rectangle(Graph):
    def __init__(self, parameter):
        '''
        parameter: "startx starty endx endy"
        '''
        super(Rectangle, self).__init__()
        self.name = "Rectangle"
        self.parameter = parameter
        self.Solve_Parameter()

    def Solve_Parameter(self):
        parameter = self.parameter.split(" ")
        gap_x = float(parameter[2]) - float(parameter[0])
        gap_y = float(parameter[3]) - float(parameter[1])
        bottom_leftx = min(float(parameter[0]), float(parameter[2]))
        bottom_lefty = min(float(parameter[1]), float(parameter[3]))
        self.parameter = ([bottom_leftx, bottom_lefty], gap_x, gap_y)

    def Show(self, index):
        rect = plt.Rectangle(self.parameter[0], self.parameter[1], self.parameter[2], fill=None)
        plt.gcf().gca().add_artist(rect)
        locx = self.parameter[0][0] + self.parameter[1] * 0.5
        locy = self.parameter[0][1] + self.parameter[2] * 0.5
        plt.text(locx, locy, str(index), ha='center', va='bottom', fontsize=7)

    def Move(self, parameter):
        '''
        :param parameter: [shift_x shift_y]
        '''
        self.parameter[0][0] += parameter[0]
        self.parameter[0][1] += parameter[1]

class Canvas:
    def __init__(self):
        self.graph_list = []
        self.do_operation = []
        self.undo_operation = []
        self.operation = {}
        self.graph_lib = {"line":Line, "circle": Circle, "rectangle": Rectangle}
        self.Register_Operation()

    def Register_Operation(self):
        self.operation["copy"] = Copy()
        self.operation["move"] = Move()
        self.operation["list"] = List()
        self.operation["add"] = Add()
        self.operation["remove"] = Remove()
        self.operation["undo"] = Undo()
        self.operation["redo"] = Redo()


    def Run_Command(self, command):
        cmd_name = command.split(" ")[0]
        try:
            parameter = command.split(cmd_name+' ')[1]
        except:
            parameter = None
        self.operation[cmd_name].do(self, parameter)
        if(self.operation[cmd_name].record == True):
            self.do_operation.append(command)


if __name__ == '__main__':
    canvas = Canvas()
    command = input("-")
    while(command != "exit"):
        canvas.Run_Command(command)
        command = input("-")


