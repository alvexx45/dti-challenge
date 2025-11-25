import React, { useState, useEffect } from 'react';
import './App.css';

const API_URL = 'http://localhost:5000';

function App() {
  const [alunos, setAlunos] = useState([]);
  const [estatisticas, setEstatisticas] = useState(null);
  const [alunosAtencao, setAlunosAtencao] = useState([]);
  const [novoAluno, setNovoAluno] = useState('');
  const [alunoSelecionado, setAlunoSelecionado] = useState(null);
  const [notas, setNotas] = useState(['', '', '', '', '']);
  const [frequencia, setFrequencia] = useState('');
  const [mensagem, setMensagem] = useState({ texto: '', tipo: '' });

  useEffect(() => {
    carregarDados();
  }, []);

  const carregarDados = async () => {
    try {
      const [alunosRes, estatRes, atencaoRes] = await Promise.all([
        fetch(`${API_URL}/alunos`),
        fetch(`${API_URL}/estatisticas/media-turma`),
        fetch(`${API_URL}/estatisticas/alunos-atencao`)
      ]);

      if (alunosRes.ok) setAlunos(await alunosRes.json());
      if (estatRes.ok) setEstatisticas(await estatRes.json());
      if (atencaoRes.ok) setAlunosAtencao(await atencaoRes.json());
    } catch (error) {
      mostrarMensagem('Erro ao carregar dados. Backend inativo.', 'erro');
    }
  };

  const mostrarMensagem = (texto, tipo) => {
    setMensagem({ texto, tipo });
    setTimeout(() => setMensagem({ texto: '', tipo: '' }), 3000);
  };

  const adicionarAluno = async (e) => {
    e.preventDefault();
    if (!novoAluno.trim()) {
      mostrarMensagem('Digite o nome do aluno', 'erro');
      return;
    }

    try {
      const res = await fetch(`${API_URL}/alunos`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nome: novoAluno })
      });

      if (res.ok) {
        mostrarMensagem('Aluno adicionado com sucesso!', 'sucesso');
        setNovoAluno('');
        carregarDados();
      } else {
        const erro = await res.json();
        mostrarMensagem(erro.error || 'Erro ao adicionar aluno', 'erro');
      }
    } catch (error) {
      mostrarMensagem('Erro ao conectar com o servidor', 'erro');
    }
  };

  const removerAluno = async (nome) => {
    if (!window.confirm(`Deseja realmente remover ${nome}?`)) return;

    try {
      const res = await fetch(`${API_URL}/alunos/${encodeURIComponent(nome)}`, {
        method: 'DELETE'
      });

      if (res.ok) {
        mostrarMensagem('Aluno removido com sucesso!', 'sucesso');
        setAlunoSelecionado(null);
        carregarDados();
      }
    } catch (error) {
      mostrarMensagem('Erro ao remover aluno', 'erro');
    }
  };

  const selecionarAluno = (aluno) => {
    setAlunoSelecionado(aluno);
    setNotas(aluno.notas.map(n => n.toString()));
    setFrequencia(aluno.frequencia.toString());
  };

  const atualizarNotas = async (e) => {
    e.preventDefault();
    if (!alunoSelecionado) return;

    const notasNum = notas.map(n => parseFloat(n) || 0);
    if (notasNum.some(n => n < 0 || n > 10)) {
      mostrarMensagem('Notas devem estar entre 0 e 10', 'erro');
      return;
    }

    try {
      const res = await fetch(`${API_URL}/alunos/${encodeURIComponent(alunoSelecionado.nome)}/notas`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ notas: notasNum })
      });

      if (res.ok) {
        mostrarMensagem('Notas atualizadas!', 'sucesso');
        carregarDados();
      }
    } catch (error) {
      mostrarMensagem('Erro ao atualizar notas', 'erro');
    }
  };

  const atualizarFrequencia = async (e) => {
    e.preventDefault();
    if (!alunoSelecionado) return;

    const freq = parseFloat(frequencia);
    if (isNaN(freq) || freq < 0 || freq > 100) {
      mostrarMensagem('Frequência deve estar entre 0 e 100', 'erro');
      return;
    }

    try {
      const res = await fetch(`${API_URL}/alunos/${encodeURIComponent(alunoSelecionado.nome)}/frequencia`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ frequencia: freq })
      });

      if (res.ok) {
        mostrarMensagem('Frequência atualizada!', 'sucesso');
        carregarDados();
      }
    } catch (error) {
      mostrarMensagem('Erro ao atualizar frequência', 'erro');
    }
  };

  return (
    <div className="App">
      {mensagem.texto && (
        <div className={`mensagem ${mensagem.tipo}`}>
          {mensagem.texto}
        </div>
      )}

      <div className="container">
        <div className="card estatisticas">
          <h2>📊 Estatísticas da Turma</h2>
          {estatisticas && (
            <div>
              <p><strong>Média Geral:</strong> {estatisticas.media_geral}</p>
              <div className="disciplinas">
                <h3>Média por Disciplina:</h3>
                {estatisticas.medias_por_disciplina.map((media, idx) => (
                  <div key={idx} className="disciplina">
                    <span>Disciplina {idx + 1}:</span>
                    <span className="nota">{media}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {alunosAtencao.alunos_atencao_especial?.length > 0 && (
          <div className="card atencao">
            <h2>⚠️ Alunos que Precisam de Atenção</h2>
            <div className="lista-atencao">
              {alunosAtencao.alunos_atencao_especial.map((aluno, idx) => (
                <div key={idx} className="aluno-atencao">
                  <strong>{aluno.nome}</strong>
                  <ul>
                    {aluno.motivos.map((motivo, i) => (
                      <li key={i}>{motivo}</li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="card">
          <h2>➕ Adicionar Aluno</h2>
          <form onSubmit={adicionarAluno}>
            <input
              type="text"
              placeholder="Nome do aluno"
              value={novoAluno}
              onChange={(e) => setNovoAluno(e.target.value)}
            />
            <button type="submit">Adicionar</button>
          </form>
        </div>

        <div className="card">
          <h2>👥 Lista de Alunos ({alunos.length})</h2>
          <div className="lista-alunos">
            {alunos.map((aluno, idx) => (
              <div
                key={idx}
                className={`aluno-item ${alunoSelecionado?.nome === aluno.nome ? 'selecionado' : ''}`}
                onClick={() => selecionarAluno(aluno)}
              >
                <div className="aluno-info">
                  <strong>{aluno.nome}</strong>
                  <div className="aluno-stats">
                    <span>Média: {aluno.media}</span>
                    <span>Frequência: {aluno.frequencia}%</span>
                  </div>
                </div>
                <button
                  className="btn-remover"
                  onClick={(e) => {
                    e.stopPropagation();
                    removerAluno(aluno.nome);
                  }}
                >
                  🗑️
                </button>
              </div>
            ))}
          </div>
        </div>

        {alunoSelecionado && (
          <div className="card edicao">
            <h2>✏️ Editando: {alunoSelecionado.nome}</h2>
            
            <form onSubmit={atualizarNotas}>
              <h3>Notas (0 a 10)</h3>
              <div className="notas-grid">
                {notas.map((nota, idx) => (
                  <div key={idx} className="nota-input">
                    <label>Disciplina {idx + 1}:</label>
                    <input
                      type="number"
                      step="0.1"
                      min="0"
                      max="10"
                      value={nota}
                      onChange={(e) => {
                        const newNotas = [...notas];
                        newNotas[idx] = e.target.value;
                        setNotas(newNotas);
                      }}
                    />
                  </div>
                ))}
              </div>
              <button type="submit">Salvar Notas</button>
            </form>

            <form onSubmit={atualizarFrequencia}>
              <h3>Frequência (0 a 100%)</h3>
              <input
                type="number"
                step="0.1"
                min="0"
                max="100"
                value={frequencia}
                onChange={(e) => setFrequencia(e.target.value)}
                placeholder="Frequência em %"
              />
              <button type="submit">Salvar Frequência</button>
            </form>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
