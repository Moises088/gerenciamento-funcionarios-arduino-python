from logging import root
import serial
import time
from tkinter import *
from tkinter import messagebox, ttk
import datetime

id = 1
id_report = 1

# Abra a porta serial à qual seu arduino está conectado.
arduino = serial.Serial("COM3", 9600)
print(arduino.name)

# Criando classe de funcionários
class Employees:
    def __init__(self, name, code, job_position, status):
        self.id = id
        self.name = name
        self.code = code
        self.job_position = job_position
        self.status = status

# Criando classe de relatórios
class EmployeeReports:
    def __init__(self, employee_id, status):
        now = datetime.datetime.now()
        self.id = id_report
        self.employee_id = employee_id
        self.info = "--"
        self.date = now.strftime("%d/%m/%Y %H:%M:%S")
        self.status = status

# Funcionários iniciais
employees = []
employees.append(Employees("Moisés", "1234", "Dev", "Ativado"))

# Funcionários ativados
employees_actives = []

# Mapeamento de teclado
keypad_map = [
    "1", "2", "3", "4", "5",
    "6", "7", "8", "9", "0",
    "A", "B", "C", "D",
    "#", "*"
]

# Código que está sendo digitado
typed_code = ""

# Função de fechar janela
def closeWindow():
    if messagebox.askokcancel("Fechar", "Deseja fechar o programa?"):
        root.destroy()

# Função de traduzir a tecla pressionada
def translateKeyPressed(key):
    decodeKey = key.decode("utf-8")
    if decodeKey in keypad_map:
        return decodeKey
    return ""

# Função para limpar o código digitado
def clearCode():
    global typed_code
    typed_code = ""

# Setando o código
def setCode(key):
    global typed_code
    typed_code = typed_code + key
    print("typed_code", typed_code)

# Buscando o usuário
def searchEmployee(typed_code):
    print(typed_code)
    findedEmployee = False
    for employee in employees:
        if(employee.code == typed_code):
            findedEmployee = employee
    return findedEmployee

def toggleLed():
    arduino.write('1'.encode())
    time.sleep(3)
    arduino.write('2'.encode())

# definindo status
def defStatus(employee_id):
    newList = [num for num in reversed(employees_actives)]
    status = ""
    for list in newList:
        if list.employee_id == employee_id:
            status = list.status
            break
    if status == "Ativo":
        return "Inativo"
    
    return "Ativo"
        

# Quando encontrar o funcionário
def activeEmployee(employee):
    global id_report
    arduino.write('3'.encode())
    time.sleep(3)
    arduino.write('2'.encode())
    status = defStatus(1)
    employees_actives.append(EmployeeReports(employee.id, status))
    id_report = id_report + 1
    generateTable(employees_actives[id_report-2])


# Configurando a janela
root = Tk()
root.title("Gerenciamento de Funcionários")
root.geometry("850x400")
root.config(bg="#e3e6fc")
root.resizable(False, False)

mainF = Frame(root, width = 800).pack(side=TOP,fill=NONE)
mainLabel = Label(
    mainF, 
    text="Bem vindo ao Gerenciamento de Funcionários",  
    bg="#3246a8", 
    fg="#fff",
    height=3, 
    font=("Arial", 14),
    width=113
).pack()

container = Frame(mainF, width = 800).pack(side=BOTTOM,fill=BOTH)

frameLeft = Frame(container)
frameLeft.pack(side=LEFT, expand = 1)

leftLabel = Label(
    frameLeft, 
    text="Funcionários",  
    bg="#3246a8", 
    fg="#fff",
    font=("Arial", 12),
    width = 44
).pack(side=TOP)
containerEmployees = Frame(frameLeft, bg = "#e3e6fc", width = 380, height = 470)
containerEmployees.pack()

employeeTable = ttk.Treeview(containerEmployees)

employeeTable['columns'] = ('id', 'nome', 'código', 'cargo', 'status')

employeeTable.column("#0", width=0,  stretch=NO)
employeeTable.column("id",anchor=CENTER, width=40)
employeeTable.column("nome",anchor=CENTER,width=120)
employeeTable.column("código",anchor=CENTER,width=80)
employeeTable.column("cargo",anchor=CENTER,width=80)
employeeTable.column("status",anchor=CENTER,width=80)

employeeTable.heading("#0",text="",anchor=CENTER)
employeeTable.heading("id",text="Id",anchor=CENTER)
employeeTable.heading("nome",text="Nome",anchor=CENTER)
employeeTable.heading("código",text="Código",anchor=CENTER)
employeeTable.heading("cargo",text="Cargo",anchor=CENTER)
employeeTable.heading("status",text="Status",anchor=CENTER)

for employee in employees:
    employeeTable.insert(parent='',index='end',iid=0,text='',
    values=(employee.id,employee.name,employee.code,employee.job_position, employee.status))

employeeTable.pack()

frameRight = Frame(container)
frameRight.pack(side=RIGHT, expand = 1)

leftLabel = Label(
    frameRight, 
    text="Relatórios",  
    bg="green", 
    fg="#fff",
    font=("Arial", 12),
    width = 44
).pack(side=TOP)
containerReports = Frame(frameRight, bg = "#e3e6fc", width = 380, height = 470)
containerReports.pack()

reportsTable = ttk.Treeview(containerReports)

reportsTable['columns'] = ('id', 'id_funcionario', 'info', 'data', 'status')

reportsTable.column("#0", width=0,  stretch=NO)
reportsTable.column("id",anchor=CENTER, width=40)
reportsTable.column("id_funcionario",anchor=CENTER,width=110)
reportsTable.column("info",anchor=CENTER,width=40)
reportsTable.column("data",anchor=CENTER,width=130)
reportsTable.column("status",anchor=CENTER,width=80)

reportsTable.heading("#0",text="",anchor=CENTER)
reportsTable.heading("id",text="Id",anchor=CENTER)
reportsTable.heading("id_funcionario",text="Id Funcionário",anchor=CENTER)
reportsTable.heading("info",text="Info",anchor=CENTER)
reportsTable.heading("data",text="Data",anchor=CENTER)
reportsTable.heading("status",text="Status",anchor=CENTER)

def generateTable(employee):
    reportsTable.insert(parent='',index='end',iid=(employee.id - 1),text='',
    values=(employee.id,employee.employee_id,employee.info,employee.date, employee.status))
    root.update()

reportsTable.pack()

while True:
    root.update()
    if(arduino.in_waiting > 0):
        print("ARDUINO")
        keypad=arduino.read()
        translatedKey = translateKeyPressed(keypad)
        if(translatedKey == "*"):
            clearCode()
        elif(translatedKey == "#"):
            employee = searchEmployee(typed_code)
            if(employee):
                activeEmployee(employee)
            else:
                toggleLed()
            clearCode()
        else:
            setCode(translatedKey)

        del keypad
