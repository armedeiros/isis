
#PROJETO PESQUISA GALATEA UNESP BAURU 2020/2021
#DR. DORIVAL ROSSI
#DR. FERNANDO MARAR
#ANDRE MEDEIROS


### todas as libs necessarias em ordem
import sys
import os
import numpy as np #classica!
import winsound ##

from datetime import datetime
from pywinauto.application import Application 
#automação processos windows (trabalha na camada de mensagens do sistema operacional)
winsound.Beep(2200, 30)
import string

print("\n> Importando recursos de fala.........: " + str(datetime.now()))
import pyttsx3 as fala 
winsound.Beep(2200, 30)
print("> Importando recursos de recognição...: " + str(datetime.now()))
import speech_recognition as sr 
winsound.Beep(2200, 30)

print("> Importando recursos de conversação..: " + str(datetime.now()))
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer 
winsound.Beep(2200, 30)
print("> Importando recursos de visão comput.: " + str(datetime.now()))
import cv2
winsound.Beep(2200, 30)
####

### vars iniciais
n      = 0 #contador
dtnas  = "2020-03-01 13:25:00.000000" # dt de nascimento 
action = 0 #define ação

rec   = sr.Recognizer() #tratamento do reconhecimento de fala
###

###tratamento da robo
bot = ChatBot('GALATEA') #inicia o Bot no ambiente
winsound.Beep(2200, 30)
#carga inicial de vocabulario
chats =  ['Como vai?', 'Tudo legal','Voce pode me ajudar?', 'Claro que posso! Diga?', 'Voce Conhece TOTVS Protheus?', 'Ouvi dizer que esse software eh muito bom!', 'Radio CBN', 'Noticias sao importantes', 'Qual seu nome?', 'Me chamo GALATEA muito prazer em conhecer voce']
chats += ['Oi!', 'Olah Pessoa Humana!', 'O dia esta bom','Dias assim sao bons', 'Voce sabe sobre muita coisa?', 'Posso aprender se voce me ensinar', 'Como voce se chama?', 'Me chamam de GALATEA.', 'Quantos anos voce tem?', 'Eu nao tenho idade...']
chats += ['Conhece o Fluig?', 'Eh uma plataforma legal!', 'Voce gosta?','Gosto nao se discute', 'Ja ouviu falar?', 'Depende, posso pesquisar...']
chats += ['Desligar', 'Ja vai? Ateh logo!', 'Voce sabe se vai chover amanha?', 'Vamos ver o clima...']
chats += ['Entender', 'Sempre refletindo', 'Boa dia', 'Olah ser humano! Tenha um bom dia.']
chats += ['Kurosawa Mushroom?', 'Claro! Deliciosos Cogumelos de Bauru!']
chats += ['Orientador UNESP?', 'Professor Dorival']

#manda a robo treinar com o vocabulario inicial
print("> Iniciando vocabulário neural........: " + str(datetime.now()))


# Create a new trainer for the chatbot
trainer = ListTrainer(bot)

# Train the chatbot based on the english corpus
trainer.train(chats)

#bot.set_trainer(ListTrainer)
#bot.train(chats) #executa o treino com o vocabulario fornecido

###
###treino alternativo
#x = 0
#y = len(chats)
#while x < y:
#	print (chats[x] + " - " + chats[x+1])
#	bot.train([chats[x], chats[x + 1]])
#	x += 2
###

##
#tratamento de voz
voz = fala.init('sapi5')
ids = voz.getProperty('voices') #vozes disponiveis

rate = voz.getProperty('rate') #velocidade
print("> Velocidade de fala..................: " + str(rate))
voz.setProperty('rate', rate + 45) #ajusta velocidade da voz, buscando algo mais 'natural' +20

volume = voz.getProperty('volume')
print("> Volume de voz.......................: " + str(volume))
voz.setProperty('volume', 2.0) #ajusta o volume maximo
###			


###funcao de visao computacional
def cv():
	
	#Iniciamos camera
	captura = cv2.VideoCapture(0)
	 
	while(1):
		 
		#Captura img em RGB -> HSV
		_, imagen = captura.read()
		hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
	 
		#Faixa de cores desejadas
		verde_baixos = np.array([49, 50, 50], dtype=np.uint8) #49 50 50
		verde_altos = np.array([80, 255, 255], dtype=np.uint8) # 80 255 255
	 
		#mascara com essa faixa de cores
		mask = cv2.inRange(hsv, verde_baixos, verde_altos)
	 
		#encontrar a area onde o objeto esta
		moments = cv2.moments(mask)
		area = moments['m00']
	 
		if(area > 200000):
			 
			#centro do objeto detectado
			x = int(moments['m10']/moments['m00'])
			y = int(moments['m01']/moments['m00'])
			 
			#Mostramos coordenadas
			#print ("x = ", x)
			#print ("y = ", y)
	 
			#retangulo de detecção
			cv2.rectangle(imagen, (x-5, y-5), (x+5, y+5),(0,0,255), 2)
			cv2.putText(imagen, "pos x,y:"+ str(x)+","+str(y), (x+10,y+10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1) #cv2.FONT_HERSHEY_SIMPLEX
		 
		#mascara x original
		##cv2.imshow('mask', mask)
		cv2.imshow('Câmera Atual do Dispositivo', imagen)				
		
		#tecla = cv2.waitKey(5) & 0xFF  = shutdown
		if cv2.waitKey(1) & 0xFF == ord('q'):
			captura.release()
			break
	
	#libera janela	
	cv2.destroyAllWindows()
###----

#Loop robotico
#inicia captura de audio
with sr.Microphone() as s: 
	#limpa ruidos
	rec.adjust_for_ambient_noise (s)	

	#loop de dialogo
	while True: 
		if (n == 0):
			print("\n\n||||| INICIANDO GALÁTEA - MODELO COMPUTACIONAL ||||| ... [modo log] ...\n\n")
			
			voz.say("Oi Eu sou a modelo computacional GALÁTEA, vamos conversar?")
			voz.runAndWait()
        
        ##estrutura de ssegurança do bloco de executação, tratando exceções
		try:
			time = datetime.now()
			winsound.Beep(2200, 30)
			print('ouvindo......: ' + str(time))
			
            #captura o audio
			rec.adjust_for_ambient_noise(s)
            
			audio = rec.listen(s) 
			
            
			time = time.now()
            
			print('processando..: ' + str(time))
			winsound.Beep(1000, 30)
			
			#processa via google open
			#call api google para pt-br/en on-line only
			#audio_capt = rec.recognize_google(audio, language='pt') #, key="AIzaSyC89xR_JvtkoO-9-LcXMex5NEhLUAB49MU") #language='pt_BR') #topmaster-30db4@appspot.gserviceaccount.com #, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")
			audio_capt = rec.recognize_google(audio, language='pt-br')
            
			time = datetime.now()
			print('respondendo..: ' + str(time) + '\n')
			
		except sr.UnknownValueError:
			voz.say("Desculpe. Eu nao consegui compreender...")
			voz.runAndWait()
			n += 1
			continue
			
		except sr.RequestError as e:
			voz.say("Desculpe. Mas estamos sem conexao no momento...")
			voz.runAndWait()
			n += 1
			continue
			
		except (KeyboardInterrupt, EOFError, SystemExit):
			voz.say("Desculpe. Identifiquei um desligamento inesperado.")
			voz.runAndWait()
			print("\n\n||||| DESLIGANDO GALATEA - MODELO COMPUTACIONAL ||||| \n||||| Andre Medeiros ")
			exit()	
			
		#lib sphinx para english off-line, em portuguese ainda em desenolvimento, assim que lançada permitirá que façamos a tradução off-line
		#audio_capt = rec.recognize_sphinx (audio)		

		#imprime o que foi dito
		print ("Ser humano diz ... ->   " + audio_capt + "\n")
		
		#upper pra facilitar os ifs
		audio_capt = audio_capt.upper()
        			
		
        ###
		###tratamento de ações executadas 
		###
		
		#verifica o que foi dito e executa ação WINDOWS (você pode definir palavras chaves pra suas próprias ações
		if (audio_capt.find('DESLIGAR') >= 0): 
			print("\n\n||||| DESLIGANDO GALATEA - MODELO COMPUTACIONAL ||||| \n||||| Andre Medeiros ") # + str(n)+ "\n")
			voz.say("Desligando...")
			voz.runAndWait()	

			#fim dialogo
			exit()  
		
		if (audio_capt.find('YOUTUBE') >= 0): 
			busca = audio_capt[audio_capt.find('YOUTUBE')+8:]
			print ("\nAção executada: Procurando videos com o tema... " + busca + "\n")
			
			#abre o caminho/path
			os.startfile("https://www.youtube.com/results?search_query=" + busca)
			action = 1
			
		if (audio_capt.find('OUTLOOK') >= 0): 
			print ("\nAção executada: Abrindo e-mail...\n")
			os.startfile("Outlook.exe")
			action = 1
		
		#if (audio_capt.find('GMAIL') >= 0): 
		#	print ("\nAção executada: Abrindo Gmail...\n")
		#	os.startfile("http://gmail.com")
		#	action = 1
			
		if (audio_capt.find('CBN') >= 0): 
			print ("\nAção executada: Abrindo radio on-line...\n")
			os.startfile("http://cbn.globoradio.globo.com/servicos/estudio-ao-vivo/ESTUDIO-AO-VIVO.htm?praca=SP")
			action = 1

		if (audio_capt.find('PESQUIS') >= 0): 
			
			busca = audio_capt[audio_capt.find('PESQUIS') + 9:]
			print ("\nAção executada: Pesquisando no Google sobre... " + busca + "\n")

			#abre o caminho invocando o browser padrao
			os.startfile("https://www.google.com.br/search?hl=pt-BR&q=" + busca)
			action = 1
		
		if (audio_capt.find('PROTHEUS') >= 0) or (audio_capt.find('PROTEUS') >= 0) or (audio_capt.find('PRO TEUS') >= 0): 
			
			print ("\nAção executada: Executando Software TOTVS...\n")

			#abre o caminho, usando o .lnk por uma questao de compatibilidade > verificar modelo melhor depois
			os.startfile("C:\TOTVSOPV12.lnk")				
			action = 1
		
		if (audio_capt.find('TEMPO') >= 0) or (audio_capt.find('CLIMA') >= 0): 
			
			print ("\nAção executada: Verificando as condições climáticas...\n" )	
            #abre o caminho invocando o browser padrao
			os.startfile("https://www.ipmetradar.com.br/")			
			action = 1
        
		if (audio_capt.find('ATIVAR CAMERA') >= 0) or (audio_capt.find('ATIVAR CÂMERA') >= 0) or (audio_capt.find('ATIVAR A CÂMERA') >= 0): 

			voz.say("Ativando câmera para identificar objetos")
			voz.runAndWait()
			
			###inicia camera 
			cv()
			action = 1
		
		if (audio_capt.find('DIGITE') >= 0): 
			repetir = audio_capt[audio_capt.find('DIGITE')+6:]
			
			print ("\nAção executada: Repetindo a frase ..." + repetir + "\n" )			

			### TESTE - automação com pywinauto - escrever o que foi dito pelo humano num arquivo .txt
			app = Application().start("notepad.exe")			

			# 'digita' o texto capturado pelo audio
			app.UntitledNotepad.Edit.type_keys(repetir, with_spaces = True)			
			###------
						
			#voz.say("Repetindo frase do humano, abre aspas ... " + repetir + "...fecha aspas")
			#voz.runAndWait()
			action = 1

			
		if action == 0: # se nao for uma ação ela processa uma resposta 
			#a robo responde (processo array com palavras já treinadas e ouvidas) - para reiniciar, basta apagar arquivo dbsqlite
			resposta = bot.get_response(audio_capt)
			print ("GALATEA responde ... ->   " + str(resposta) + "\n")
			voz.say(resposta)
			voz.runAndWait()				

		n += 1 #contador
		action = 0 #verifica acoes executadas


