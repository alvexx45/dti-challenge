from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import List, Dict
import statistics

app = Flask(__name__)
CORS(app)

# estrutura de dados para armazenar informações dos alunos
alunos_data = {}

class Aluno:
    def __init__(self, nome: str):
        self.nome = nome
        self.notas = [0.0] * 5  # 5 disciplinas
        self.frequencia = 0.0
    
    def calcular_media(self) -> float:
        return sum(self.notas) / len(self.notas) if self.notas else 0.0
    
    def to_dict(self) -> Dict:
        return {
            'nome': self.nome,
            'notas': self.notas,
            'frequencia': self.frequencia,
            'media': round(self.calcular_media(), 2)
        }


# rotas da API

@app.route('/alunos', methods=['GET'])
def listar_alunos():
    """Lista todos os alunos"""
    return jsonify([aluno.to_dict() for aluno in alunos_data.values()])


@app.route('/alunos', methods=['POST'])
def adicionar_aluno():
    data = request.get_json()
    nome = data.get('nome')
    
    if not nome:
        return jsonify({'error': 'Nome é obrigatório'}), 400
    
    if nome in alunos_data:
        return jsonify({'error': 'Aluno já existe'}), 400
    
    alunos_data[nome] = Aluno(nome)
    return jsonify(alunos_data[nome].to_dict()), 201


@app.route('/alunos/<nome>', methods=['GET'])
def obter_aluno(nome):
    aluno = alunos_data.get(nome)
    if not aluno:
        return jsonify({'error': 'Aluno não encontrado'}), 404
    
    return jsonify(aluno.to_dict())


@app.route('/alunos/<nome>', methods=['DELETE'])
def remover_aluno(nome):
    if nome not in alunos_data:
        return jsonify({'error': 'Aluno não encontrado'}), 404
    
    del alunos_data[nome]
    return jsonify({'message': 'Aluno removido com sucesso'}), 200


@app.route('/alunos/<nome>/notas', methods=['PUT'])
def atualizar_notas(nome):
    aluno = alunos_data.get(nome)
    if not aluno:
        return jsonify({'error': 'Aluno não encontrado'}), 404
    
    data = request.get_json()
    notas = data.get('notas', [])
    
    if len(notas) != 5:
        return jsonify({'error': 'Devem ser fornecidas exatamente 5 notas'}), 400
    
    # Valida se todas as notas estão entre 0 e 10
    for nota in notas:
        if not isinstance(nota, (int, float)) or nota < 0 or nota > 10:
            return jsonify({'error': 'Notas devem estar entre 0 e 10'}), 400
    
    aluno.notas = notas
    return jsonify(aluno.to_dict())


@app.route('/alunos/<nome>/frequencia', methods=['PUT'])
def atualizar_frequencia(nome):
    aluno = alunos_data.get(nome)
    if not aluno:
        return jsonify({'error': 'Aluno não encontrado'}), 404
    
    data = request.get_json()
    frequencia = data.get('frequencia')
    
    if frequencia is None:
        return jsonify({'error': 'Frequência é obrigatória'}), 400
    
    if not isinstance(frequencia, (int, float)) or frequencia < 0 or frequencia > 100:
        return jsonify({'error': 'Frequência deve estar entre 0 e 100'}), 400
    
    aluno.frequencia = frequencia
    return jsonify(aluno.to_dict())


@app.route('/estatisticas/media-turma', methods=['GET'])
def calcular_media_turma():
    if not alunos_data:
        return jsonify({'error': 'Nenhum aluno cadastrado'}), 404
    
    medias_disciplinas = []
    
    for i in range(5):  # 5 disciplinas
        notas_disciplina = [aluno.notas[i] for aluno in alunos_data.values()]
        media = sum(notas_disciplina) / len(notas_disciplina) if notas_disciplina else 0.0
        medias_disciplinas.append(round(media, 2))
    
    return jsonify({
        'medias_por_disciplina': medias_disciplinas,
        'media_geral': round(sum(medias_disciplinas) / len(medias_disciplinas), 2)
    })


@app.route('/estatisticas/alunos-acima-media', methods=['GET'])
def alunos_acima_media():
    if not alunos_data:
        return jsonify({'error': 'Nenhum aluno cadastrado'}), 404
    
    # Calcula a média geral da turma
    todas_medias = [aluno.calcular_media() for aluno in alunos_data.values()]
    media_turma = statistics.mean(todas_medias)
    
    # Filtra alunos acima da média
    alunos_destaque = [
        {
            **aluno.to_dict(),
            'diferenca_media': round(aluno.calcular_media() - media_turma, 2)
        }
        for aluno in alunos_data.values()
        if aluno.calcular_media() > media_turma
    ]
    
    return jsonify({
        'media_turma': round(media_turma, 2),
        'alunos_acima_media': alunos_destaque,
        'quantidade': len(alunos_destaque)
    })


@app.route('/estatisticas/alunos-baixa-frequencia', methods=['GET'])
def alunos_baixa_frequencia():
    if not alunos_data:
        return jsonify({'error': 'Nenhum aluno cadastrado'}), 404
    
    alunos_atencao = [
        aluno.to_dict()
        for aluno in alunos_data.values()
        if aluno.frequencia < 75
    ]
    
    return jsonify({
        'limite_frequencia': 75,
        'alunos_baixa_frequencia': alunos_atencao,
        'quantidade': len(alunos_atencao)
    })


@app.route('/estatisticas/alunos-atencao', methods=['GET'])
def alunos_atencao_especial():
    if not alunos_data:
        return jsonify({'error': 'Nenhum aluno cadastrado'}), 404
    
    # calcular media da turma
    todas_medias = [aluno.calcular_media() for aluno in alunos_data.values()]
    media_turma = statistics.mean(todas_medias)
    
    alunos_atencao = []
    
    for aluno in alunos_data.values():
        motivos = []
        if aluno.frequencia < 75:
            motivos.append(f'Frequência baixa: {aluno.frequencia}%')
        if aluno.calcular_media() < media_turma:
            motivos.append(f'Média abaixo da turma: {aluno.calcular_media():.2f}')
        
        if motivos:
            alunos_atencao.append({
                **aluno.to_dict(),
                'motivos': motivos
            })
    
    return jsonify({
        'media_turma': round(media_turma, 2),
        'alunos_atencao_especial': alunos_atencao,
        'quantidade': len(alunos_atencao)
    })


@app.route('/relatorio-completo', methods=['GET'])
def relatorio_completo():
    """Retorna um relatório completo com todas as estatísticas"""
    if not alunos_data:
        return jsonify({'error': 'Nenhum aluno cadastrado'}), 404
    
    # medias por disciplina
    medias_disciplinas = []
    for i in range(5):
        notas_disciplina = [aluno.notas[i] for aluno in alunos_data.values()]
        media = sum(notas_disciplina) / len(notas_disciplina) if notas_disciplina else 0.0
        medias_disciplinas.append(round(media, 2))
    
    # media geral da turma
    todas_medias = [aluno.calcular_media() for aluno in alunos_data.values()]
    media_turma = statistics.mean(todas_medias)
    
    # frequência media da turma
    frequencia_media = statistics.mean([aluno.frequencia for aluno in alunos_data.values()])
    
    return jsonify({
        'total_alunos': len(alunos_data),
        'medias_por_disciplina': medias_disciplinas,
        'media_geral_turma': round(media_turma, 2),
        'frequencia_media_turma': round(frequencia_media, 2),
        'alunos': [aluno.to_dict() for aluno in alunos_data.values()]
    })


@app.route('/', methods=['GET'])
def home():
    """Rota inicial com informações da API"""
    return jsonify({
        'message': 'Sistema de Gerenciamento de Notas e Frequência',
        'versao': '1.0',
        'endpoints': {
            'GET /': 'Informações da API',
            'GET /alunos': 'Lista todos os alunos',
            'POST /alunos': 'Adiciona um novo aluno',
            'GET /alunos/<nome>': 'Obtém informações de um aluno',
            'DELETE /alunos/<nome>': 'Remove um aluno',
            'PUT /alunos/<nome>/notas': 'Atualiza notas de um aluno',
            'PUT /alunos/<nome>/frequencia': 'Atualiza frequência de um aluno',
            'GET /estatisticas/media-turma': 'Média da turma por disciplina',
            'GET /estatisticas/alunos-acima-media': 'Alunos acima da média',
            'GET /estatisticas/alunos-baixa-frequencia': 'Alunos com frequência < 75%',
            'GET /estatisticas/alunos-atencao': 'Alunos que precisam de atenção',
            'GET /relatorio-completo': 'Relatório completo da turma'
        }
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
