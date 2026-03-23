from servidor.processa_cliente import ProcessaCliente
import servidor
import socket
from dados.dados import Dados
from servidor.operacoes.somar import Somar

class Maquina:
	def __init__(self):
		self.s = socket.socket()
		self.s.bind(('', servidor.PORT))
		self.s.listen(35000)
		self.sum = Somar()
		self.dados = Dados()

	def execute(self):
		print("Waiting for clients on port " + str(servidor.PORT))
		while True: # Loop infinito para múltiplos clients
			print("On accept...")
			connection, address = self.s.accept()
			print("Client", address, " connected")
			processo_cliente = ProcessaCliente(connection, address, self.dados)
			processo_cliente.start()


	# def __init__(cliente.interface.Interface:object interface):
	# 	self.interface:object = interface
	# 	self.somar:object  = servidor.operacoes.somar.Somar()
	# 	self.dividir:object = servidor.operacoes.dividir.Dividir()
	# def exec():
	# 	res = self.interface.exec()
    # 		if res =="+":
    #     	s:object = somar.Somar(x,y)
    #     	res = s.executar(x,y)
    #     	interacao.resultado(res)
    #     print("O valor da operação somar é:", res)
    # elif res =="/":
    #     s:object = dividir.Dividir(x,y)
    #     res = s.executar()
    #     if type(res)==str:
    #         print (res)
    #     else:
    #         print("O valor da operação divisão é:",res)

#c = command.split()
		# Get the operator
	#	if c[0] =="+":
			#Call operator
	#		res = self.sum.execute(float(c[1]),float(c[2]))
	#	return res