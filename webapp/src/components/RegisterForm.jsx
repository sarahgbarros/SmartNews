import React, { useState } from "react";
import { register } from "../services/api"; 

const RegisterForm = ({ onSuccess }) => {
    // ALTERAÇÃO: Nome agora é username, e adicionamos passwordConfirm
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [passwordConfirm, setPasswordConfirm] = useState(""); // Novo campo
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const [showPassword, setShowPassword] = useState(false);
    const [showPasswordConfirm, setShowPasswordConfirm] = useState(false); // Novo estado

    const validateForm = () => {
        if (!username.trim() || !email.trim() || !password.trim() || !passwordConfirm.trim()) {
            setError("Todos os campos são obrigatórios.");
            return false;
        }
        if (password.length < 6) { 
            setError("A senha deve ter pelo menos 6 caracteres.");
            return false;
        }
        if (password !== passwordConfirm) { // Validação de confirmação
            setError("A senha e a confirmação de senha não coincidem.");
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
            // ALTERAÇÃO: Chama register com os 4 campos necessários pelo backend
            await register(email, username, password, passwordConfirm); 
            onSuccess();
        } catch (err) {
            // Captura o erro formatado vindo do api.js
            const errorMessage = err.message || "Falha no registro. Tente novamente.";
            setError(errorMessage);
        } finally {
            setLoading(false);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="form-container" aria-label="Formulário de Cadastro">
            <h2>Crie sua Conta</h2>
            
            {error && (
                <div className="error-message" role="alert"> 
                    <p>{error}</p>
                </div>
            )}

            {/* Campo Username (anteriormente Nome) */}
            <div className="input-group">
                <label htmlFor="username">Nome de Usuário</label>
                <input 
                    id="username" 
                    type="text" 
                    placeholder="Seu nome de usuário" 
                    value={username} 
                    onChange={e => setUsername(e.target.value)} 
                    required 
                    autoComplete="username"
                />
            </div>

            {/* Campo Email */}
            <div className="input-group">
                <label htmlFor="email">Email</label>
                <input 
                    id="email" 
                    type="email" 
                    placeholder="seu.email@exemplo.com" 
                    value={email} 
                    onChange={e => setEmail(e.target.value)} 
                    required 
                    autoComplete="email"
                />
            </div>
            
            {/* Campo Senha com Controle de Visibilidade */}
            <div className="input-group password-group">
                <label htmlFor="password">Senha</label>
                <input 
                    id="password" 
                    type={showPassword ? "text" : "password"} 
                    placeholder="Crie uma senha segura" 
                    value={password} 
                    onChange={e => setPassword(e.target.value)} 
                    required 
                    autoComplete="new-password"
                />
                <button 
                    type="button" 
                    className="toggle-password-btn" 
                    onClick={() => setShowPassword(!showPassword)}
                    aria-label={showPassword ? "Ocultar senha" : "Mostrar senha"}
                >
                    {showPassword ? "👁️" : "🔒"} 
                </button>
            </div>
            
            {/* NOVO: Campo Confirmação de Senha */}
            <div className="input-group password-group">
                <label htmlFor="password_confirm">Confirme a Senha</label>
                <input 
                    id="password_confirm" 
                    type={showPasswordConfirm ? "text" : "password"} 
                    placeholder="Confirme sua senha" 
                    value={passwordConfirm} 
                    onChange={e => setPasswordConfirm(e.target.value)} 
                    required 
                    autoComplete="new-password"
                />
                <button 
                    type="button" 
                    className="toggle-password-btn" 
                    onClick={() => setShowPasswordConfirm(!showPasswordConfirm)}
                    aria-label={showPasswordConfirm ? "Ocultar confirmação" : "Mostrar confirmação"}
                >
                    {showPasswordConfirm ? "👁️" : "🔒"} 
                </button>
            </div>
            
            <button 
                type="submit" 
                disabled={loading}
                className="submit-button"
            >
                {loading ? (
                    <>
                        <span className="spinner" role="status" aria-hidden="true">🔄</span> 
                        Registrando...
                    </>
                ) : (
                    "Registrar"
                )}
            </button>
        </form>
    );
};

export default RegisterForm;