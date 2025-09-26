import React from "react";
import { useNavigate, Link } from "react-router-dom";
import RegisterForm from "../components/RegisterForm";

const RegisterPage = () => {
    const navigate = useNavigate();

    const handleRegisterSuccess = () => {
        navigate("/login"); 
    };

    return (
        <div className="auth-wrapper"> 
            
            <div className="login-card"> 
                <RegisterForm onSuccess={handleRegisterSuccess} />
                
                <div className="register-cta">
                    <p>
                        Já tem conta? <Link to="/login" className="register-link">
                            <strong>Entrar agora</strong>
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

export default RegisterPage;