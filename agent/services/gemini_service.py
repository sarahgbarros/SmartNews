from google import genai

class GeminiService:
    def __init__(self):
        self.client = genai.Client()

    def generate_summary(self, news_dict: dict):

        try:
            title = news_dict.get("title", "No Title")
            content = news_dict.get("content", "No Content")

            prompt = f"Faça um resumo conciso e profissional a seguinte notícia em 40 palavras :\n\nTítulo: {title}\nConteúdo: {content}\n"
            response = self.client.generate_text(
                model="gemini-1.5-flashgemini-2.5-flash",
                prompt=prompt,
                temperature=0.7,
            )
            summary = response.text.strip()
            return summary
        
        except Exception as e:
            print(f"Erro ao gerar resumo com Gemini: {e}")
            return "Resumo indisponível."

