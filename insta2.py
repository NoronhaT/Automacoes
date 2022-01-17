import tkinter.messagebox
from instapy import InstaPy
from tkinter import *


#Criar o objeto em TK
root = Tk()
#Tamanho do objeto
root.geometry("800x800")

#Nome do objeto
root.title('InstaNinja')
#cria o widget 'Rótulo' para o Formulário de Registro e usa o método place()
label_0 =Label(root,text="LOGIN", width=20,font=("bold",20))
# método place no tkinter é um gerenciador de geometria usado para organizar os widgets colocando-os em uma posição específica
label_0.place(x=90,y=60)
#isso cria o widget 'Label' para Usuário e usa o método place().
label_1 =Label(root,text="Usuário", width=20,font=("bold",10))
label_1.place(x=80,y=130)

#Aceita a string de entrada do usuário.
entry_1=Entry(root)
entry_1.place(x=240,y=130)
nome_user = entry_1.get()


#método para inserção da senha.
label_3 =Label(root,text="Senha", width=20,font=("bold",10))
label_3.place(x=68,y=180)

entry_3=Entry(root)
entry_3.place(x=240,y=180)

#Qual usuario pegar seguidores.
label_5 =Label(root,text="Perfil Alvo", width=20,font=("bold",10))
label_5.place(x=68,y=330)

entry_5=Entry(root)
entry_5.place(x=240,y=330)


#Etiqueta para ações e métodos.
label_4 =Label(root,text="Ações", width=20,font=("bold",10))
label_4.place(x=70,y=230)


#Variável de valor integral iniciada em 0
var=IntVar()

#Cria um campo com o estilo 'Radio button' com o método place()

# Radiobutton(root,text="Remover Seguidores",padx= 5, variable= var, value=1).place(x=235,y=230)
Radiobutton(root,text="Captar Seguidores de alguém",padx= 20, variable= var, value=2).place(x=220,y=250)
# Radiobutton(root,text="Comentar/Likes em Hashtags",padx= 20, variable= var, value=3).place(x=220,y=270)
Radiobutton(root,text="Remover não Seguidores",padx= 20, variable= var, value=4).place(x=220,y=290)


#INFORMA O USUÁRIO QUE AO REGISTRAR O NOME DE USUÁRIO, ELE NÃO PODERÁ ALTERAR DE NOVO:

tkinter.messagebox.showwarning(title="ATENÇÃO", message="Utilize com grandes intervalos, o Instagram monitora os acessos!")



# Verifica a opção escolhida e dá andamento no login:

def checaVar():
        if var.get() == 4 and len(entry_1.get())!=0 and len(entry_3.get())!=0:
                tkinter.messagebox.showinfo(title="REMOVE SEGUIDOR", message="Ao logar irei remover 150 pessoas que não seguem seu perfil de volta!")
                session = InstaPy(username=entry_1.get(), password = entry_3.get()).login()
                session.unfollow_users(amount=150, nonFollowers=True, style="RANDOM", unfollow_after=42*60*60, sleep_delay=655)

        elif var.get() == 2 and len(entry_5.get())!=0 and len(entry_3.get())!=0:
                tkinter.messagebox.showinfo(title="COPIA SEGUIDOR",
                                            message="Ao logar irei seguir 200 pessoas do perfil selecionado!")
                session = InstaPy(username=entry_1.get(), password=entry_3.get()).login()
                session.follow_user_followers([entry_5.get()], amount=200, randomize=True)

        elif len(entry_5.get()) == 0 and entry_5==2:
                tkinter.messagebox.showinfo(title="SEM ALVO", message= "Um usuário do instagram deve ser selecionado!")

        else:
                tkinter.messagebox.showerror(title="SEM DADOS INSERIDOS", message="São necessárias mais informações para continuar! Tente novamente")





#Cria um botão de submissão da informações
botao_iniciar = Button(root, text='Iniciar' , width=20,bg="black",fg='white', command= checaVar).place(x=180,y=380)



#É o que mantém o programa rodando.

root.mainloop()






