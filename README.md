# 📚 Sistema de Gerenciamento de Notas e Frequência

Sistema de gerenciamento de notas e frequência de alunos.

## 🎯 Objetivo

Organize e acompanhar:
- Notas dos alunos em 5 disciplinas (0 a 10)
- Frequência de cada aluno (0 a 100%)
- Médias individuais e da turma
- Identificação automática de alunos que precisam de atenção especial

## 🏗️ Arquitetura

### Backend (Python/Flask)
- API RESTful completa
- Gerenciamento de alunos, notas e frequências
- Cálculos automáticos de médias
- Estatísticas e relatórios
- CORS para integração com frontend

### Frontend (React)
- Estatísticas em tempo real
- Alertas visuais para alunos em situação de atenção

## 🚀 Instalação e Execução

### Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

O backend rodará em `http://localhost:5000`

### Frontend

```bash
cd frontend
npm install
npm start
```

O frontend rodará em `http://localhost:3000`

## 📁 Estrutura do Projeto

```
dti-challenge/
├── backend/
│   ├── app.py              # API Flask
│   ├── requirements.txt    # Dependências Python
│   └── README.md           # Documentação do backend
├── frontend/
│   ├── src/
│   │   ├── App.js          # Componente principal
│   │   ├── App.css         # Estilos
│   │   └── index.js        # Ponto de entrada
│   ├── package.json        # Dependências Node
│   └── README.md           # Documentação do frontend
└── README.md               # Este arquivo
```

## 🔗 Endpoints da API

- `GET /alunos` - Lista todos os alunos
- `POST /alunos` - Adiciona novo aluno
- `GET /alunos/<nome>` - Obtém dados de um aluno
- `DELETE /alunos/<nome>` - Remove um aluno
- `PUT /alunos/<nome>/notas` - Atualiza notas
- `PUT /alunos/<nome>/frequencia` - Atualiza frequência
- `GET /estatisticas/media-turma` - Média por disciplina
- `GET /estatisticas/alunos-acima-media` - Alunos acima da média
- `GET /estatisticas/alunos-baixa-frequencia` - Alunos com frequência < 75%
- `GET /estatisticas/alunos-atencao` - Alunos que precisam de atenção
- `GET /relatorio-completo` - Relatório completo