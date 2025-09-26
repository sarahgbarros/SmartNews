import React, { useState } from "react";
import { login } from "../services/api"; 

const LoginForm = ({ onSuccess, onForgotPassword }) => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const [showPassword, setShowPassword] = useState(false); 


    const validateForm = () => {
        if (!email.trim() || !password.trim()) {
            setError("Por favor, preencha todos os campos.");
            return false;
        }
        
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            setError("Por favor, insira um email válido.");
            return false;
        }
        return true;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        
        
        if (!validateForm()) {
            return;
        }
        
        setLoading(true);
        try {
            await login(email, password);
            onSuccess();

            setEmail("");
            setPassword(""); 
        } catch (err) {
    
            const errorMessage = err.message || "Falha no login. Verifique suas credenciais.";
            setError(errorMessage);
        } finally {
            setLoading(false);
        }
    };

    return (
        
        <form onSubmit={handleSubmit} className="form-container" aria-label="Formulário de Login">
            <h2>Bem-vindo de Volta!</h2>
            
        
            {error && (
                <div className="error-message" role="alert"> 
                    <p>{error}</p>
                </div>
            )}

            
            <div className="input-group">
                <label htmlFor="email">Email</label>
                <input 
                    id="email" 
                    type="email" 
                    placeholder="seu.email@exemplo.com" 
                    value={email} 
                    onChange={e => setEmail(e.target.value)} 
                    required 
                    autoComplete="username" 
                    aria-describedby="email-hint"
                />
            </div>
            
            <div className="input-group password-group">
                <label htmlFor="password">Senha</label>
                <input 
                    id="password" 
                    type={showPassword ? "text" : "password"} 
                    placeholder="Senha" 
                    value={password} 
                    onChange={e => setPassword(e.target.value)} 
                    required 
                    autoComplete="current-password"
                />
                <button 
                    type="button" 
                    className="toggle-password-btn" 
                    onClick={() => setShowPassword(!showPassword)}
                    aria-label={showPassword ? "Ocultar senha" : "Mostrar senha"}
                >
                </button>
            </div>
            

            {onForgotPassword && (
                <div className="forgot-password-link">
                    <button type="button" onClick={onForgotPassword} className="link-button">
                        Esqueceu a senha?
                    </button>
                </div>
            )}

            <button 
                type="submit" 
                disabled={loading}
                className="submit-button"
            >
                {loading ? (
                    <>
                        {/* Ícone de loading (spinner) */}
                        <span className="spinner" role="status" aria-hidden="true">🔄</span> 
                        Entrando...
                    </>
                ) : (
                    "Entrar"
                )}
            </button>
        </form>
    );
};

export default LoginForm;