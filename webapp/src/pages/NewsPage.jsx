import React, { useState, useEffect } from "react";
import NewsCard from "../components/NewsCard";
import Header from "../components/Header";
import PeriodTabs from "../components/PeriodTabs";
import PaginationControls from "../components/PaginationControls"; 
import { getNews } from "../services/api";

const PAGE_SIZE = 10; 

const NewsPage = ({ userCategories = [] }) => {
    const [news, setNews] = useState([]);
    const [period, setPeriod] = useState("day");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [page, setPage] = useState(1);
    const [paginationData, setPaginationData] = useState({ count: 0, next: null, previous: null });

    useEffect(() => {
        setPage(1); 
    }, [period, userCategories]); 

    useEffect(() => {
        const fetchNews = async () => {
            setLoading(true);
            setError(null);
            
            try {
                const categoriesToFetch = Array.isArray(userCategories) ? userCategories.map(c => c.toLowerCase()) : [];
                const newsResponse = await getNews(period, categoriesToFetch, page); 
                
                let newsArray = [];
                let count = 0;
                let next = null;
                let previous = null;

                if (Array.isArray(newsResponse)) {
                    newsArray = newsResponse;
                    count = newsArray.length; 
                } else if (newsResponse && Array.isArray(newsResponse.results)) {
                    newsArray = newsResponse.results;
                    count = newsResponse.count;
                    next = newsResponse.next;
                    previous = newsResponse.previous;
                } else {
                    throw new Error("Formato de resposta inesperado do servidor.");
                }
                
                setPaginationData({ 
                    count: count, 
                    next: next, 
                    previous: previous 
                });
                
                setNews(newsArray); 
                setError(null);
                
                if (newsArray.length === 0) {
                    setError("Nenhuma notícia encontrada para o período e categorias selecionados.");
                }
                
            } catch (err) {
                setError(err.message || "Ocorreu um erro desconhecido ao carregar as notícias."); 
                setNews([]);
            } finally {
                setLoading(false);
            }
        };

        fetchNews();
        
    }, [period, userCategories, page]); 

    const totalPages = Math.ceil(paginationData.count / PAGE_SIZE);

    return (
        <div className="container news-page"> 
            <Header />
            
            <PeriodTabs period={period} setPeriod={setPeriod} />

            <main className="content-area">
                
                {error && !loading && (
                    <div className="error-message page-error" role="alert">
                        {error}
                    </div>
                )}

                {loading ? (
                    <div className="loading-state">
                        <p className="spinner large">🌀</p>
                        <p>Carregando as últimas notícias...</p>
                    </div>
                ) : (
                    <div className="news-list">
                        {news.length === 0 && !error ? (
                            <div className="empty-state">
                                <p>📰 Nenhuma notícia encontrada.</p>
                                <p className="hint">Tente mudar o período ou remover os filtros de categoria.</p>
                            </div>
                        ) : (
                            news.map(item => <NewsCard key={item.id} news={item} />)
                        )}
                    </div>
                )}
            </main>
            
            {!loading && news.length > 0 && (
                <PaginationControls
                    page={page}
                    setPage={setPage}
                    totalPages={totalPages}
                />
            )}
        </div>
    );
};

export default NewsPage;