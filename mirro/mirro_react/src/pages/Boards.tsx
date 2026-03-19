import React, { useContext, useEffect, useState } from "react"
import type { errors } from "../components/types"
import { Context } from "../App";
import { useNavigate } from "react-router";

function Boards() {
    const navigate = useNavigate()
    const [err, setErr] = useState<errors>()
    const [activeFilter, setActiveFilter] = useState('all')
    const [boards, setBoards] = useState([{}])
    const [sort, setSort] = useState('');
    const { XCSRFToken, token, setToken } = useContext(Context)
    const logout = (e: React.MouseEvent) => {
        e.preventDefault()
        setErr(undefined)
        setToken('')
        fetch('http://127.0.0.1:8000/api/logout/')
            .catch(() => { setErr({ name: 'general', text: 'Ошибка сети' }) })
    }
    useEffect(() => {
        setErr(undefined)
        const headers: HeadersInit = { 'X-CSRFToken': XCSRFToken }
        if (token) { headers['Authorization'] = `Bearer ${token}` }
        const formData = new FormData()
        formData.append('filter_param', activeFilter)
        formData.append('sort', sort)
        fetch('http://127.0.0.1:8000/api/boards/', { headers: headers, method: 'GET', body: formData, credentials: 'include', })
            .then(res => { return res.json() })
            .then(data => {
                if (data.code >= 200 && data.code < 300 && data.data) setBoards(data.data)
                else setErr({ name: 'general', text: data.message || 'Произошла ошибка' })
            })
            .catch(() => { setErr({ name: 'general', text: 'Ошибка сети' }) })
    }, [activeFilter, activeFilter]);
    return (
        <>
            <div className="container">
                <div id="boards-page" className="page active">
                    <div className="logout-container">
                        <button onClick={() => navigate('/login')}>Вход</button>
                        <button id="logout-btn" onClick={(e) => logout(e)} className="btn-logout">Выйти</button>
                    </div>

                    <h1>Доски</h1>

                    <div className="filter-controls">
                        <div className="nav-tabs">
                            <div className={`nav-tab ${activeFilter === 'all' ? 'active' : ''}`} onClick={() => setActiveFilter('all')}>Все доски                                </div>
                            <div className={`nav-tab ${activeFilter === 'accessed' ? 'active' : ''}`} onClick={() => setActiveFilter('accessed')}>Доступные мне                                </div>
                            <div className={`nav-tab ${activeFilter === 'publishedall' ? 'active' : ''}`} onClick={() => setActiveFilter('published')}>Публичные                                </div>
                        </div>

                        <div className="sort-control">
                            <select id="sort-select">
                                <option onClick={() => setSort('')}>Без сортировки</option>
                                <option onClick={() => setSort('likes')}>По лайкам</option>
                            </select>
                        </div>

                        <button id="create-board-btn">Создать доску</button>
                    </div>

                    <div className="board-grid" id="boards-container">
                        {boards.map()}
                        <div className="board-card" onclick="location.href='board.html'">
                            <div className="board-title">Проект Alpha</div>
                            <div className="board-owner">Владелец: Иван Петров</div>
                            <div className="board-stats">
                                <span className="like-btn liked">
                                    ❤ <span>24</span>
                                </span>
                                <span>Доступ: ✏️</span>
                            </div>
                        </div>

                        <div className="board-card" onclick="location.href='board.html'">
                            <div className="board-title">Дизайн сайта</div>
                            <div className="board-owner">Владелец: Мария Сидорова</div>
                            <div className="board-stats">
                                <span className="like-btn">
                                    ❤ <span>18</span>
                                </span>
                                <span>Доступ: 👁️</span>
                            </div>
                        </div>

                        <div className="board-card" onclick="location.href='board.html'">
                            <div className="board-title">План маркетинга</div>
                            <div className="board-owner">Владелец: Алексей Козлов</div>
                            <div className="board-stats">
                                <span className="like-btn liked">
                                    ❤ <span>31</span>
                                </span>
                                <span>Доступ: 👥</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div id="create-board-modal" className="modal">
                    <div className="modal-content">
                        <span className="close-modal">&times;</span>
                        <h2>Создать новую доску</h2>

                        {err && (<div id="login-error" className="error-message">{err.text}</div>)}

                        <form id="create-board-form">
                            <div className="form-group">
                                <label htmlFor="board-title-input">Название доски</label>
                                <input type="text" id="board-title-input" className="error" required />
                            </div>
                            <button type="submit">Создать</button>
                        </form>
                    </div>
                </div>
            </div>

            <script>

            </script>
        </>
    )
}
export default Boards