from tkinter import *
from tkinter import ttk
import glob
import os
import random


class Asker(Frame):

    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.parent = parent
        self.makeWidget()

    def count_questions(self, a):
        number_of_questions = len(a)
        self.label2.configure(text='Number of the remaining questions: {}'.format(number_of_questions))

    def better_open(self):
        self.button4['state'] = NORMAL
        self.button2['state'] = NORMAL
        self.questions = []
        self.answers = []
        whole_list = []

        file = self.file_name.get()
        with open(file) as f:
            for line in f.readlines():
                df = line.rstrip('\n')
                whole_list.append(df)

        t = len(whole_list) - 1
        counter = 0
        while counter < t:
            self.questions.append(whole_list[counter])
            counter += 1
            self.answers.append(whole_list[counter])
            counter += 1
            counter += 1

        self.text1.delete(0.0, END)
        self.text1.insert(0.0, self.questions[0])

        if self.v.get() == 1:
            self.radio2.configure(state="disabled")
        if self.v.get() == 2:
            self.radio1.configure(state="disabled")

        self.count_questions(self.questions)

    def hint_func(self):
        self.text2.pack(fill=BOTH, expand=True)
        self.text2.delete(0.0, END)
        self.text2.insert(0.0, self.answers[0])

    def good_ans(self):
        self.text2.pack_forget()
        self.questions = self.questions[1:]
        if self.v.get() == 1:

            try:
                self.text1.delete(0.0, END)
                self.text2.delete(0.0, END)
                self.text1.insert(0.0, self.questions[0])
                self.answers = self.answers[1:]
            except IndexError:
                self.text1.insert(0.0, 'no more questions')
                self.button4['state'] = DISABLED
                self.button2['state'] = DISABLED
                self.radio2.configure(state="normal")
                self.radio1.configure(state="normal")

        elif self.v.get() == 2:
            self.answers = self.answers[1:]
            try:
                max_position = len(self.questions) - 1
                random_position = random.randint(0, max_position)
                pop_quest = self.questions.pop(random_position)
                pop_answ = self.answers.pop(random_position)
                self.questions.insert(0, pop_quest)
                self.answers.insert(0, pop_answ)

                self.text1.delete(0.0, END)
                self.text2.delete(0.0, END)
                self.text1.insert(0.0, self.questions[0])

            except ValueError:
                self.text1.delete(0.0, END)
                self.text2.delete(0.0, END)

                self.text1.insert(0.0, 'no more questions')
                self.button4['state'] = DISABLED
                self.button2['state'] = DISABLED
                self.radio2.configure(state="normal")
                self.radio1.configure(state="normal")
        self.count_questions(self.questions)

    def bad_ans(self):
        self.text2.pack_forget()
        a = len(self.questions)
        position = a-1
        question1 = self.questions[0]
        answer1 = self.answers[0]

        self.questions = self.questions[1:]
        self.answers = self.answers[1:]

        self.questions.insert(position, question1)
        self.answers.insert(position, answer1)

        self.text1.delete(0.0, END)
        self.text2.delete(0.0, END)
        self.text1.insert(0.0, self.questions[0])

    def files_in_directory(self):
        files_abs_path = glob.glob(str(os.getcwd()) + '/' + '*.txt')
        file_names = []
        for i in files_abs_path:
            file_names.append(os.path.split(i)[1])
        return file_names

    def makeWidget(self):

        frame = Frame(self,  borderwidth=1, padx=10, pady=10)
        frame.pack(fill=X,  side=TOP)
        self.pack(fill=BOTH, expand=True)

        frame2 = Frame(self, borderwidth=1, padx=10, pady=10)
        frame2.pack(fill=X,  side=TOP)

        label_questions = Label(frame2, text='Question: ', font=('Arial',16))
        label_questions.pack(side=LEFT)

        frame3 = Frame(self, borderwidth=1, padx=10, pady=10)
        frame3.pack(fill=BOTH, expand=True)

        frame4 = Frame(self, borderwidth=1, padx=10, pady=10)
        frame4.pack(fill=BOTH)

        label_answers = Label(frame4, text='Answer: ', font=('Arial', 16))
        label_answers.pack(side=LEFT)

        self.file_name = StringVar()
        c = ttk.Combobox(frame, textvariable=self.file_name)
        c['values'] = tuple(self.files_in_directory())
        c.pack(side=LEFT, fill=X, expand=True)

        self.text1 = Text(frame3,font=('Arial', 12), width=60, height=3)
        self.text1.pack(fill=BOTH, expand=True)

        button1 = Button(frame, text='Open ', command=self.better_open)
        button1.pack(side=RIGHT)

        self.button2 = Button(frame4, text='Wrong', command=self.bad_ans)
        self.button2.pack(side=RIGHT)

        button3 = Button(frame4, text='OK', command=self.good_ans)
        button3.pack(side=RIGHT)

        self.button4 = Button(frame4, text='Hint', command = self.hint_func)
        self.button4.pack(side=RIGHT)

        frame5 = Frame(self, borderwidth=1, width=100, height=76, padx=10, pady=10)
        frame5.pack(fill=BOTH, expand=True)

        self.text2 = Text(frame5, font=('Arial', 12), width=60, height=3)
        self.text2.pack(fill=BOTH, expand=True)

        self.text2.pack_forget()

        self.v = IntVar()
        self.v.set(1)
        self.radio1 = Radiobutton(frame, text="In order", variable=self.v, value=1)
        self.radio1.pack(anchor=W)
        self.radio2 = Radiobutton(frame, text="Random", variable=self.v, value=2)
        self.radio2.pack(anchor=W)

        self.label2 = Label(frame2, text='Number of the remaining questions: {}'.format(0), font=('Arial', 12))
        self.label2.pack(side=RIGHT)

if __name__ == '__main__':
    root = Tk()
    Asker(root)
    root.title('Asker')
    root.mainloop()