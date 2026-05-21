import { useState, useEffect } from "react"
import axios from "axios"

// Use a URL do Render em produção, localhost em desenvolvimento
const API = import.meta.env.VITE_API_URL || "http://localhost:8000"

export default function App() {
  const [email, setEmail] = useState("")
  const [senha, setSenha] = useState("")
  const [nome, setNome] = useState("")
  const [token, setToken] = useState(null)
  const [erro, setErro] = useState("")
  const [pedidos, setPedidos] = useState([])
  const [carregando, setCarregando] = useState(false)
  const [mostrarCriarConta, setMostrarCriarConta] = useState(false)

  // Criar conta
  async function criarConta() {
    setCarregando(true)
    setErro("")
    try {
      await axios.post(`${API}/auth/criar_conta`, {
        nome: nome,
        email: email,
        senha: senha,
        ativo: true,
        admin: false
      })
      alert("Conta criada com sucesso! Faça login.")
      setMostrarCriarConta(false)
      setNome("")
      setEmail("")
      setSenha("")
    } catch (e) {
      setErro(e.response?.data?.detail || "Erro ao criar conta")
    } finally {
      setCarregando(false)
    }
  }

  // Login
  async function login() {
    setCarregando(true)
    setErro("")
    try {
      const resp = await axios.post(`${API}/auth/login`, { email, senha })
      setToken(resp.data.access_token)
      setErro("")
      setEmail("")
      setSenha("")
    } catch (e) {
      setErro(e.response?.data?.detail || "Credenciais inválidas")
    } finally {
      setCarregando(false)
    }
  }

  // Listar pedidos
  async function listarPedidos() {
    setCarregando(true)
    try {
      const resp = await axios.get(`${API}/pedidos/listar/pedidos-usuario`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setPedidos(resp.data.pedidos)
      setErro("")
    } catch (e) {
      setErro("Erro ao buscar pedidos")
    } finally {
      setCarregando(false)
    }
  }

  // Criar pedido
  async function criarPedido() {
    setCarregando(true)
    try {
      const resp = await axios.post(`${API}/pedidos/pedido`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      })
      alert(resp.data.mensagem)
      await listarPedidos()
    } catch (e) {
      setErro("Erro ao criar pedido")
    } finally {
      setCarregando(false)
    }
  }

  // Cancelar pedido
  async function cancelarPedido(pedidoId) {
    if (!confirm("Cancelar este pedido?")) return
    setCarregando(true)
    try {
      const resp = await axios.post(`${API}/pedidos/pedido/cancelar/${pedidoId}`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      })
      alert(resp.data.mensagem)
      await listarPedidos()
    } catch (e) {
      setErro("Erro ao cancelar pedido")
    } finally {
      setCarregando(false)
    }
  }

  useEffect(() => {
    if (token) listarPedidos()
  }, [token])

  // Tela logado
  if (token) {
    return (
      <div style={{ padding: "20px" }}>
        <h1>🍕 Sistema de Pedidos</h1>
        <p>✅ Logado com sucesso!</p>
        
        <div style={{ margin: "20px 0", display: "flex", gap: "10px" }}>
          <button onClick={criarPedido} disabled={carregando}>
            🛒 Criar Novo Pedido
          </button>
          <button onClick={listarPedidos} disabled={carregando}>
            🔄 Atualizar
          </button>
        </div>

        {carregando && <p>⏳ Carregando...</p>}

        {pedidos.length === 0 && !carregando && (
          <p>Você ainda não tem nenhum pedido.</p>
        )}

        {pedidos.length > 0 && (
          <div>
            <h2>Meus Pedidos</h2>
            {pedidos.map(pedido => (
              <div key={pedido.id} style={{
                border: "1px solid #ccc",
                borderRadius: "8px",
                padding: "15px",
                margin: "10px 0",
                backgroundColor: pedido.status === "CANCELADO" ? "#ffe6e6" : "#f9f9f9"
              }}>
                <p><strong>Pedido #{pedido.id}</strong></p>
                <p>Status: <strong>{pedido.status}</strong></p>
                <p>Preço Total: R$ {pedido.preco?.toFixed(2) || "0.00"}</p>
                
                {pedido.status !== "CANCELADO" && (
                  <button onClick={() => cancelarPedido(pedido.id)} disabled={carregando}>
                    ❌ Cancelar
                  </button>
                )}
              </div>
            ))}
          </div>
        )}
        
        {erro && <p style={{color: "red"}}>{erro}</p>}
      </div>
    )
  }

  // Tela de login / criar conta
  return (
    <div style={{ padding: "20px", maxWidth: "400px", margin: "0 auto" }}>
      <h1>🍕 Pizza Delivery</h1>
      
      {!mostrarCriarConta ? (
        <>
          <h2>Login</h2>
          <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
            <input 
              placeholder="Email" 
              type="email"
              value={email}
              onChange={e => setEmail(e.target.value)} 
              style={{ padding: "10px" }}
            />
            <input 
              placeholder="Senha" 
              type="password" 
              value={senha}
              onChange={e => setSenha(e.target.value)}
              style={{ padding: "10px" }}
              onKeyPress={(e) => e.key === 'Enter' && login()}
            />
            <button onClick={login} disabled={carregando}>
              {carregando ? "Entrando..." : "Entrar"}
            </button>
            <button onClick={() => setMostrarCriarConta(true)}>
              Criar Conta
            </button>
            {erro && <p style={{color: "red"}}>{erro}</p>}
          </div>
        </>
      ) : (
        <>
          <h2>Criar Conta</h2>
          <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
            <input 
              placeholder="Nome" 
              value={nome}
              onChange={e => setNome(e.target.value)} 
              style={{ padding: "10px" }}
            />
            <input 
              placeholder="Email" 
              type="email"
              value={email}
              onChange={e => setEmail(e.target.value)} 
              style={{ padding: "10px" }}
            />
            <input 
              placeholder="Senha" 
              type="password" 
              value={senha}
              onChange={e => setSenha(e.target.value)}
              style={{ padding: "10px" }}
            />
            <button onClick={criarConta} disabled={carregando}>
              {carregando ? "Criando..." : "Criar Conta"}
            </button>
            <button onClick={() => setMostrarCriarConta(false)}>
              Voltar para Login
            </button>
            {erro && <p style={{color: "red"}}>{erro}</p>}
          </div>
        </>
      )}
    </div>
  )
}