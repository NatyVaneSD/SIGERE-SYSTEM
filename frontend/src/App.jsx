// frontend/src/App.jsx

import { useState, useEffect } from 'react';
import axios from 'axios';

// URL da API base, ajustada para o backend
const API_URL = '/api/';

// Função debounce para evitar chamadas de API excessivas
const debounce = (func, delay) => {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => {
      func.apply(null, args);
    }, delay);
  };
};

function App() {
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');
  const [requisicaoCadastrada, setRequisicaoCadastrada] = useState(false);
  
  // Estados para os dados do formulário
  const [requisicaoFormData, setRequisicaoFormData] = useState({
    tipo_documento: '',
    numero_caso: '',
    data_requisicao: '',
    data_recebimento: '',
    objetivo_pericia: '',
    status_requisicao: 'ESPERA',
    peso_requisicao: 'P1',
    pae_requisicao: '',
    solicitante: '',
    tipo_exame: ''
  });

  const [materialFormData, setMaterialFormData] = useState({
    tipo_equipamento: '',
    outros_equipamentos: '',
    quantidade: '',
    local_armazenamento: '',
    prateleira: ''
  });

  // Novos estados para armazenar as sugestões do autocomplete
  const [solicitanteSuggestions, setSolicitanteSuggestions] = useState([]);
  const [tipoExameSuggestions, setTipoExameSuggestions] = useState([]);

  // Estados para controlar a visibilidade dos campos "Outros"
  const [showOutrosEquipamentos, setShowOutrosEquipamentos] = useState(false);
  const [showOutrosExames, setShowOutrosExames] = useState(false);

  // Simula o carregamento inicial
  useEffect(() => {
    setTimeout(() => {
      setLoading(false);
    }, 1000);
  }, []);
  
  // Função para buscar as sugestões de solicitantes
  const fetchSolicitanteSuggestions = async (query) => {
    if (query.length < 2) { // Evita buscas muito curtas
      setSolicitanteSuggestions([]);
      return;
    }
    try {
      const response = await axios.get(`${API_URL}solicitantes/autocomplete?query=${query}`);
      setSolicitanteSuggestions(response.data);
    } catch (error) {
      console.error('Erro ao buscar sugestões de solicitantes:', error);
    }
  };

  // Função para buscar as sugestões de tipos de exame
  const fetchTipoExameSuggestions = async (query) => {
    if (query.length < 2) {
      setTipoExameSuggestions([]);
      return;
    }
    try {
      const response = await axios.get(`${API_URL}tipos-exame/autocomplete?query=${query}`);
      setTipoExameSuggestions(response.data);
    } catch (error) {
      console.error('Erro ao buscar sugestões de tipos de exame:', error);
    }
  };

  // Funções com debounce para chamar as APIs
  const debouncedFetchSolicitantes = debounce(fetchSolicitanteSuggestions, 300);
  const debouncedFetchTipoExame = debounce(fetchTipoExameSuggestions, 300);

  const handleRequisicaoChange = (e) => {
    const { name, value } = e.target;
    setRequisicaoFormData({ ...requisicaoFormData, [name]: value });
    
    // Atualiza a visibilidade do campo "Outros" para exames
    if (name === 'tipo_exame' && value === 'OUTROS') {
      setShowOutrosExames(true);
    } else {
      setShowOutrosExames(false);
    }

    // Chama a função de busca com debounce
    if (name === 'solicitante') {
      debouncedFetchSolicitantes(value);
    } else if (name === 'tipo_exame') {
      debouncedFetchTipoExame(value);
    }
  };

  const handleMaterialChange = (e) => {
    const { name, value } = e.target;
    setMaterialFormData({ ...materialFormData, [name]: value });
    
    if (name === 'tipo_equipamento') {
      setShowOutrosEquipamentos(value === 'OUTROS');
    }
  };

  const handleRequisicaoSubmit = (e) => {
    e.preventDefault();
    console.log('Dados da Requisição:', requisicaoFormData);
    setMessage('Requisição cadastrada com sucesso! Agora cadastre o material.');
    setRequisicaoCadastrada(true);
  };

  const handleMaterialSubmit = (e) => {
    e.preventDefault();
    console.log('Dados do Material:', materialFormData);
    setMessage('Material cadastrado com sucesso!');
    setRequisicaoCadastrada(false);
    setRequisicaoFormData({ 
      tipo_documento: '',
      numero_caso: '',
      data_requisicao: '',
      data_recebimento: '',
      objetivo_pericia: '',
      status_requisicao: 'ESPERA',
      peso_requisicao: 'P1',
      pae_requisicao: '',
      solicitante: '',
      tipo_exame: ''
    });
    setMaterialFormData({ 
      tipo_equipamento: '',
      outros_equipamentos: '',
      quantidade: '',
      local_armazenamento: '',
      prateleira: ''
    });
  };

  if (loading) {
    return (
      <div className="spinner-container">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      <header className="top-bar">
        <span className="top-bar-title">Sistema de Cadastro</span>
      </header>
      
      <aside className="sidebar">
        <div className="sidebar-links">
          <a href="#" className="sidebar-link">Início</a>
          <a href="#" className="sidebar-link">BUSCAR REQUISIÇÃO</a>
          <a href="#" className="sidebar-link">GERÊNCIA</a>
        </div>
      </aside>

      <main className="main-content">
        <div className="form-card">
          <h2 className="form-title">Cadastro de Requisição</h2>
          
          {message && (
            <div className={`message-box ${message.includes('sucesso') ? 'message-success' : 'message-error'}`}>
              {message}
            </div>
          )}

          {!requisicaoCadastrada && (
            <form onSubmit={handleRequisicaoSubmit}>
              <div className="form-grid">
                <div className="form-group">
                  <label className="form-label">Tipo de Documento:</label>
                  <select name="tipo_documento" value={requisicaoFormData.tipo_documento} onChange={handleRequisicaoChange} required className="form-select">
                    <option value="">Selecione...</option>
                    <option value="AUTO">AUTO</option>
                    <option value="BOP">BOP</option>
                    <option value="FLAG">FLAG</option>
                    <option value="IPL">IPL</option>
                    <option value="OF">OFÍCIO</option>
                    <option value="MEMO">MEMO</option>
                    <option value="PROC">PROC</option>
                    <option value="TOMBO">TOMBO</option>
                  </select>
                </div>
                <div className="form-group">
                  <label className="form-label">Nº do Documento:</label>
                  <input type="text" name="numero_caso" value={requisicaoFormData.numero_caso} onChange={handleRequisicaoChange} required className="form-input" />
                </div>
                <div className="form-group">
                  <label className="form-label">Data da Requisição:</label>
                  <input type="date" name="data_requisicao" value={requisicaoFormData.data_requisicao} onChange={handleRequisicaoChange} required className="form-input" />
                </div>
                <div className="form-group">
                  <label className="form-label">Data de Recebimento:</label>
                  <input type="date" name="data_recebimento" value={requisicaoFormData.data_recebimento} onChange={handleRequisicaoChange} required className="form-input" />
                </div>
                <div className="form-group">
                  <label className="form-label">Unidade Solicitante:</label>
                  <input type="text" name="solicitante" value={requisicaoFormData.solicitante} onChange={handleRequisicaoChange} list="solicitante-suggestions" required className="form-input" />
                  <datalist id="solicitante-suggestions">
                    {solicitanteSuggestions.map((suggestion, index) => (
                      <option key={index} value={suggestion} />
                    ))}
                  </datalist>
                </div>
                <div className="form-group">
                  <label className="form-label">Tipo de Exame:</label>
                  <input type="text" name="tipo_exame" value={requisicaoFormData.tipo_exame} onChange={handleRequisicaoChange} list="tipo-exame-suggestions" required className="form-input" />
                  <datalist id="tipo-exame-suggestions">
                    {tipoExameSuggestions.map((suggestion, index) => (
                      <option key={index} value={suggestion} />
                    ))}
                  </datalist>
                </div>
                <div className="form-group" style={{ gridColumn: 'span 2' }}>
                  <label className="form-label">Objetivo da Perícia:</label>
                  <textarea name="objetivo_pericia" value={requisicaoFormData.objetivo_pericia} onChange={handleRequisicaoChange} required rows="3" className="form-textarea" />
                </div>
                <div className="form-group">
                  <label className="form-label">Nível de Prioridade:</label>
                  <select name="peso_requisicao" value={requisicaoFormData.peso_requisicao} onChange={handleRequisicaoChange} required className="form-select">
                    <option value="">Selecione...</option>
                    <option value="P1">P1</option>
                    <option value="P2">P2</option>
                    <option value="P3">P3</option>
                    <option value="P4">P4</option>
                  </select>
                </div>
                <div className="form-group">
                  <label className="form-label">Status:</label>
                  <select name="status_requisicao" value={requisicaoFormData.status_requisicao} onChange={handleRequisicaoChange} required className="form-select">
                    <option value="">Selecione...</option>
                    <option value="ESPERA">EM ESPERA</option>
                    <option value="PROCESSAMENTO">EM ANDAMENTO</option>
                    <option value="ENTREGUE">FINALIZADO</option>
                    <option value="CANCELADO">CANCELADO</option>
                  </select>
                </div>
              </div>
              <div className="submit-button-container">
                <button type="submit" className="submit-button">
                  Cadastrar
                </button>
              </div>
            </form>
          )}

          {requisicaoCadastrada && (
            <div className="form-card" style={{ marginTop: '2rem' }}>
              <h2 className="form-title">Cadastro de Material</h2>
              <form onSubmit={handleMaterialSubmit}>
                <div className="form-grid">
                  <div className="form-group">
                    <label className="form-label">Tipo de Equipamento:</label>
                    <select name="tipo_equipamento" value={materialFormData.tipo_equipamento} onChange={handleMaterialChange} required className="form-select">
                      <option value="">Selecione...</option>
                      <option value="SMARTPHONE">SMARTPHONE</option>
                      <option value="TABLET">TABLET</option>
                      <option value="NOTEBOOK">NOTEBOOK</option>
                      <option value="CPU">CPU</option>
                      <option value="HD">HD</option>
                      <option value="SSD">SSD</option>
                      <option value="PENDRIVE">PENDRIVE</option>
                      <option value="OUTROS">OUTROS</option>
                    </select>
                  </div>
                  {showOutrosEquipamentos && (
                    <div className="form-group">
                      <label className="form-label">Outros:</label>
                      <input type="text" name="outros_equipamentos" value={materialFormData.outros_equipamentos} onChange={handleMaterialChange} required className="form-input" />
                    </div>
                  )}
                  <div className="form-group">
                    <label className="form-label">Quantidade (UNID):</label>
                    <input type="number" name="quantidade" value={materialFormData.quantidade} onChange={handleMaterialChange} required className="form-input" />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Local de Armazenamento:</label>
                    <select name="local_armazenamento" value={materialFormData.local_armazenamento} onChange={handleMaterialChange} required className="form-select">
                      <option value="">Selecione...</option>
                      <option value="DEPOSITO 01">DEPOSITO 01</option>
                      <option value="DEPOSITO 02">DEPOSITO 02</option>
                      <option value="DEPOSITO 03">DEPOSITO 03</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label className="form-label">Prateleira:</label>
                    <input type="text" name="prateleira" value={materialFormData.prateleira} onChange={handleMaterialChange} required className="form-input" />
                  </div>
                </div>
                <div className="submit-button-container">
                  <button type="submit" className="submit-button">
                    Cadastrar Material
                  </button>
                </div>
              </form>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
