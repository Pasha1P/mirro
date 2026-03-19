import { useContext, useState } from "react"
import { useNavigate } from "react-router"
import type { errors } from "../components/types"
import { Context } from "../App"

function Registration() {
    const [user, setUser] = useState({ username: '', email: '', password: '' })
    const [err, setErr] = useState<errors>()
    const navigate = useNavigate()
    const { XCSRFToken, token } = useContext(Context);
    const submitt = (e: React.SubmitEvent) => {
        e.preventDefault()
        setErr(undefined)
        const formData = new FormData()
        formData.append('username', user.username)
        formData.append('email', user.email)
        formData.append('password', user.password)
        const headers: HeadersInit = { 'X-CSRFToken': XCSRFToken }
        if (token) { headers['Authorization'] = `Bearer ${token}` }
        fetch('http://127.0.0.1:8000/api/users/', { headers: headers, method: 'POST', body: formData, credentials: 'include', })
            .then(res => { return res.json() })
            .then(data => {
                console.log(data.errors[0])
                // if (data.code >= 200 && data.code < 300) navigate('/login')
                    
                // if (data.errors) setErr({ name: data.errors[0].title, text: data.errors[0].message })
                // else setErr({ name: 'general', text: data.message || 'Произошла ошибка' })

            })
            .catch(() => { setErr({ name: 'general', text: 'Ошибка сети' }) })
    }
    return (
        <>
            <div className="container-s">
                <div id="register-page" className="page active">
                    <h1>Регистрация</h1>
                    {err && (<div id="login-error" className="error-message">{err.text}</div>)}

                    <form id="register-form" onSubmit={submitt}>
                        <div className="form-group">
                            <label htmlFor="register-name">Имя</label>
                            <input type="text" id="register-name" className={err?.name === 'username' ? "error" : ""} onChange={(e) => { setUser(user => ({ ...user, username: e.target.value })) }} required />
                        </div>
                        <div className="form-group">
                            <label htmlFor="register-email">Email</label>
                            <input type="email" id="register-email" className={err?.name === 'email' ? "error" : ""} onChange={(e) => { setUser(user => ({ ...user, email: e.target.value })) }} required />
                        </div>
                        <div className="form-group">
                            <label htmlFor="register-password">Пароль</label>
                            <input type="password" id="register-password" className={err?.name === 'password' ? "error" : ""} onChange={(e) => { setUser(user => ({ ...user, password: e.target.value })) }} required />
                        </div>
                        <button type="submit">Зарегистрироваться</button>
                    </form>
                    <p style={{ marginTop: '20px' }}>Уже есть аккаунт? <a href="" onClick={() => { navigate('/login') }}>Войти</a></p>
                </div>
            </div>
        </>
    )
}
export default Registration