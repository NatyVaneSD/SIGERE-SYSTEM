import { useState, useEffect } from 'react';
import axios from 'axios';

// URL base da API do backend Django.
const API_URL = '/api/';

// Constantes para as escolhas dos campos.
const TIPO_DOCUMENTO_CHOICES = [
  { value: 'FLAG', label: 'FLAG' },
  { value: 'IPL', label: 'IPL' },
  { value: 'BOP', label: 'BOP' },
  { value: 'OF', label: 'OF' },
  { value: 'TCO', label: 'TCO' },
  { value: 'MEMO', label: 'MEMO' },
];

const PESO_CHOICES = [
  { value: 'P1', label: 'PESO 01' },
  { value: 'P2', label: 'PESO 02' },
  { value: 'P3', label: 'PESO 03' },
  { value: 'P4', label: 'PESO 04' },
];

const STATUS_CHOICES = [
  { value: 'ESPERA', label: 'Em Espera' },
  { value: 'PROCESSAMENTO', label: 'Em Processamento' },
  { value: 'ENTREGUE', label: 'Entregue' },
  { value: 'TRANSFERIDO', label: 'Transferido' },
  { value: 'DEVOLVIDO', label: 'Devolvido' },
  { value: 'CANCELADO', label: 'Cancelado' },
];

const EQUIPAMENTO_CHOICES = [
  { value: 'SMARTPHONE', label: 'SMARTPHONE' },
  { value: 'NOTEBOOK', label: 'NOTEBOOK' },
  { value: 'PENDRIVE', label: 'PENDRIVE' },
  { value: 'HD', label: 'HD' },
  { value: 'SSD', label: 'SSD' },
  { value: 'CPU', label: 'CPU' },
  { value: 'CARTAO MICROSD', label: 'CARTÃO MICROSD' },
  { value: 'OUTROS', label: 'Outros' },
];

const DEPOSITO_CHOICES = [
  { value: 'D1', label: 'Depósito 01' },
  { value: 'D2', label: 'Depósito 02' },
  { value: 'D3', label: 'Depósito 03' },
];

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
  const [requisicaoCadastrada, setRequisicaoCadastrada] = useState(false);
  const [message, setMessage] = useState('');
  const [requisicaoId, setRequisicaoId] = useState(null);

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
    unidade_solicitante: '',
    tipo_exame: '',
    numero_protocolo: '',
  });

  const [materialFormData, setMaterialFormData] = useState({
    tipo_equipamento: '',
    outros_tipo: '',
    quant_equipamento: '',
    deposito: '',
    prateleira: '',
  });

  const [solicitanteSuggestions, setSolicitanteSuggestions] = useState([]);
  const [unidadeSolicitanteSuggestions, setUnidadeSolicitanteSuggestions] = useState([]);
  const [tipoExameSuggestions, setTipoExameSuggestions] = useState([]);
  const [showOutrosEquipamentos, setShowOutrosEquipamentos] = useState(false);

  const fetchSolicitanteSuggestions = async (query) => {
    if (query.length < 2) {
      setSolicitanteSuggestions([]);
      return;
    }
    try {
      // Simulação de chamada de API. Substitua por sua lógica real.
      // const response = await axios.get(`${API_URL}solicitantes/autocomplete/?query=${query}`);
      // setSolicitanteSuggestions(response.data);
      console.log(`Buscando sugestões para solicitante: ${query}`);
      setSolicitanteSuggestions(['Sugestão A', 'Sugestão B']);
    } catch (error) {
      console.error('Erro ao buscar sugestões de solicitantes:', error);
    }
  };

  const fetchUnidadeSolicitanteSuggestions = async (query) => {
    if (query.length < 2) {
      setUnidadeSolicitanteSuggestions([]);
      return;
    }
    try {
      // Simulação de chamada de API. Substitua por sua lógica real.
      // const response = await axios.get(`${API_URL}unidades-solicitantes/autocomplete/?query=${query}`);
      // setUnidadeSolicitanteSuggestions(response.data);
      console.log(`Buscando sugestões para unidade solicitante: ${query}`);
      setUnidadeSolicitanteSuggestions(['Unidade X', 'Unidade Y']);
    } catch (error) {
      console.error('Erro ao buscar sugestões de unidades solicitantes:', error);
    }
  };

  const fetchTipoExameSuggestions = async (query) => {
    if (query.length < 2) {
      setTipoExameSuggestions([]);
      return;
    }
    try {
      // Simulação de chamada de API. Substitua por sua lógica real.
      // const response = await axios.get(`${API_URL}tipos-exame/autocomplete/?query=${query}`);
      // setTipoExameSuggestions(response.data);
      console.log(`Buscando sugestões para tipo de exame: ${query}`);
      setTipoExameSuggestions(['Análise de Dados', 'Análise Forense']);
    } catch (error) {
      console.error('Erro ao buscar sugestões de tipos de exame:', error);
    }
  };

  const debouncedFetchSolicitantes = debounce(fetchSolicitanteSuggestions, 300);
  const debouncedFetchUnidadeSolicitante = debounce(fetchUnidadeSolicitanteSuggestions, 300);
  const debouncedFetchTipoExame = debounce(fetchTipoExameSuggestions, 300);

  const handleRequisicaoChange = (e) => {
    const { name, value } = e.target;
    setRequisicaoFormData({ ...requisicaoFormData, [name]: value });

    if (name === 'solicitante') {
      debouncedFetchSolicitantes(value);
    } else if (name === 'unidade_solicitante') {
      debouncedFetchUnidadeSolicitante(value);
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

  const handleRequisicaoSubmit = async (e) => {
    e.preventDefault();
    try {
      // await axios.post(`${API_URL}requisicoes/`, requisicaoFormData);
      
      // Simulação de resposta de sucesso
      setRequisicaoId(123);
      
      setMessage('Requisição cadastrada com sucesso! Agora cadastre o material.');
      setRequisicaoCadastrada(true);
    } catch (error) {
      console.error('Erro ao cadastrar requisição:', error);
      setMessage('Erro ao cadastrar requisição. Tente novamente.');
    }
  };

  const handleMaterialSubmit = async (e) => {
    e.preventDefault();
    try {
      const materialData = {
        ...materialFormData,
        requisicao: requisicaoId,
      };

      // await axios.post(`${API_URL}equipamentos/`, materialData);

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
        unidade_solicitante: '',
        tipo_exame: '',
        numero_protocolo: '',
      });
      setMaterialFormData({ 
        tipo_equipamento: '',
        outros_tipo: '',
        quant_equipamento: '',
        deposito: '',
        prateleira: '',
      });
      setRequisicaoId(null);
    } catch (error) {
      console.error('Erro ao cadastrar material:', error);
      setMessage('Erro ao cadastrar material. Tente novamente.');
    }
  };

  return (
    <div className="min-h-screen">
      {/* Estilos CSS tradicionais */}
      <style>{`
        body, h1, h2, h3, h4, h5, h6, p, ul, ol, li, input, select, button, textarea {
          margin: 0;
          padding: 0;
          box-sizing: border-box;
        }

        body {
          font-family: 'Inter', sans-serif;
          background-color: #0b111b; /* Cor de fundo escura */
          color: #e2e8f0;
        }

        .min-h-screen {
          min-height: 100vh;
          display: flex;
          flex-direction: column;
        }

        .top-bar {
          background-color: #1a202c; /* Cor escura para a barra superior */
          color: #ffffff;
          padding: 1rem;
          text-align: center;
          position: fixed;
          top: 0;
          left: 0;
          width: 100%;
          z-index: 1000;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .top-bar-title {
          font-weight: 600;
          font-size: 1.25rem;
        }

        .sidebar {
          display: none;
          width: 14rem;
          background-color: #1a202c;
          padding: 1rem;
          box-shadow: 2px 0 4px rgba(0, 0, 0, 0.1);
          height: 100%;
          position: fixed;
          top: 0;
          left: 0;
          z-index: 999;
          transition: transform 0.3s ease-in-out;
          transform: translateX(-100%);
        }

        .sidebar.active {
          transform: translateX(0);
        }

        .sidebar-links {
          display: flex;
          flex-direction: column;
          gap: 1rem;
          padding-top: 4rem;
        }

        .sidebar-link {
          color: #a0aec0;
          font-weight: 500;
          padding: 0.5rem 1rem;
          border-radius: 0.375rem;
          text-decoration: none;
          transition: background-color 0.2s ease-in-out;
        }

        .sidebar-link:hover {
          background-color: #2d3748;
          color: #ffffff;
        }

        .main-content {
          flex: 1;
          padding: 2rem;
          padding-top: 6rem; /* Espaço para o header fixo */
        }
        
        .main-content-shifted {
          margin-left: 14rem;
        }

        @media (min-width: 768px) {
          .sidebar {
            display: block;
            transform: translateX(0);
          }
          .main-content {
            margin-left: 14rem;
          }
        }

        .form-card {
          background-color: #1a202c; /* Cor de fundo escura */
          padding: 2rem;
          border-radius: 0.5rem;
          box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
          max-width: 56rem;
          margin-left: auto;
          margin-right: auto;
        }

        .form-title {
          font-size: 1.5rem;
          font-weight: 700;
          margin-bottom: 1.5rem;
          text-align: center;
          color: #ffffff;
        }

        .form-grid {
          display: grid;
          grid-template-columns: 1fr;
          gap: 1.5rem; /* Aumentado o gap para melhor espaçamento */
        }

        @media (min-width: 768px) {
          .form-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr));
          }
        }

        .form-group {
          display: flex;
          flex-direction: column;
        }

        .form-label {
          font-size: 0.875rem;
          font-weight: 500;
          color: #a0aec0; /* Cor do texto da label */
          margin-bottom: 0.25rem;
        }

        .form-input, .form-select, .form-textarea {
          padding: 0.75rem; /* Aumentado o padding */
          border: 1px solid #4a5568; /* Borda mais escura */
          background-color: #2d3748; /* Fundo do campo mais escuro */
          color: #ffffff;
          border-radius: 0.375rem;
          width: 100%;
          transition: border-color 0.2s;
        }
        
        .form-input:focus, .form-select:focus, .form-textarea:focus {
          border-color: #4299e1; /* Borda azul no foco */
          outline: none;
        }

        .form-textarea {
          resize: vertical;
        }

        .submit-button-container {
          display: flex;
          justify-content: center;
          margin-top: 1.5rem;
        }

        .submit-button {
          background-color: #4299e1;
          color: #ffffff;
          font-weight: 700;
          padding: 0.75rem 2rem;
          border-radius: 0.5rem;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
          transition: background-color 0.2s ease-in-out;
          width: 100%;
          border: none;
        }

        @media (min-width: 768px) {
          .submit-button {
            width: auto;
          }
        }

        .submit-button:hover {
          background-color: #3182ce;
        }

        .message-box {
          padding: 1rem;
          margin-bottom: 1.5rem;
          border-radius: 0.5rem;
          font-weight: 600;
          text-align: center;
        }

        .message-success {
          background-color: #14532d;
          color: #a7f3d0;
        }

        .message-error {
          background-color: #991b1b;
          color: #fca5a5;
        }
        
        .hamburger-menu {
          display: block;
          position: fixed;
          top: 1rem;
          left: 1rem;
          z-index: 1001;
          background: #1a202c;
          border: 1px solid #4a5568;
          border-radius: 0.25rem;
          padding: 0.5rem;
          cursor: pointer;
        }
        
        @media (min-width: 768px) {
          .hamburger-menu {
            display: none;
          }
        }
      `}</style>

      {/* Estrutura do layout */}
      <div className="top-bar">
        <h1 className="top-bar-title">Sistema de Gestão de Requisições</h1>
      </div>

      <div className="sidebar">
        <div className="sidebar-links">
          <a href="#" className="sidebar-link">Início</a>
          <a href="#" className="sidebar-link">Buscar Requisição</a>
          <a href="#" className="sidebar-link">Gerência</a>
        </div>
      </div>
      
      <main className="main-content">
        <div className="form-card">
          <h2 className="form-title">
            {requisicaoCadastrada ? 'Cadastro de Material' : 'Cadastro de Requisição e Protocolo'}
          </h2>
          {message && (
            <div className={`message-box ${message.includes('sucesso') ? 'message-success' : 'message-error'}`}>
              {message}
            </div>
          )}
          {!requisicaoCadastrada && (
            <form onSubmit={handleRequisicaoSubmit} className="space-y-6">
              <div className="form-grid">
                <div className="form-group">
                  <label htmlFor="tipo_documento" className="form-label">Tipo de Documento:</label>
                  <select
                    id="tipo_documento"
                    name="tipo_documento"
                    value={requisicaoFormData.tipo_documento}
                    onChange={handleRequisicaoChange}
                    required
                    className="form-select"
                  >
                    <option value="">Selecione...</option>
                    {TIPO_DOCUMENTO_CHOICES.map(option => (
                      <option key={option.value} value={option.value}>{option.label}</option>
                    ))}
                  </select>
                </div>
                <div className="form-group">
                  <label htmlFor="numero_caso" className="form-label">Nº do Caso:</label>
                  <input
                    type="text"
                    id="numero_caso"
                    name="numero_caso"
                    value={requisicaoFormData.numero_caso}
                    onChange={handleRequisicaoChange}
                    required
                    className="form-input"
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="numero_protocolo" className="form-label">Nº do Protocolo:</label>
                  <input
                    type="text"
                    id="numero_protocolo"
                    name="numero_protocolo"
                    value={requisicaoFormData.numero_protocolo}
                    onChange={handleRequisicaoChange}
                    required
                    className="form-input"
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="data_requisicao" className="form-label">Data da Requisição:</label>
                  <input
                    type="date"
                    id="data_requisicao"
                    name="data_requisicao"
                    value={requisicaoFormData.data_requisicao}
                    onChange={handleRequisicaoChange}
                    required
                    className="form-input"
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="data_recebimento" className="form-label">Data de Recebimento:</label>
                  <input
                    type="date"
                    id="data_recebimento"
                    name="data_recebimento"
                    value={requisicaoFormData.data_recebimento}
                    onChange={handleRequisicaoChange}
                    required
                    className="form-input"
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="unidade_solicitante" className="form-label">Unidade Solicitante:</label>
                  <input
                    type="text"
                    id="unidade_solicitante"
                    name="unidade_solicitante"
                    value={requisicaoFormData.unidade_solicitante}
                    onChange={handleRequisicaoChange}
                    list="unidade-solicitante-suggestions"
                    required
                    className="form-input"
                  />
                  <datalist id="unidade-solicitante-suggestions">
                    {unidadeSolicitanteSuggestions.map((suggestion, index) => (
                      <option key={index} value={suggestion} />
                    ))}
                  </datalist>
                </div>
                <div className="form-group">
                  <label htmlFor="solicitante" className="form-label">Solicitante:</label>
                  <input
                    type="text"
                    id="solicitante"
                    name="solicitante"
                    value={requisicaoFormData.solicitante}
                    onChange={handleRequisicaoChange}
                    list="solicitante-suggestions"
                    required
                    className="form-input"
                  />
                  <datalist id="solicitante-suggestions">
                    {solicitanteSuggestions.map((suggestion, index) => (
                      <option key={index} value={suggestion} />
                    ))}
                  </datalist>
                </div>
                <div className="form-group">
                  <label htmlFor="tipo_exame" className="form-label">Tipo de Exame:</label>
                  <input
                    type="text"
                    id="tipo_exame"
                    name="tipo_exame"
                    value={requisicaoFormData.tipo_exame}
                    onChange={handleRequisicaoChange}
                    list="tipo-exame-suggestions"
                    required
                    className="form-input"
                  />
                  <datalist id="tipo-exame-suggestions">
                    {tipoExameSuggestions.map((suggestion, index) => (
                      <option key={index} value={suggestion} />
                    ))}
                  </datalist>
                </div>
                <div className="form-group">
                  <label htmlFor="peso_requisicao" className="form-label">Nível de Prioridade:</label>
                  <select
                    id="peso_requisicao"
                    name="peso_requisicao"
                    value={requisicaoFormData.peso_requisicao}
                    onChange={handleRequisicaoChange}
                    required
                    className="form-select"
                  >
                    <option value="">Selecione...</option>
                    {PESO_CHOICES.map(option => (
                      <option key={option.value} value={option.value}>{option.label}</option>
                    ))}
                  </select>
                </div>
                {requisicaoFormData.peso_requisicao !== 'P1' && (
                  <div className="form-group">
                    <label htmlFor="pae_requisicao" className="form-label">Nº PAE:</label>
                    <input
                      type="text"
                      id="pae_requisicao"
                      name="pae_requisicao"
                      value={requisicaoFormData.pae_requisicao}
                      onChange={handleRequisicaoChange}
                      required={requisicaoFormData.peso_requisicao !== 'P1'}
                      className="form-input"
                    />
                  </div>
                )}
              </div>
              <div className="form-group">
                <label htmlFor="objetivo_pericia" className="form-label">Objetivo da Perícia:</label>
                <textarea
                  id="objetivo_pericia"
                  name="objetivo_pericia"
                  value={requisicaoFormData.objetivo_pericia}
                  onChange={handleRequisicaoChange}
                  required
                  rows="3"
                  className="form-textarea"
                />
              </div>
              <div className="form-group">
                <label htmlFor="status_requisicao" className="form-label">Status:</label>
                <select
                  id="status_requisicao"
                  name="status_requisicao"
                  value={requisicaoFormData.status_requisicao}
                  onChange={handleRequisicaoChange}
                  required
                  className="form-select"
                >
                  <option value="">Selecione...</option>
                  {STATUS_CHOICES.map(option => (
                    <option key={option.value} value={option.value}>{option.label}</option>
                  ))}
                </select>
              </div>
              <div className="submit-button-container">
                <button
                  type="submit"
                  className="submit-button"
                >
                  Cadastrar
                </button>
              </div>
            </form>
          )}

          {requisicaoCadastrada && (
            <form onSubmit={handleMaterialSubmit} className="space-y-6">
              <div className="form-grid">
                <div className="form-group">
                  <label htmlFor="tipo_equipamento" className="form-label">Tipo de Equipamento:</label>
                  <select
                    id="tipo_equipamento"
                    name="tipo_equipamento"
                    value={materialFormData.tipo_equipamento}
                    onChange={handleMaterialChange}
                    required
                    className="form-select"
                  >
                    <option value="">Selecione...</option>
                    {EQUIPAMENTO_CHOICES.map(option => (
                      <option key={option.value} value={option.value}>{option.label}</option>
                    ))}
                  </select>
                </div>
                {showOutrosEquipamentos && (
                  <div className="form-group">
                    <label htmlFor="outros_tipo" className="form-label">Outros:</label>
                    <input
                      type="text"
                      id="outros_tipo"
                      name="outros_tipo"
                      value={materialFormData.outros_tipo}
                      onChange={handleMaterialChange}
                      required
                      className="form-input"
                    />
                  </div>
                )}
                <div className="form-group">
                  <label htmlFor="quant_equipamento" className="form-label">Quantidade (UNID):</label>
                  <input
                    type="number"
                    id="quant_equipamento"
                    name="quant_equipamento"
                    value={materialFormData.quant_equipamento}
                    onChange={handleMaterialChange}
                    required
                    className="form-input"
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="deposito" className="form-label">Local de Armazenamento (Depósito):</label>
                  <select
                    id="deposito"
                    name="deposito"
                    value={materialFormData.deposito}
                    onChange={handleMaterialChange}
                    required
                    className="form-select"
                  >
                    <option value="">Selecione...</option>
                    {DEPOSITO_CHOICES.map(option => (
                      <option key={option.value} value={option.value}>{option.label}</option>
                    ))}
                  </select>
                </div>
                <div className="form-group">
                  <label htmlFor="prateleira" className="form-label">Prateleira:</label>
                  <input
                    type="text"
                    id="prateleira"
                    name="prateleira"
                    value={materialFormData.prateleira}
                    onChange={handleMaterialChange}
                    required
                    className="form-input"
                  />
                </div>
              </div>
              <div className="submit-button-container">
                <button
                  type="submit"
                  className="submit-button"
                >
                  Cadastrar Material
                </button>
              </div>
            </form>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;