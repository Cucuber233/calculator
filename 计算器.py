import tkinter as tk
import tkinter.messagebox
class App:
    def __init__(self):
        self.root=tk.Tk()
        self.root.title('计算器')
        self.root.geometry('450x450+600+300')
        self.root.protocol("WM_DELETE_WINDOW",self.close)
        self.root.bind('<KeyPress>',self.press)
        self.createWidget()
        #======用于存储算式======#
        self.stack=[]
        #======判断运算符是否被按下======#
        self.opispressd=False

    def press(self, event):
        if event.char in ['+','-','*','/','1','2','3','4','5','6','7','8','9','0']:
            self.work(event.char)
        elif event.keysym == 'Return':
            self.work('=')
        elif event.keysym == 'BackSpace':
            self.work('←')

    #======用于创建按钮组件======#
    def createbutton(self,i,j):
        tk.Button(self.root, text=self.bl[i][j], font=('微软雅黑', 16),width=3,command=lambda: self.work(self.bl[i][j])).\
            grid(row=i + 1, column=j + 1 if i == 5 and j == 1 else j, sticky='wesn', \
                 rowspan=2 if i == 4 and j == 3 else 1, \
                 columnspan=2 if i == 5 and j == 0 else 1)

    #======创建组件======#
    def createWidget(self):
        #======面板显示数值对象======#
        self.show=tk.StringVar()
        self.show.set('0')
        #======输入框组件======#
        self.e01=tk.Label(self.root,textvariable=self.show,width=16,font=("微软雅黑",25),anchor='e',bg='white')
        self.e01.grid(row=0,column=0,columnspan=4,sticky='wesn')
        #======历史记录组件======#
        self.text=tk.Text(self.root,width=15,font=("微软雅黑",10))
        self.text.grid(row=0,column=4,rowspan=8,sticky='wesn')
        self.text.insert(1.0,'历史记录\n')
        #======按钮列表======#
        self.bl=[['CE', 'x2', '√', '←'],
                 ['C',  '//', '/', '*'],
                 ['7',  '8',  '9', '-'],
                 ['4',  '5',  '6', '+'],
                 ['1',  '2',  '3', '='],
                 ['0',  '.']]
        #======创建按钮组件======#
        for i in range(6):
            for j in range(2 if i == 5 else 4):
                self.createbutton(i,j)

    #======所有按钮共用一个处理函数work()======#

    def work(self, x):
        #======点击数字1~9时把数值加入show中======#
        #======数字输入情况需要考虑运算符状态和小数点======#
        if '0'<=x<='9' or x=='.' :
            if self.opispressd==True:
                self.show.set(0)
                self.opispressd=False
            if x=='.' and ('.'not in self.show.get()):
                self.show.set(self.show.get()+'.')
            elif x!='.':
                if self.show.get()=='0':
                    self.show.set(x)
                else:
                    self.show.set(self.show.get()+x)
        #======点击运算符时，把show变量和运算符压栈======#
        #======如果使用 + - * /或 //进行计算，则需要直接进行运算======#
        elif x in ['+','-','*','/','//']:
            if len(self.stack)==0:
                self.stack.append(str(self.show.get()))
                self.stack.append(x)
                self.opispressd = True
##            elif self.opispressd==False:
##                # 如果栈里已经有算式，那么将show加入stack算式中
##                self.stack.append(str(self.show.get()))#已经是一个完整的算式
##                # 把stack中的元素合并为字符串 str1= ''.join(self.stack)
##                # 使用eval(str1)进行计算 '5+5' -> 10
##                # 把运算结果赋值给show，同时把show和当前按下的运算符加入stack
##                str1 = ''.join(self.stack)
##                #运算异常处理
##                try:
##                    ans=eval(str1)
##                except ZeroDivisionError:
##                    tk.messagebox.showerror('错误','除数不能为0')
##                    self.stack.clear()
##                    return #停止work函数
##                self.show.set(str(ans))#把结果赋值给show
##                #把算式加入历史记录
##                self.text.insert(2.0,str1+'='+str(ans)+'\n')
##                self.stack.clear()
##                self.stack.append(self.show.get())
##                self.stack.append(x)
##                self.opispressd=True

        #======点击等于号时，如果栈为空，则把运算符设为按下======#
        #======如果栈不为空，进行运算======#
        elif x == '=':
            if len(self.stack)==0:#如果算式为空，不做任何操作
                self.opispressd=True
                return
            #如果算式不为空，则进行运算
            self.stack.append(str(self.show.get()))
            calc = ''.join(self.stack)
            try:
                result = eval(calc)
            except ZeroDivisionError:
                tk.messagebox.showinfo('错误','除数不能为0')
                self.stack.clear()
                return
            result = round(result,10)
            self.show.set(result)
            self.opispressd = True
            self.stack.clear()
            self.text.insert(2.0,'\n'+calc+'='+str(result)+'\n')

        #====== 按下C键时，清空栈和show  ======#
        #====== 按下CE键时，清空show   ======#
        elif x in ['C','CE']:
            if x=='CE':
                self.show.set(0)
            else:
                self.show.set(0)
                self.stack.clear()

        elif x in ['x2','√']:
            self.stack.clear() #清空算式
            if x=='x2':
                t=float(self.show.get())
                self.show.set(str(t**2))
                self.text.insert(2.0,str(t)+'**2='+str(self.show.get()+'\n'))
            else:
                if float(self.show.get()) < 0:
                    tk.messagebox.showerror('错误','负数没有算术平方根。')
                else:
                    t = float(self.show.get())
                    self.show.set(str(t ** 0.5))
                    self.text.insert(2.0, '√' + str(t) +'='+ str(self.show.get() + '\n'))

        elif x =='←':
            if len(self.show.get())==1:
                self.show.set('0')
            else:
                length=len(self.show.get())
                self.show.set(self.show.get()[:length-1])



    def close(self):
        if tk.messagebox.askokcancel('退出','确定退出计算器吗？'):
            self.root.destroy()
            
    def run(self):
        self.root.mainloop()

app= App()
app.run()
