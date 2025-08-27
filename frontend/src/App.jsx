// frontend/src/App.jsx

// Importações essenciais do React e de bibliotecas externas
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
      <div className="flex justify-center items-center h-screen bg-gray-100">
        <div className="w-12 h-12 rounded-full border-4 border-t-4 border-blue-500 animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 font-sans">
      <header className="top-bar bg-[#247dd6] text-white p-4 text-center">
        <span className="font-semibold text-lg">Sistema de Cadastro</span>
      </header>
      
      <aside className="hidden md:block w-56 bg-white p-4 shadow-lg h-full fixed top-0 left-0">
        <div className="flex flex-col space-y-4 pt-16">
          <a href="#" className="text-gray-700 font-medium hover:bg-gray-200 p-2 rounded-md">Início</a>
          <a href="#" className="text-gray-700 font-medium hover:bg-gray-200 p-2 rounded-md">BUSCAR REQUISIÇÃO</a>
          <a href="#" className="text-gray-700 font-medium hover:bg-gray-200 p-2 rounded-md">GERÊNCIA</a>
        </div>
      </aside>

      <main className="md:ml-56 p-8">
        <div className="formCadastro bg-white p-8 rounded-lg shadow-lg max-w-4xl mx-auto">
          <h2 className="text-2xl font-bold mb-6 text-center">Cadastro de Requisição</h2>
          
          {message && (
            <div className={`p-4 mb-6 rounded-lg text-white font-semibold text-center ${message.includes('sucesso') ? 'bg-green-600' : 'bg-red-600'}`}>
              {message}
            </div>
          )}

          {!requisicaoCadastrada && (
            <form onSubmit={handleRequisicaoSubmit}>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="flex flex-col">
                  <label className="text-sm font-medium text-gray-700">Tipo de Documento:</label>
                  <select name="tipo_documento" value={requisicaoFormData.tipo_documento} onChange={handleRequisicaoChange} required className="p-2 border border-gray-300 rounded-md">
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
                <div className="flex flex-col">
                  <label className="text-sm font-medium text-gray-700">Nº do Documento:</label>
                  <input type="text" name="numero_caso" value={requisicaoFormData.numero_caso} onChange={handleRequisicaoChange} required className="p-2 border border-gray-300 rounded-md" />
                </div>
                <div className="flex flex-col">
                  <label className="text-sm font-medium text-gray-700">Data da Requisição:</label>
                  <input type="date" name="data_requisicao" value={requisicaoFormData.data_requisicao} onChange={handleRequisicaoChange} required className="p-2 border border-gray-300 rounded-md" />
                </div>
                <div className="flex flex-col">
                  <label className="text-sm font-medium text-gray-700">Data de Recebimento:</label>
                  <input type="date" name="data_recebimento" value={requisicaoFormData.data_recebimento} onChange={handleRequisicaoChange} required className="p-2 border border-gray-300 rounded-md" />
                </div>
                <div className="flex flex-col">
                  <label className="text-sm font-medium text-gray-700">Unidade Solicitante:</label>
                  <input type="text" name="solicitante" value={requisicaoFormData.solicitante} onChange={handleRequisicaoChange} list="solicitante-suggestions" required className="p-2 border border-gray-300 rounded-md" />
                  <datalist id="solicitante-suggestions">
                    {solicitanteSuggestions.map((suggestion, index) => (
                      <option key={index} value={suggestion} />
                    ))}
                  </datalist>
                </div>
                <div className="flex flex-col">
                  <label className="text-sm font-medium text-gray-700">Tipo de Exame:</label>
                  <input type="text" name="tipo_exame" value={requisicaoFormData.tipo_exame} onChange={handleRequisicaoChange} list="tipo-exame-suggestions" required className="p-2 border border-gray-300 rounded-md" />
                  <datalist id="tipo-exame-suggestions">
                    {tipoExameSuggestions.map((suggestion, index) => (
                      <option key={index} value={suggestion} />
                    ))}
                  </datalist>
                </div>
                <div className="flex flex-col col-span-1 md:col-span-2">
                  <label className="text-sm font-medium text-gray-700">Objetivo da Perícia:</label>
                  <textarea name="objetivo_pericia" value={requisicaoFormData.objetivo_pericia} onChange={handleRequisicaoChange} required rows="3" className="p-2 border border-gray-300 rounded-md" />
                </div>
                <div className="flex flex-col">
                  <label className="text-sm font-medium text-gray-700">Nível de Prioridade:</label>
                  <select name="peso_requisicao" value={requisicaoFormData.peso_requisicao} onChange={handleRequisicaoChange} required className="p-2 border border-gray-300 rounded-md">
                    <option value="">Selecione...</option>
                    <option value="P1">P1</option>
                    <option value="P2">P2</option>
                    <option value="P3">P3</option>
                    <option value="P4">P4</option>
                  </select>
                </div>
                <div className="flex flex-col">
                  <label className="text-sm font-medium text-gray-700">Status:</label>
                  <select name="status_requisicao" value={requisicaoFormData.status_requisicao} onChange={handleRequisicaoChange} required className="p-2 border border-gray-300 rounded-md">
                    <option value="">Selecione...</option>
                    <option value="ESPERA">EM ESPERA</option>
                    <option value="PROCESSAMENTO">EM ANDAMENTO</option>
                    <option value="ENTREGUE">FINALIZADO</option>
                    <option value="CANCELADO">CANCELADO</option>
                  </select>
                </div>
              </div>
              <div className="flex justify-center mt-6">
                <button type="submit" className="w-full md:w-auto bg-blue-600 text-white font-bold py-3 px-8 rounded-lg shadow-md hover:bg-blue-700 transition-colors">
                  Cadastrar
                </button>
              </div>
            </form>
          )}

          {requisicaoCadastrada && (
            <div className="formCadastro bg-white p-8 rounded-lg shadow-lg mt-8">
              <h2 className="text-2xl font-bold mb-6 text-center">Cadastro de Material</h2>
              <form onSubmit={handleMaterialSubmit}>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="flex flex-col">
                    <label className="text-sm font-medium text-gray-700">Tipo de Equipamento:</label>
                    <select name="tipo_equipamento" value={materialFormData.tipo_equipamento} onChange={handleMaterialChange} required className="p-2 border border-gray-300 rounded-md">
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
                    <div className="flex flex-col">
                      <label className="text-sm font-medium text-gray-700">Outros:</label>
                      <input type="text" name="outros_equipamentos" value={materialFormData.outros_equipamentos} onChange={handleMaterialChange} required className="p-2 border border-gray-300 rounded-md" />
                    </div>
                  )}
                  <div className="flex flex-col">
                    <label className="text-sm font-medium text-gray-700">Quantidade (UNID):</label>
                    <input type="number" name="quantidade" value={materialFormData.quantidade} onChange={handleMaterialChange} required className="p-2 border border-gray-300 rounded-md" />
                  </div>
                  <div className="flex flex-col">
                    <label className="text-sm font-medium text-gray-700">Local de Armazenamento:</label>
                    <select name="local_armazenamento" value={materialFormData.local_armazenamento} onChange={handleMaterialChange} required className="p-2 border border-gray-300 rounded-md">
                      <option value="">Selecione...</option>
                      <option value="DEPOSITO 01">DEPOSITO 01</option>
                      <option value="DEPOSITO 02">DEPOSITO 02</option>
                      <option value="DEPOSITO 03">DEPOSITO 03</option>
                    </select>
                  </div>
                  <div className="flex flex-col">
                    <label className="text-sm font-medium text-gray-700">Prateleira:</label>
                    <input type="text" name="prateleira" value={materialFormData.prateleira} onChange={handleMaterialChange} required className="p-2 border border-gray-300 rounded-md" />
                  </div>
                </div>
                <div className="flex justify-center mt-6">
                  <button type="submit" className="w-full md:w-auto bg-blue-600 text-white font-bold py-3 px-8 rounded-lg shadow-md hover:bg-blue-700 transition-colors">
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