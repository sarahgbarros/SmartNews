import React, { useState, useEffect } from "react";
import LoginForm from "./components/LoginForm";
import RegisterForm from "./components/RegisterForm";
import NewsPage from "./pages/NewsPage";
import { getNews } from "./services/api"; 

const arraysEqual = (a, b) => {
    if (a.length !== b.length) return false;
    
    const sortedA = [...a].sort(); 
    const sortedB = [...b].sort();
    for (let i = 0; i < sortedA.length; i++) {
        if (sortedA[i] !== sortedB[i]) return false;
    }
    return true;
};

const App = () => {
    const [user, setUser] = useState(null);
    const [view, setView] = useState("news"); 
    const [categories, setCategories] = useState([]);
    const [news, setNews] = useState([]);
    const [period, setPeriod] = useState("day");

    const handleLoginSuccess = () => {
        setUser(true);
        setView("news");
    };

    const handleRegisterSuccess = () => {
        setUser(true);
        setView("news"); 
    };


    const handleBackToNews = () => {
        setView("news"); 
    }

    useEffect(() => {
    const fetchNews = async () => {
        try {
                
            const categoriesToFetch = categories.length > 0 
                ? categories 
                : ['general']; 
                    
            const data = await getNews(period, categoriesToFetch);

            if (Array.isArray(data)) {
                setNews(data);
            } else if (data && Array.isArray(data.results)) {
                setNews(data.results);
            } else {
                setNews([]);
            }
        } catch (err) {
            console.error("Error fetching news:", err);
        }
    };
    fetchNews();
}, [period, categories]);


    return (
        <div className="container">
            {view === "login" && <LoginForm onSuccess={handleLoginSuccess} />}
            {view === "register" && <RegisterForm onSuccess={handleRegisterSuccess} />}           
            {view === "news" && (
                <NewsPage 
                    userCategories={categories}
                    news={news}
                    period={period}
                    onPeriodChange={setPeriod}
                />
            )}
            
            <div style={{ marginTop: "20px", textAlign: "center" }}>
                {!user && view !== "login" && <button onClick={() => setView("login")}>Entrar</button>}
                {!user && view !== "register" && <button onClick={() => setView("register")}>Registrar</button>}
                {user && <button onClick={() => setUser(null) || setView("news")}>Sair</button>} 
                
                {view !== "news" && <button onClick={() => setView("news")}>Notícias</button>}
            </div>
        </div>
    );
};

export default App;