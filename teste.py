def update(self):
	deltaTime = Time.currentTime - Persistence.loadState().lastTime
	
	# máquina de estados do vpet
	if (state == 'normal'):
		# taxas estão relacionadas ao estado atual do Pet
		hungerRate = 5; healthRate = 4; happyRate = 3
		# atualiza itens de status (versão "muito simples")
		hunger = hunger - (hungerRate * random.uniform(0.8, 1.2)) * deltaTime
		health = health - (healthRate * random.uniform(0.9, 1.1)) * deltaTime
		happy = happy - (happyRate * random.uniform(0.85, 1.15)) * deltaTime
	
		# atualiza estados
		if (self.happy < 25):
			state = 'triste'
		elif(self.health < 25):
			state = 'doente'
		elif(self.hunger < 60):
			state = 'faminto'
		elif(self.happy <= 0 or self.health <= 0 or self.hunger <= 0):
			self.state = 'morto'
	
	# else ... // if (state == 'sick') ... outros estados

	# atualiza desenho do pet e ícones na tela
	self.updateGraphics()
	# salva estado: barras de status (number), estado (string) e hora (number)
	Persistence.saveState(hunger, health, happy, state, Time.currentTime)

