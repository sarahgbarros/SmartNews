import React from 'react';

const periods = ["day", "week", "month"];
const periodLabels = { day: "Hoje", week: "Semana", month: "Mês" };

const PeriodTabs = ({ period, setPeriod }) => {
    return (
        <div className="period-tabs-container">
            <nav className="period-tabs" aria-label="Navegação por período">
                {periods.map(p => (
                    <button 
                        key={p} 
                        onClick={() => setPeriod(p)} 
                        className={`tab-button ${period === p ? "active" : ""}`}
                        aria-current={period === p ? "page" : undefined}
                    >
                        {periodLabels[p]}
                    </button>
                ))}
            </nav>
        </div>
    );
};

export default PeriodTabs;