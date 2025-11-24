from flask import Flask, render_template, request, session, redirect, url_for
from collections import Counter

app = Flask(__name__)

# --- CONFIGURAÇÃO DA SESSÃO ---
app.secret_key = 'chave_secreta_do_tesouro_pirata'

# --- DADOS DO QUIZ ---

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

# --- PERFIS DE RESULTADO ---
# Nota: Atualizei os caminhos das imagens para bater com o print da sua pasta local.

perfis_homem = {
    "A": {
        "nome": "Barba Negra (Edward Teach)", 
        "desc": "Você é o terror dos sete mares. Usa o medo como arma e não tem piedade. Sua presença incendeia o convés.", 
        "img": "/static/img/barba_negra.jpg"
    },
    "B": {
        "nome": "Bartholomew Roberts", 
        "desc": "Um líder nato, elegante e organizado. Você prefere códigos de conduta e disciplina, mas é letal em combate.", 
        "img": "/static/img/bartholomew_roberts.jpg"
    },
    "C": {
        "nome": "Henry Morgan", 
        "desc": "Mais do que um pirata, um empresário do crime. Você busca riqueza acima de tudo e sabe como manipular o sistema.", 
        "img": "/static/img/henry_morgan.jpg"
    },
    "D": {
        "nome": "Jack Sparrow", 
        "desc": "Caótico, improvisador e com uma sorte incrível. Ninguém sabe se você é um gênio ou um louco.", 
        "img": "/static/img/jack_sparrow.jpg" 
    },
    "E": {
        "nome": "William Kidd", 
        "desc": "Um estrategista incompreendido. Você tenta seguir as regras, mas o destino sempre o empurra para a pirataria.", 
        "img": "/static/img/william_kidd.jpg"
    },
}

perfis_mulher = {
    "A": {
        "nome": "Anne Bonny", 
        "desc": "Impulsiva, perigosa e feroz. Você luta melhor que qualquer homem e não leva desaforo para casa.", 
        "img": "/static/img/anne_bonny.jpg"
    },
    "B": {
        "nome": "Ching Shih", 
        "desc": "A maior pirata da história. Uma líder suprema, estrategista militar que comandou frotas inteiras com disciplina de ferro.", 
        "img": "/static/img/ching_shih.jpg"
    },
    "C": {
        "nome": "Grace O'Malley", 
        "desc": "A Rainha Pirata. Você luta pela sua família e suas terras. Rica, poderosa e politicamente astuta.", 
        "img": "/static/img/grace_omalley.jpg"
    },
    "D": {
        "nome": "Mary Read", 
        "desc": "Aventureira e mestre dos disfarces. Você vive pela emoção e pela lealdade aos seus poucos amigos verdadeiros.", 
        "img": "/static/img/mary_read.jpg"
    },
    "E": {
        "nome": "Jeanne de Clisson", 
        "desc": "A Leoa da Bretanha. Movida por vingança e justiça, você pinta seus navios de vermelho e caça seus inimigos.", 
        "img": "/static/img/jeanne_de_clisson.jpg"
    }
}

# --- ROTAS DO FLASK ---

@app.route('/')
def index():
    # Limpa a sessão ao entrar na home
    session.clear()
    return render_template('index.html', etapa='inicio')

@app.route('/iniciar', methods=['POST'])
def iniciar():
    session['genero'] = request.form.get('genero')
    session['pergunta_atual_index'] = 0 
    session['respostas'] = [] 
    return redirect(url_for('question'))

@app.route('/question')
def question():
    if 'genero' not in session:
        return redirect(url_for('index'))
        
    indice = session.get('pergunta_atual_index', 0)
    
    if indice < len(perguntas):
        pergunta_da_vez = perguntas[indice]
        progresso = f"Pergunta {indice + 1} de {len(perguntas)}"
        
        return render_template('index.html', 
                               etapa='quiz', 
                               pergunta=pergunta_da_vez,
                               progresso=progresso)
    else:
        return redirect(url_for('resultado_final'))

@app.route('/responder', methods=['POST'])
def responder():
    resposta_escolhida = request.form.get('resposta')
    
    respostas_atuais = session.get('respostas', [])
    respostas_atuais.append(resposta_escolhida)
    session['respostas'] = respostas_atuais
    
    session['pergunta_atual_index'] = session.get('pergunta_atual_index', 0) + 1
    
    return redirect(url_for('question'))

@app.route('/resultado')
def resultado_final():
    respostas = session.get('respostas', [])
    genero = session.get('genero')
    
    if not respostas: 
        return redirect(url_for('index'))

    contagem = Counter(respostas)
    # Pega a letra mais comum. Se houver empate, pega a primeira que aparecer.
    if contagem:
        letra_vencedora = contagem.most_common(1)[0][0]
    else:
        letra_vencedora = 'D' # Fallback caso algo dê muito errado

    if genero == 'homem':
        resultado_final = perfis_homem.get(letra_vencedora, perfis_homem['D'])
    else:
        resultado_final = perfis_mulher.get(letra_vencedora, perfis_mulher['D'])
            
    return render_template('result.html', resultado=resultado_final)

if __name__ == '__main__':
    app.run(debug=True)