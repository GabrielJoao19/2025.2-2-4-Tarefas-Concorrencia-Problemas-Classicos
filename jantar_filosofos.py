import threading
import time
import random

# Configurações do Problema
NUM_FILOSOFOS = 5
REFEICOES_PARA_SACIAR = 3

class Filosofo(threading.Thread):
    def __init__(self, id, talher_esq, talher_dir):
        super().__init__()
        self.id = id
        self.talher_esq = talher_esq
        self.talher_dir = talher_dir
        self.refeicoes = 0

    def pensar(self):
        print(f" Filósofo {self.id} está pensando...")
        time.sleep(random.uniform(0.5, 1.5))

    def comer(self):
        print(f" Filósofo {self.id} está COMENDO (refeição {self.refeicoes + 1})")
        time.sleep(random.uniform(1, 2))
        self.refeicoes += 1

    def run(self):
        """Ciclo de vida do filósofo na thread"""
        while self.refeicoes < REFEICOES_PARA_SACIAR:
            self.pensar()

            # --- ESTRATÉGIA DE PREVENÇÃO DE DEADLOCK ---
            # Ordenamos os talheres pelo índice para evitar espera circular.
            # Cada filósofo sempre tentará pegar o talher de menor número primeiro.
            id_primeiro = min(self.talher_esq, self.talher_dir)
            id_segundo = max(self.talher_esq, self.talher_dir)

            print(f" Filósofo {self.id} quer os talheres {id_primeiro} e {id_segundo}")

            # Usamos os Locks dos talheres globais
            with lista_talheres[id_primeiro]:
                with lista_talheres[id_segundo]:
                    self.comer()
            
            print(f" Filósofo {self.id} soltou os talheres e voltou a pensar.")

# Criamos os 5 Locks globais (um para cada talher na mesa)
lista_talheres = [threading.Lock() for _ in range(NUM_FILOSOFOS)]

def main():
    print("="*40)
    print("INICIANDO O JANTAR DOS FILÓSOFOS")
    print("="*40)

    # Inicializamos os filósofos
    filosofos = []
    for i in range(NUM_FILOSOFOS):
        # O filósofo i senta entre o talher i e o (i+1)%5
        f = Filosofo(i, i, (i + 1) % NUM_FILOSOFOS)
        filosofos.append(f)

    # Disparamos as threads
    for f in filosofos:
        f.start()

    # Aguardamos todos terminarem
    for f in filosofos:
        f.join()

    print("\n" + "="*40)
    print("JANTAR FINALIZADO COM SUCESSO!")
    print("="*40)

if __name__ == "__main__":
    main()