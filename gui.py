from tkinter import *
from tkinter import messagebox
import datetime as dt

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.deactivate_all_but(['personal_number'])
        self.users_list = self.read_lists('users.txt')
        self.books_list  = self.read_lists('books.txt')
        self.master.protocol('WM_DELETE_WINDOW',self.exit_program)

        # konstanter
        self.current_user = []
        self.all_possiable_actions = ["Search by writer","Search by titel","Loan a book"
            ,"Return a book","Show all books","Delete a book","Add a new book"
            ,"Add a new user","Delete a user","Show all users","Show late users"]

    def create_widgets(self):
        self.global_pad_x = 8
        self.global_pad_y = 6

        self.run_b = Button(self)
        self.run_b["text"] = "RUN"
        self.run_b["command"] = self.actions_runner
        self.run_b.grid(row=6,column=6,padx=self.global_pad_x,pady=self.global_pad_y,sticky='nsew')

        ## inloggning
        self.login_b = Button(self,text="Login")
        self.login_b["command"] = self.login_routin
        self.login_b.grid(row=0, column=0,columnspan=2, sticky='nsew'
            ,padx=self.global_pad_x,pady=self.global_pad_y)

        ## Logout
        self.logout_b = Button(self,text="Logout")
        self.logout_b["command"] = self.logout_routin
        self.logout_b.grid(row=0, column=5, sticky='nsew',pady=self.global_pad_y,
            padx=self.global_pad_x)


        self.ResultsText = Text(self,width=25, height=19)
        self.ResultsText.insert(END,'Results are here\n')
        self.ResultsText.grid(row=1,column=0,rowspan=5,sticky='ws'
            ,padx=self.global_pad_x,pady=3)

        # Readonly. To return u have to put state='normal'
        self.ResultsText.config(state=DISABLED)

        # ADD scrollbar
        self.scrollbar_text = Scrollbar(self, command=self.ResultsText.yview)
        self.ResultsText['yscrollcommand'] = self.scrollbar_text.set
        self.scrollbar_text.grid(row=1,column=1,rowspan=5,sticky='nswe')

        self.ListLabel = Label(self)


        self.actionListLabel = Label(self,text="Choose an Action")
        self.actionListLabel.grid(row=0,column=6,sticky='s',padx=self.global_pad_x,pady=self.global_pad_y)

        self.actionList = Listbox(self,width=17, height=15)

        self.actionList.grid(row=1,column=6,rowspan=5,sticky='e'
            ,padx=self.global_pad_x,pady=3)
        self.actionList.bind('<<ListboxSelect>>',self.change_active_wdg)

        self.quit = Button(self, text="Exit", 
                              command=self.exit_program)
        self.quit.grid(row=6,column=0,columnspan=2,sticky='nsew',padx=self.global_pad_x, pady=self.global_pad_y)

        # five labels,

        self.personal_number_label = Label(self,text="Personal Number:",font=("Arial",7))
        self.personal_number_label.grid(row=0,column=2,sticky='w')
        # it entry
        self.personal_number = Entry(self)
        self.personal_number.grid(row=0,column=3,columnspan=2,sticky='w',padx=4)
        self.personal_number.config(state='disabled')

        self.welcome_label = Label(self,text="please login with personal number",font=("Helvetica",14,"bold"),fg="blue",height=3)
        self.welcome_label.grid(row=1,column=2,columnspan=4)
        #


        self.username_label = Label(self,text="User Name:")
        self.username_label.grid(row=2,column=2)
        #
        self.username = Entry(self)
        self.username.grid(row=2,column=3,columnspan=2,padx=10, sticky='w')

        self.useremail_label = Label(self,text="User Email:")
        self.useremail_label.grid(row=3,column=2)
        #
        self.useremail = Entry(self)
        self.useremail.grid(row=3,column=3, columnspan=2,padx=10, sticky='w')

        self.usertype_label = Label(self,text="User Type:")
        self.usertype_label.grid(row=4,column=2,rowspan=2)
        #
        self.choosen_usertype = IntVar()
        self.radio_btn_1=Radiobutton(self,text='admin',value=1,variable=self.choosen_usertype)
        self.radio_btn_1.grid(row=4,column=3,rowspan=2)
        self.radio_btn_1.config(state='disabled')
        self.radio_btn_2 = Radiobutton(self,text='user',value=0,variable=self.choosen_usertype)
        self.radio_btn_2.grid(row=4,column=4,rowspan=2)

        ## Under Logout
        self.book_title_label = Label(self,text="Book Title:")
        self.book_title_label.grid(row=2,column=5,sticky='w')
        self.book_title = Entry(self)
        self.book_title.grid(row=3,column=5,sticky='e',padx=4)
 
        self.book_author_label = Label(self,text="Book Author:")
        self.book_author_label.grid(row=4,column=5,sticky='w')
        self.book_author = Entry(self)
        self.book_author.grid(row=5,column=5,sticky='en',padx=4)

        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)

    def find_user_with_PN(self,p_num):
        for user in self.users_list:
            if p_num == user[1]:
                return user
        return []

    def login_routin(self):
        p_num = self.personal_number.get()
        self.current_user = self.find_user_with_PN(p_num)

        if self.current_user:
            # successful login
            self.welcome_label["text"] = "Hi "+self.current_user[0][0].upper()+self.current_user[0][1:]
            self.actionList.delete(0,'end')

            for act in reversed(self.all_possiable_actions[:[5,None][self.current_user[3]=="admin"]]):
                self.actionList.insert(0,act)

            self.login_b.config(state="disabled")
            self.personal_number.config(state='disabled')
        else:
            # we can show this in result text instead
            messagebox.showerror("Error","The personal number you entered isn't right. \nTry Again!")
            #show error message
        self.personal_number.delete(0,'end')
        

    def logout_routin(self):

        self.current_user = []
        self.personal_number.clipboard_clear()
        self.login_b.config(state="normal")
        self.welcome_label["text"] = ""
        self.actionList.delete(0,'end')
        self.deactivate_all_but(['personal_number'])
        self.Show_in_result_window(["Results are here"])

    def find_late_users(self):
        late_users = []
        today = dt.datetime.date(dt.datetime.now())
        for book in self.books_list:
            book_date = [int(x) for x in book[-3:]]
            if sum(book_date) == 0: continue
            # print("===> ",book[-3:])
            lateness = (today-dt.date(*book_date)).days
            # later than two weeks
            if lateness>14:
                # add how many they owe the library if every day late cost is 10 SEK
                # print(self.find_user_with_PN(book[-4]))
                late_users.append(self.find_user_with_PN(book[-4]) + [str((lateness-14)*10)+ " SEK"])
        return late_users




    def actions_runner(self):
        choosen_indx = -1
        if self.actionList.curselection():
            choosen_indx = int(self.actionList.curselection()[0])

        if choosen_indx in [0,1]:
            if choosen_indx == 0:
                # search by author
                searched_str,sep_type,idx = self.book_author.get(),'.',1
            else:
                # by title
                searched_str,sep_type,idx = self.book_title.get(),'_',0
            searched_str = searched_str.replace(' ',sep_type).lower()
            # general match!!
            result = []
            for book in self.books_list :
                if (searched_str in book[idx].lower()) and len(searched_str)>1:
                    result.append('\t'.join(book[:2]))
            #print("==>",result)
            if result:
                self.Show_in_result_window(result)
            else:
                self.Show_in_result_window(["No Book were found for that search query!"])
        elif choosen_indx == 2:
            searched_str = self.book_title.get()
            searched_str = searched_str.replace(' ','_').lower()
            # exact match!!
            result = []
            for i,book in enumerate(self.books_list):
                if searched_str == book[0].lower():
                    result,idx = book,i
                    break
            if result:
                if int(result[2]):
                    self.Show_in_result_window(["Sorry, that book is already loaned,","Come back in a few days"])
                else:
                    #loan
                    self.books_list[idx][2] = self.current_user[1]
                    self.books_list[idx][-3:] = str(dt.datetime.date(dt.datetime.now())).split('-')
                    self.Show_in_result_window(["Here's your book,","Be sure to return in two weeks","Enjoy!"])
            else:
                self.Show_in_result_window(["Sorry, No book were found with that title","Be sure to enter the full title"])
        elif choosen_indx == 3:
            # return a book
            # exact search
            searched_str = self.book_title.get()
            searched_str = searched_str.replace(' ','_').lower()
            result = []
            for i,book in enumerate(self.books_list):
                if searched_str == book[0].lower():
                    result,idx = book,i
                    break
            if result:
                if result[2] == self.current_user[1]:
                    # he returned the book, see if he is late
                    late_users = self.find_late_users()
                    late = 0
                    for user in late_users:
                        if self.current_user[1] == user[1]:
                            fee_amount, late = user[-1], 1
                    if late:
                        self.Show_in_result_window(["Thanks for returning it.","Fees apply: "+fee_amount])
                    else:
                        self.Show_in_result_window(["Thanks for returing the book on time"])
                    self.books_list[idx][-4:] = ['0','0','0','0']
                else:
                    #someone else's
                    #Don't accept it
                    self.Show_in_result_window(["This book is loaned to other person", "maybe there's a mistake"])
            else:
                # no such a book
                self.Show_in_result_window(["No book with that title","maybe check it again!"])

        elif choosen_indx == 4:
            r = []
            for book in self.books_list:
                r.append('\t'.join(book[:2]))
            self.Show_in_result_window(r)
        elif choosen_indx == 5:
            # assumed admin of course
            # exact search
            searched_str = self.book_title.get()
            searched_str = searched_str.replace(' ','_').lower()
            result = []
            for i,book in enumerate(self.books_list):
                if searched_str == book[0].lower():
                    result,idx = book,i
                    break
            if result:
                # confirm
                ans = messagebox.askokcancel("Confirm","Are you sure you want to delete\n"+self.books_list[idx][0])
                if ans:
                    self.Show_in_result_window(["Book:",self.books_list[idx][0],"is deleted."])
                    _ = self.books_list.pop(idx)
            else:
                self.Show_in_result_window(["No Book here with that title"])
        elif choosen_indx == 6:
            book_name = self.book_title.get().replace(' ','_')
            book_author = self.book_author.get().replace(' ','.')
            if book_name and book_author:
                self.books_list.append([book_name, book_author, '0', '0', '0', '0'])
                self.Show_in_result_window(["New Book:",book_name,"is added to library."])
            else:
                self.Show_in_result_window(["please fill all the inputs to add a book"])
        elif choosen_indx == 7:
            # add user
            name = self.username.get().replace(' ','_')
            personal_num = self.personal_number.get()
            email = self.useremail.get()
            user_type = ['average','admin'][self.choosen_usertype.get()]
            if name and personal_num and email and user_type:
                self.users_list.append([name, personal_num, email, user_type])
                self.Show_in_result_window(["A new user:",name,"is added."])
            else:
                self.Show_in_result_window(["please fill all the inputs to add a user"])
        elif choosen_indx == 8:
            #delete a user
            user_p_num = self.personal_number.get()
            user_todelete = []
            loaned = 0
            for i,user in enumerate(self.users_list):
                if user_p_num == user[1]:
                    user_todelete,idx = user,i
            if user_todelete:
                # chick if he loaned a book
                for book in self.books_list:
                    if user_p_num == book[2]:
                        loaned = 1
                        break
                if loaned:
                    self.Show_in_result_window(["User cannot be deleted", "he still has books loaned."])
                else:
                    self.Show_in_result_window(["User with number",user_p_num,"is deleted!"])
                    _ = self.users_list.pop(idx)
                    if user_p_num == self.current_user[1]:
                        self.logout_routin()
            else:
                self.Show_in_result_window(["There's no User with that PN", "check it again for typos"])

        elif choosen_indx == 9:
            #show all users
            r = []
            for user in self.users_list:
                r.append('\t'.join([user[0][0].upper()+user[0][1:],user[-1]]))
            self.Show_in_result_window(r)

        elif choosen_indx == 10:
            late_users = self.find_late_users()
            #print(late_users)
            self.Show_in_result_window(['\t'.join([user[0],user[-1]]) for user in late_users])


        self.clear_all_entries()
        #self.deactivate_all_but()
        

    def prepare_input(self,x_str):
        x_str.replace(' ','_').lower()

    def Show_in_result_window(self,message_list):
        self.ResultsText.config(state='normal')
        self.ResultsText.delete('1.0','end')

        self.ResultsText.insert('end','\n'.join(message_list))
        self.ResultsText.config(state='disabled')

    def clear_all_entries(self):
        self.username.delete(0,'end')
        self.useremail.delete(0,'end')
        self.book_author.delete(0,'end')
        self.book_title.delete(0,'end')

    def deactivate_all_but(self, widg_names=[]):
        #for wdg in self.widg_names:
        self.personal_number.config(state=['disabled','normal']['personal_number' in widg_names])
        self.username.config(state=['disabled','normal']['username' in widg_names])
        self.useremail.config(state=['disabled','normal']['useremail' in widg_names])
        radios = ['disabled','normal']['radio_btns' in widg_names]
        self.radio_btn_1.config(state=radios)
        self.radio_btn_2.config(state=radios)
        self.book_title.config(state=['disabled','normal']['book_title' in widg_names])
        self.book_author.config(state=['disabled','normal']['book_author' in widg_names])

    def change_active_wdg(self,_):
        choosen_indx = -1
        if self.actionList.curselection():
            choosen_indx = int(self.actionList.curselection()[0])
        if choosen_indx == 0:
            self.deactivate_all_but(['book_author'])
        elif choosen_indx in [1,2,3,5]:
            self.deactivate_all_but(['book_title'])
        elif choosen_indx in [4,9,10]:
            self.deactivate_all_but([])
        elif choosen_indx == 6:
            self.deactivate_all_but(['book_title','book_author'])
        elif choosen_indx == 7:
            self.deactivate_all_but(['username','useremail','personal_number','radio_btns'])
        elif choosen_indx == 8:
            self.deactivate_all_but(['personal_number'])

    def read_lists(self,userfile):
            #userslist = []
        with open(userfile, "r") as f:
            userslist_noclass =[x.split() for x in f.readlines()]
            #for x in f.readlines():
            #    userslist.append(User(*x.split()))
        return userslist_noclass

    def write_lists(self,listfile,Thelist):
        with open(listfile,'w') as f:
            f.writelines('\t'.join(Thelist[0]))
            for x in Thelist[1:]:
                f.write('\n') 
                f.writelines('\t'.join(x))

    def exit_program(self):
        self.write_lists('users.txt',self.users_list)
        self.write_lists('books.txt',self.books_list)
        self.master.destroy()


if __name__ == "__main__":

    root = Tk()
    #root.geometry('850x400+150+100')
    root.title('Sam Library Program')
    app = Application(master=root)
    app.mainloop()

