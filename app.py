from flask import Flask, render_template, request

app = Flask(__name__)

# --- DADOS DO QUIZ ---

# As perguntas (O value A, B, C, D, E define a personalidade)
perguntas = [
    {
        "id": 1,
        "texto": "Um navio mercante está no horizonte. O que você faz?",
        "opcoes": [
            ("A", "Atacar imediatamente com canhões! Sem piedade."),
            ("B", "Criar uma estratégia para cercá-los e negociar a carga."),
            ("C", "Observar de longe. Só ataco se tiver certeza da vitória."),
            ("D", "Tentar enganá-los hasteando uma bandeira falsa."),
            ("E", "Seguir o navio discretamente até que parem em uma ilha.")
        ]
    },
    {
        "id": 2,
        "texto": "O motim está começando no convés. Sua reação:",
        "opcoes": [
            ("A", "Mato o líder do motim na frente de todos."),
            ("B", "Faço um discurso inspirador para lembrar nossa irmandade."),
            ("C", "Ofereço mais ouro para quem ficar do meu lado."),
            ("D", "Fujo num bote e deixo eles se matarem."),
            ("E", "Desafio o líder para um duelo de espadas justo.")
        ]
    },
    {
        "id": 3,
        "texto": "Você encontrou um mapa do tesouro lendário. Qual o plano?",
        "opcoes": [
            ("A", "Vamos agora! Quem ficar para trás morre."),
            ("B", "Estudo a rota e os perigos antes de partir."),
            ("C", "Guardo segredo e recruto apenas os leais."),
            ("D", "Improviso no caminho, o que importa é a aventura."),
            ("E", "Vendo o mapa. Prefiro ouro na mão do que perigo no mar.")
        ]
    },
    {
        "id": 4,
        "texto": "Sua tripulação está bebendo todo o rum. Você:",
        "opcoes": [
            ("A", "Junto-me a eles! A vida é curta."),
            ("B", "Raciono a bebida. Precisamos de disciplina."),
            ("C", "Deixo beberem, mas cobro o dobro depois."),
            ("D", "Bebo escondido a minha parte melhor."),
            ("E", "Proíbo a bebida até completarmos a missão.")
        ]
    },
    {
        "id": 5,
        "texto": "Uma tempestade terrível se aproxima!",
        "opcoes": [
            ("A", "Enfrento a tempestade gritando contra os deuses!"),
            ("B", "Assumo o leme e dou ordens precisas."),
            ("C", "Calculo a rota de escape mais segura."),
            ("D", "Amarro-me ao mastro e rezo."),
            ("E", "Aproveito a confusão para roubar suprimentos extras.")
        ]
    },
    {
        "id": 6,
        "texto": "Qual é a sua arma de preferência?",
        "opcoes": [
            ("A", "Um machado pesado ou bacamarte."),
            ("B", "Um sabre elegante e rápido."),
            ("C", "Duas pistolas e muita pólvora."),
            ("D", "Qualquer coisa que estiver à mão (garrafa, cadeira)."),
            ("E", "Adaga envenenada escondida na bota.")
        ]
    },
    {
        "id": 7,
        "texto": "O que você mais valoriza na pirataria?",
        "opcoes": [
            ("A", "O poder e o medo que causo."),
            ("B", "A liberdade de não ter rei."),
            ("C", "A riqueza acumulada."),
            ("D", "A fama e as lendas sobre mim."),
            ("E", "A astúcia e a estratégia.")
        ]
    },
    {
        "id": 8,
        "texto": "Se for capturado pela Marinha Real, você...",
        "opcoes": [
            ("A", "Luto até o último suspiro."),
            ("B", "Tento negociar minha liberdade com informações."),
            ("C", "Suborno o guarda."),
            ("D", "Faço uma fuga espetacular e impossível."),
            ("E", "Aceito o destino com honra.")
        ]
    }
]

# Perfis de Piratas (Lógica Python)
# A = Agressivo/Força Bruta
# B = Líder/Carismático
# C = Ganancioso/Calculista
# D = Caótico/Sortudo
# E = Estratégico/Misterioso

perfis_homem = {
    "A": {"nome": "Barba Negra (Edward Teach)", "desc": "Você é o terror dos sete mares. Usa o medo como arma e não tem piedade. Sua presença incendeia o convés.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/Blackbeard_the_Pirate_-_fictional.jpg/250px-Blackbeard_the_Pirate_-_fictional.jpg"},
    "B": {"nome": "Bartholomew Roberts (Black Bart)", "desc": "Um líder nato, elegante e organizado. Você prefere códigos de conduta e disciplina, mas é letal em combate.", "img": "https://upload.wikimedia.org/wikipedia/commons/6/66/Bartholomew_Roberts.JPG"},
    "C": {"nome": "Henry Morgan", "desc": "Mais do que um pirata, um empresário do crime. Você busca riqueza acima de tudo e sabe como manipular o sistema.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Henry_Morgan_in_colour.jpg/220px-Henry_Morgan_in_colour.jpg"},
    "D": {"nome": "Jack Sparrow", "desc": "Caótico, improvisador e com uma sorte incrível. Ninguém sabe se você é um gênio ou um louco.", "img": "https://upload.wikimedia.org/wikipedia/en/a/a2/Jack_Sparrow_In_Pirates_of_the_Caribbean-_At_World%27s_End.JPG"},
    "E": {"nome": "William Kidd", "desc": "Um estrategista incompreendido. Você tenta seguir as regras, mas o destino sempre o empurra para a pirataria.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Captain_William_Kidd_retouched.jpg/220px-Captain_William_Kidd_retouched.jpg"}
}

perfis_mulher = {
    "A": {"nome": "Anne Bonny", "desc": "Impulsiva, perigosa e feroz. Você luta melhor que qualquer homem e não leva desaforo para casa.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Anne_Bonny_color.jpg/220px-Anne_Bonny_color.jpg"},
    "B": {"nome": "Ching Shih", "desc": "A maior pirata da história. Uma líder suprema, estrategista militar que comandou frotas inteiras com disciplina de ferro.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Zheng_Yi_Sao.jpg/220px-Zheng_Yi_Sao.jpg"},
    "C": {"nome": "Grace O'Malley", "desc": "A Rainha Pirata. Você luta pela sua família e suas terras. Rica, poderosa e politicamente astuta.", "img": "https://upload.wikimedia.org/wikipedia/commons/a/a5/Grace_OMalley.jpg"},
    "D": {"nome": "Mary Read", "desc": "Aventureira e mestre dos disfarces. Você vive pela emoção e pela lealdade aos seus poucos amigos verdadeiros.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Mary_Read_color.jpg/220px-Mary_Read_color.jpg"},
    "E": {"nome": "Jeanne de Clisson", "desc": "A Leoa da Bretanha. Movida por vingança e justiça, você pinta seus navios de vermelho e caça seus inimigos.", "img": "https://upload.wikimedia.org/wikipedia/commons/d/d5/Jeanne_de_Belleville.jpg"}
}

@app.route('/')
def index():
    return render_template('index.html', perguntas=perguntas)

@app.route('/resultado', methods=['POST'])
def resultado():
    if request.method == 'POST':
        # 1. Captura o Gênero
        genero = request.form.get('genero')
        
        # 2. Captura as respostas (A, B, C, D ou E)
        respostas = []
        for i in range(1, 9):
            resp = request.form.get(f'q{i}')
            if resp:
                respostas.append(resp)
        
        # 3. Lógica de Contagem (Python puro)
        from collections import Counter
        contagem = Counter(respostas)
        
        # Pega a letra mais comum. Se empate, pega a primeira que aparecer na ordem alfabética
        letra_vencedora = contagem.most_common(1)[0][0] 

        # 4. Define o perfil baseado no gênero
        if genero == 'homem':
            resultado_final = perfis_homem.get(letra_vencedora, perfis_homem['D'])
        else:
            resultado_final = perfis_mulher.get(letra_vencedora, perfis_mulher['D'])
            
        return render_template('result.html', resultado=resultado_final)

if __name__ == '__main__':
    app.run(debug=True)