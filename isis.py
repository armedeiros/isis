#Prof. Dr. DORIVAL ROSSI
#Prof. Dr. FERNANDO MARAR
#ANDRE MEDEIROS (mestrando)
#UNESP BAURU

### todas as libs necessarias em ordem, 
### os prints dos imports podem ser removidos, servem apenas para verificar o tempo de carga
### os beeps servem de alerta e também são opcionais
### o código preza pela simplicidade para ser acessível a todos os públicos

import sys #recursos sistema
import os #recursos sistema operacional
import numpy as np #cientifica matematica
import winsound ##recursos windows de som, para avisar os processos em andamento (carga, escuta, resposta)

from datetime import datetime #recursos de data
from pywinauto.application import Application  #automacao de telas/processos windows (trabalha na camada de mensagens do sistema operacional)
import string #texto

winsound.Beep(2200, 30)

print("\n> Importando recursos de fala.........: " + str(datetime.now()))
import pyttsx3 as fala #conversao de texto pra audio
winsound.Beep(2200, 30)

print("> Importando recursos de recognição...: " + str(datetime.now()))
import speech_recognition as sr #reconhecimento de fala com i.a
winsound.Beep(2200, 30)

print("> Importando recursos de conversação..: " + str(datetime.now()))
from chatterbot import ChatBot #recursos de chatbot com i.a
from chatterbot.trainers import ListTrainer 
from chatterbot.trainers import ChatterBotCorpusTrainer
winsound.Beep(2200, 30)

print("> Importando recursos de visão comput.: " + str(datetime.now()))
import cv2 #visao computacional
winsound.Beep(2200, 30)
####

### vars iniciais
n      = 0 #contador
dtnas  = "2020-03-03 13:33:00.000000" # dt de 'nascimento'
action = 0 #define ação

rec   = sr.Recognizer() #tratamento do reconhecimento de fala
###

###tratamento da robo
##bot = ChatBot('ISIS') #inicia o Bot no ambiente

bot = ChatBot('ISIS', 
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        #'chatterbot.logic.TimeLogicAdapter',
        'chatterbot.logic.BestMatch',
        ],
    #filters=[filters.get_recent_repeated_responses]
    database_uri='sqlite:///database.db'
)
###

winsound.Beep(2200, 30)

#carga inicial de vocabulario, aqui deve-se incluir aquele que for mais apropriado para necessidade
#pode ser arquivos com frases ou direcionado pra ações especificas
chats =  ['Como vai?', 'Tudo legal','Voce pode me ajudar?', 'Claro que posso! Diga?', 'Voce Conhece ÍSIS?', 'Ouvi dizer que esse software eh muito bom!', 'Radio', 'Noticias sao importantes', 'Qual seu nome?', 'Me chamo ÍSIS muito prazer em conhecer voce']
chats += ['Oi!', 'Olah Pessoa Humana!', 'O dia esta bom','Dias assim sao bons', 'Voce sabe sobre muita coisa?', 'Posso aprender se voce me ensinar', 'Como voce se chama?', 'Me chamam de ÍSIS.', 'Quantos anos voce tem?', 'Eu nao tenho idade...']
chats += ['Voce gosta?','Gosto nao se discute', 'Ja ouviu falar?', 'Depende, posso pesquisar...']
chats += ['Desligar', 'Ja vai? Ateh logo!', 'Voce sabe se vai chover amanha?', 'Vamos ver o clima...']
chats += ['Entender', 'Sempre refletindo', 'Bom dia', 'Olah ser humano! Tenha um bom dia.']
chats += ['Orientador UNESP?', 'Professor Dorival']

#manda a robo treinar com o vocabulario inicial
print("> Iniciando vocabulário neural........: " + str(datetime.now()))

# treinamento do bot
trainer = ListTrainer(bot)
trainer.train(chats)

###exemplos de treinos alternativos
#trainer = ChatterBotCorpusTrainer(ChatBot)
#trainer.train(chats)
#trainer.train("chatterbot.corpus.english") portuguese

#bot.set_trainer(ListTrainer)
#bot.train(chats) #executa o treino com o vocabulario fornecido

##

#tratamento de voz
voz = fala.init('sapi5')
ids = voz.getProperty('voices') #vozes disponiveis

rate = voz.getProperty('rate') #velocidade
print("> Velocidade de fala..................: " + str(rate))
voz.setProperty('rate', rate + 45) #ajusta velocidade da voz, buscando algo mais 'natural' +20

volume = voz.getProperty('volume')
print("> Volume de voz.......................: " + str(volume))
voz.setProperty('volume', 5.0) #ajusta o volume maximo
###			


###funcao de visao computacional simples para detecção de objetos cor verde, também pode-se alterar para a necessidade em especifico
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

#Loop 'robótico'
#inicia captura de audio
with sr.Microphone() as s: 

	#limpa ruido
	rec.adjust_for_ambient_noise (s)	

	#loop de dialogo
	while True: 
		rec.adjust_for_ambient_noise(s)    
		if (n == 0):
			print("\n\n||||| INICIANDO ÍSIS - PROTÓTIPO COMPUTACIONAL MAKER ||||| ... [modo log] ...\n\n")
			
			voz.say("Oi Eu sou a PROTÓTIPO ÍSIS, como posso ajudar?")
			voz.runAndWait()
        
        ##estrutura de ssegurança do bloco de executação, tratando exceções
		try:
			time = datetime.now()

			print('ouvindo......: ' + str(time))
			winsound.Beep(2200, 30)			
            
            #captura o audio
			rec.adjust_for_ambient_noise(s)
            
			audio = rec.listen(s) 
			           
			time = time.now()
            
			print('processando..: ' + str(time))
			winsound.Beep(1000, 30)
			#processa via google open
			#call api para idioma pt-br/en 
            #existem outras formas e calls, pode-se alterar caso necessário
            #exemplo:
            #lib sphinx para off-line, em pt-br ainda em testes/desenvolvimento
            #audio_capt = rec.recognize_sphinx (audio)		
			audio_capt = rec.recognize_google(audio, language='pt') 
            
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
			print("\n\n||||| DESLIGANDO ÍSIS - PROTÓTIPO COMPUTACIONAL MAKER ||||| \n||||| Andre Medeiros ")
			exit()	
			
		
		#imprime o que foi dito
		print ("Ser humano diz ... ->   " + audio_capt + "\n")
		
		#upper pra facilitar os ifs
		audio_capt = audio_capt.upper()
        			
		
        ###
		###tratamento de ações executadas pelo protótipo, pode-se incluir quantas desejar 
		###
		
		#verifica o que foi dito e executa ação em WINDOWS (você pode definir palavras chaves pra suas próprias ações e também outros sistemas operacionais)
		if (audio_capt.find('DESLIGAR') >= 0): 
			print("\n\n||||| DESLIGANDO ÍSIS - PROTÓTIPO COMPUTACIONAL MAKER ||||| \n||||| Andre Medeiros ") # + str(n)+ "\n")
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
		
		if (audio_capt.find('GMAIL') >= 0): 
			print ("\nAção executada: Abrindo Gmail...\n")
			os.startfile("http://gmail.com")
			action = 1
			
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
						
			action = 1

			
		if action == 0: # se nao for uma ação ela processa uma resposta 
			#a robo responde (processo array com palavras já treinadas e ouvidas) - para reiniciar vocabulário, basta apagar arquivo dbsqlite
			resposta = bot.get_response(audio_capt)
			print ("ISIS responde ... ->   " + str(resposta) + "\n")
			voz.say(resposta)
			voz.runAndWait()				

		n += 1 #contador
		action = 0 #verifica acoes executadas


