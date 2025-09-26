import React from 'react';

const NewsCard = ({ news }) => {
    const formattedDate = new Date(news.published_at).toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
    });

    let categoryName = null;
    if (typeof news.category === 'object' && news.category !== null) {
        categoryName = news.category.name;
    } else if (typeof news.category === 'string') {
        categoryName = news.category;
    }

    return (
        <article className="news-card"> 
            
            {categoryName && (
                <span className="news-category">{categoryName}</span>
            )}

            <h2 className="news-title">{news.title}</h2>

            <p className="news-content">{news.content}</p>

            <div className="news-footer">
                <time dateTime={news.published_at} className="news-date-time">
                    {formattedDate}
                </time>
            </div>
            
        </article>
    );
};

export default NewsCard;