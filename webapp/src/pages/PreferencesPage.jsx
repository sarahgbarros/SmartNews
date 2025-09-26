import React, { useState, useEffect } from "react";
import { savePreferences, getCategories, getUserData } from "../services/api";

const PreferencesPage = ({ onSave, onBack }) => {
    const currentUser = getUserData();
    
    const initialSelectedNames = (currentUser?.categories || []).map(cat => cat.name || cat);
    
    const [availableCategories, setAvailableCategories] = useState([]);
    const [selectedCategoryNames, setSelectedCategoryNames] = useState(initialSelectedNames); 
    const [loading, setLoading] = useState(false);
    const [saveStatus, setSaveStatus] = useState(null); 

    useEffect(() => {
        const loadCategories = async () => {
            try {
                const categories = await getCategories(); 
                setAvailableCategories(categories);
            } catch (error) {
                console.error("Erro ao carregar categorias:", error);
            }
        };
        loadCategories();
    }, []);
    
    const handleCategoryToggle = (categoryName) => {
        setSelectedCategoryNames(prev =>
            prev.includes(categoryName)
                ? prev.filter(name => name !== categoryName)
                : [...prev, categoryName]
        );
    };

    const handleSave = async () => {
        setLoading(true);
        setSaveStatus(null);
        
        try {
    
            const updatedUser = await savePreferences(selectedCategoryNames); 
            
            const categoriesToPassToApp = (updatedUser?.categories || []).map(cat => cat.name || cat);
            
            setSaveStatus('success');
            onSave(categoriesToPassToApp.length > 0 ? categoriesToPassToApp : selectedCategoryNames);
            
        } catch (error) {
            console.error("Erro ao salvar preferências:", error);
            setSaveStatus('error');
    
            const errorMessage = error.message || "Ocorreu um erro desconhecido no servidor.";
            alert(`Erro ao salvar: ${errorMessage}`); 
        } finally {
            setLoading(false);
        }
    };

    const handleBackToNews = () => {
        onBack();
    };

    return (
        <div className="preferences-page container">
            <div className="pref-header">
                <h2>Minhas Preferências de Notícias</h2>
                <button 
                    onClick={handleBackToNews} 
                    className="back-button secondary-auth"
                >
                    &larr; Voltar para Notícias
                </button>
            </div>
            
            <p>Selecione suas categorias de interesse:</p>
            
            <div className="category-selection">
                {availableCategories.map(cat => (
                    <button
                        key={cat.id}
                        onClick={() => handleCategoryToggle(cat.name)}
                        className={`category-button ${selectedCategoryNames.includes(cat.name) ? 'selected' : ''}`}
                        disabled={loading}
                    >
                        {cat.name}
                    </button>
                ))}
            </div>
            
            <button 
                onClick={handleSave} 
                disabled={loading || selectedCategoryNames.length === 0}
                className="save-button primary-auth"
            >
                {loading ? 'Salvando...' : 'Salvar Preferências'}
            </button>

            {saveStatus === 'success' && <p className="status-success">Preferências salvas com sucesso!</p>}
            {saveStatus === 'error' && <p className="status-error">Falha ao salvar. Verifique o console.</p>}
        </div>
    );
};

export default PreferencesPage;