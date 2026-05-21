import { useState } from "react"
import axios from "axios"

const API = "http://127.0.0.1:8000"

export default function App() {
  const [email, setEmail] = useState("")
  const [senha, setSenha] = useState("")
  const [token, setToken] = useState(null)
  const [erro, setErro] = useState("")
  const [pedidos, setPedidos] = useState([])

  async function login() {
    try {
      const resp = await axios.post(`${API}/auth/login`, { email, senha })
      setToken(resp.data.access_token)
      setErro("")
    } catch (e) {
      setErro("Credenciais inválidas")
    }
  }

  async function listarPedidos() {
    try {
      const resp = await axios.get(`${API}/pedidos/listar`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setPedidos(resp.data.pedidos)
    } catch (e) {
      setErro("Erro ao buscar pedidos")
    }
  }

  if (token) {
    return (
      <div>
        <p>✅ Logado!</p>
        <button onClick={listarPedidos}>Listar Pedidos</button>
        {pedidos.length > 0 && (
          <ul>
            {pedidos.map(p => (
              <li key={p.id}>
                Pedido #{p.id} — Status: {p.status} — R$ {p.preco}
              </li>
            ))}
          </ul>
        )}
        {erro && <p style={{color: "red"}}>{erro}</p>}
      </div>
    )
  }

  return (
    <div>
      <h1>Login</h1>
      <input placeholder="Email" onChange={e => setEmail(e.target.value)} />
      <input placeholder="Senha" type="password" onChange={e => setSenha(e.target.value)} />
      <button onClick={login}>Entrar</button>
      {erro && <p style={{color: "red"}}>{erro}</p>}
    </div>
  )
}