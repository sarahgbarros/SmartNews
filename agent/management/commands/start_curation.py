from agent.tasks import generate_news_task, import_news_from_files_task
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Inicia o processo de curadoria de notícias'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Iniciando a curadoria de notícias...'))
        
        tasks_initiated = 0

        try:
            result_generate = generate_news_task.apply_async(queue='producer')
            self.stdout.write(
                self.style.SUCCESS(f'Task de GERAÇÃO (ID: {result_generate.id}) enviada para o Produtor.')
            )
            tasks_initiated += 1
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Erro ao iniciar a Task de GERAÇÃO: {e}'))

        try:
            result_import = import_news_from_files_task.apply_async(queue='producer')
            self.stdout.write(
                self.style.SUCCESS(f'Task de IMPORTAÇÃO (ID: {result_import.id}) enviada para o Produtor.')
            )
            tasks_initiated += 1
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Erro ao iniciar a Task de IMPORTAÇÃO: {e}'))
            
        if tasks_initiated > 0:
            self.stdout.write(self.style.SUCCESS('Curadoria iniciada com sucesso. Os Workers Produtores foram acionados para ambas as fontes.'))
        else:
            self.stdout.write(self.style.ERROR('Nenhuma Task de curadoria pôde ser iniciada.'))