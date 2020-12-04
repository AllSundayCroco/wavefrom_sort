import matplotlib
import matplotlib.pyplot as plt
import time

class dynamicplot:
    
    def __init__(self):
        self.fig = plt.figure(figsize=(10, 4.8))
        self.ax_loss = self.fig.add_subplot(121)
        self.ax_acc = self.fig.add_subplot(122)
        self.Loss1_list = []
        self.acc1_list = []
        self.Loss2_list = []
        self.acc2_list = []
    
    def plotdefine(self):
        plt.ion()
        self.fig.show()
        self.fig.canvas.draw()
        
    def showplot(self,loss1,acc1,loss2,acc2):
        self.loss1 = loss1
        self.acc1 = acc1
        self.loss2 = loss2
        self.acc2 = acc2
        #plot
        
        
        self.Loss1_list.append(self.loss1)
        self.acc1_list.append(self.acc1)
        self.Loss2_list.append(self.loss2)
        self.acc2_list.append(self.acc2)
    
        self.ax_loss.clear()
        self.ax_loss.plot(self.Loss1_list,label = 'adam')
        self.ax_loss.plot(self.Loss2_list,label = 'gwdc')
        # ax_loss.set_title()
        self.ax_loss.set_xlabel('Iterations')
        self.ax_loss.set_ylabel('Loss')
        
        self.ax_acc.clear()
        self.ax_acc.plot(self.acc1_list)
        self.ax_acc.plot(self.acc2_list)
        # ax_acc.set_title()
        self.ax_acc.set_xlabel('Iterations')
        self.ax_acc.set_ylabel('Accuracy')
        self.fig.canvas.draw()
        
        time.sleep(1)
#adamwang push test
