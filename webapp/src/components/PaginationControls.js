import React from 'react';

const PaginationControls = ({ page, setPage, totalPages }) => {
    if (totalPages <= 1) return null; 

    const isFirstPage = page === 1;
    const isLastPage = page === totalPages;

    return (
        <div className="pagination-controls">
            <button 
                className="pagination-button"
                onClick={() => setPage(page - 1)}
                disabled={isFirstPage}
                aria-label="Página anterior"
            >
                &larr; Anterior
            </button>
            
            <span className="pagination-text">
                Página **{page}** de **{totalPages}**
            </span>

            <button
                className="pagination-button"
                onClick={() => setPage(page + 1)}
                disabled={isLastPage}
                aria-label="Próxima página"
            >
                Próxima &rarr;
            </button>
        </div>
    );
};

export default PaginationControls;