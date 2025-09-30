const API_URL = "http://localhost:8000/api";

const getAccess = () => localStorage.getItem("access_token");

export const getUserData = () => {
    const userString = localStorage.getItem("user");
    if (userString) {
        try {
            return JSON.parse(userString);
        } catch (e) {
            console.error("Erro ao fazer parse dos dados do usuário no localStorage:", e);
            return null;
        }
    }
    return null;
};

const setAuthData = (access, user) => {
    localStorage.setItem("access_token", access);
    localStorage.setItem("user", JSON.stringify(user));
};

const clearTokens = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user");
};

const formatErrorDetail = (errorData) => {
    if (typeof errorData === 'string') {
        return errorData;
    }
    
    if (typeof errorData === 'object' && errorData !== null) {
        const messages = Object.keys(errorData).map(key => {
            const fieldName = key.charAt(0).toUpperCase() + key.slice(1).replace('_', ' ');
            const errorList = Array.isArray(errorData[key]) ? errorData[key].join(' ') : String(errorData[key]);
            
            return `${fieldName}: ${errorList}`;
        });
        
        return messages.join(' | ');
    }
    
    return "Ocorreu um erro desconhecido no servidor.";
};

async function fetchWithAuth(url, options = {}) {
    const access = getAccess();
    const headers = { 
        ...options.headers, 
        ...(access ? { Authorization: `Bearer ${access}` } : {}) 
    };
    
    let response = await fetch(url, { ...options, headers });
    let data;

    const contentType = response.headers.get("content-type");
    if (contentType && contentType.includes("application/json")) {
        try {
            data = await response.json();
        } catch (e) {
            data = {};
        }
    }

    if (response.status === 401) {
        clearTokens();
        throw new Error("Sessão expirada. Faça login novamente.");
    }

    if (!response.ok) {
        const errorData = data || {};
        throw new Error(errorData.detail || formatErrorDetail(errorData) || `Erro ${response.status} na requisição.`);
    }
    
    return data;
}

export async function login(email, password) {
    const res = await fetch(`${API_URL}/user/login/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
    });

    let data = {};
    const contentType = res.headers.get("content-type");
    if (res.status !== 204 && contentType && contentType.includes("application/json")) {
        data = await res.json();
    }

    if (!res.ok) throw new Error(data.error || data.detail || formatErrorDetail(data) || "Erro no login");

    const user = data.user;
    setAuthData(data.access, user); 

    return { user: user }; 
}

export async function register(email, username, password, passwordConfirm) {
    const res = await fetch(`${API_URL}/user/register/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, username, password, password_confirm: passwordConfirm }),
    });

    let data = {};
    const contentType = res.headers.get("content-type");
    if (res.status !== 204 && contentType && contentType.includes("application/json")) {
        data = await res.json();
    }

    if (!res.ok) {
        const errorMessage = formatErrorDetail(data);
        throw new Error(errorMessage || "Erro no registro");
    }

    const user = data.user;
    setAuthData(data.access, user); 

    return { user: user }; 
}

export const getNews = async (period, categories = []) => {
    const params = {
        period: period,
    };

    if (categories && categories.length > 0) {
        params.category__in = categories.join(',');
    }
    
    const queryParams = new URLSearchParams(params).toString();
    const url = `${API_URL}/news/?${queryParams}`;

    try {
        const data = await fetchWithAuth(url);
        return data;
    } catch (error) {
        console.error("Erro na API ao buscar notícias:", error);
        throw error;
    }
};


export async function savePreferences(categories = []) {
    const url = `${API_URL}/user/preferences/`;
    
    const updatedUser = await fetchWithAuth(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ categories }),
    });

    const currentToken = getAccess();
    if (currentToken && updatedUser) {
        setAuthData(currentToken, updatedUser);
        return updatedUser;
    }
    
    if (!updatedUser && currentToken) {
        const currentUser = getUserData();
        return currentUser; 
    }
    return updatedUser;
}

export const getCategories = async () => {
    const url = `${API_URL}/news/categories/`; 
    
    const response = await fetch(url);
    
    let data;
    const contentType = response.headers.get("content-type");
    if (contentType && contentType.includes("application/json")) {
        data = await response.json();
    }
    
    if (!response.ok) {
        throw new Error(data?.detail || "Erro ao buscar categorias disponíveis.");
    }

    return data;
};

export function logout() {
    clearTokens();
}