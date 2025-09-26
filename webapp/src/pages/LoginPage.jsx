import React from "react";
import { useNavigate, Link } from "react-router-dom";
import LoginForm from "../components/LoginForm";

const LoginPage = () => {
    const navigate = useNavigate();

    const handleLoginSuccess = () => {
        navigate("/news"); 
    };

    const handleForgotPassword = () => {
        navigate("/forgot-password"); 
    };

    return (
    
        <div className="auth-wrapper"> 
            
            <div className="login-card"> 
            
                <LoginForm 
                    onSuccess={handleLoginSuccess} 
                    onForgotPassword={handleForgotPassword}
                />
                
                <div className="register-cta">
                    <p>
                        Não tem conta? <Link to="/register" className="register-link">
                            **Registre-se aqui**
                        </Link>
                    </p>
                </div>
                
            </div>
            

            <footer className="auth-footer">
                <Link to="/terms" className="footer-link">Termos de Uso</Link> | <Link to="/privacy" className="footer-link">Política de Privacidade</Link>
            </footer>
        </div>
    );
};

export default LoginPage;