import { Context } from "../App"
import { useContext, useState } from "react"
import { useNavigate } from "react-router"
import type { errors } from "../components/types"

function Login() {
    const navigate = useNavigate()
    const [user, setUser] = useState({ email: '', password: '' })
    const [err, setErr] = useState<errors>()
    const { XCSRFToken, token, setToken } = useContext(Context);
    const submitt = (e: React.SubmitEvent) => {
        e.preventDefault()
        setErr(undefined)
        const formData = new FormData()
        formData.append('email', user.email)
        formData.append('password', user.password)
        const headers: HeadersInit = { 'X-CSRFToken': XCSRFToken }
        if (token) { headers['Authorization'] = `Bearer ${token}` }
        fetch('http://127.0.0.1:8000/api/auth/', { headers: headers, method: 'POST', body: formData, credentials: 'include', })
            .then(res => { return res.json() })
            .then(data => {
                if (data.code >= 200 && data.code < 300) {
                    setToken(data.data['token'])
                    navigate('/boards')
                }
                else {
                    if (data.errors) setErr({ name: data.errors[0].title, text: data.errors[0].message })
                    else setErr({ name: 'general', text: data.message || 'Произошла ошибка' })
                }
            })
            .catch(() => { setErr({ name: 'general', text: 'Ошибка сети' }) })
    }
    return (
        <>
            <div className="container-s">
                <div id="login-page" className="page active">
                    <h1>Вход в систему</h1>
                    {err && (<div id="login-error" className="error-message">{err.text}</div>)}
                    <form id="login-form" onSubmit={submitt}>
                        <div className="form-group" id="div-login-email">
                            <label htmlFor="login-email">Email</label>
                            <input type="email" id="login-email" className={err?.name === 'email' ? "error" : ""} onChange={(e) => { setUser(user => ({ ...user, email: e.target.value })) }} required />
                        </div>
                        <div className="form-group">
                            <label htmlFor="login-password">Пароль</label>
                            <input type="password" id="login-password" className={err?.name === 'password' ? "error" : ""} onChange={(e) => { setUser(user => ({ ...user, password: e.target.value })) }} required />
                        </div>
                        <button type="submit">Войти</button>
                    </form>
                    <p style={{ marginTop: '20px' }}>Нет аккаунта? <a href="" onClick={() => { navigate('/registration') }}>Зарегистрироваться</a></p>
                </div>
            </div>
        </>
    )
}
export default Login;
