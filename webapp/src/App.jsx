import React, { useState, useEffect } from "react";
import LoginForm from "./components/LoginForm";
import RegisterForm from "./components/RegisterForm";
import NewsPage from "./pages/NewsPage";
import PreferencesPage from "./pages/PreferencesPage";
import { getNews } from "./services/api"; 

// Função auxiliar para comparar arrays (shallow comparison)
const arraysEqual = (a, b) => {
    if (a.length !== b.length) return false;
    // O sort() é crucial aqui para garantir a ordem da comparação
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

    // ... (Outros Handlers de Login/Registro/Back permanecem iguais)

    const handleLoginSuccess = () => {
        setUser(true);
        setView("news");
    };

    const handleRegisterSuccess = () => {
        setUser(true);
        setView("preferences"); 
    };
    
    // ✅ CORREÇÃO: Verifica se as categorias realmente mudaram antes de atualizar o estado
    const handlePreferencesSave = (selectedCategories) => {
        if (!arraysEqual(categories, selectedCategories)) {
            setCategories(selectedCategories);
        }
        setView("news");
    };

    const handleBackToNews = () => {
        setView("news"); 
    }

    // ✅ MELHORIA: A busca só precisa de period e categories
    useEffect(() => {
        const fetchNews = async () => {
            try {
                // Lógica de fallback para a API
                const categoriesToFetch = categories.length > 0 
                    ? categories 
                    : ['general']; 
                    
                const data = await getNews(period, categoriesToFetch);
                setNews(data);
            } catch (err) {
                console.error("Error fetching news:", err);
            }
        };
        fetchNews();
    }, [period, categories]); // Monitora apenas period e categories

    return (
        <div className="container">
            {view === "login" && <LoginForm onSuccess={handleLoginSuccess} />}
            {view === "register" && <RegisterForm onSuccess={handleRegisterSuccess} />}
            
            {view === "preferences" && (
                <PreferencesPage 
                    onSave={handlePreferencesSave} 
                    onBack={handleBackToNews} 
                />
            )}
            
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
                
                {user && view !== "preferences" && <button onClick={() => setView("preferences")}>Preferências</button>}
                {user && <button onClick={() => setUser(null) || setView("news")}>Sair</button>} 
                
                {view !== "news" && <button onClick={() => setView("news")}>Notícias</button>}
            </div>
        </div>
    );
};

export default App;