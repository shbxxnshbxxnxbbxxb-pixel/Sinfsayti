from django.core.management.base import BaseCommand
from main.views import calculate_weekly_leader

class Command(BaseCommand):
    help = 'Haftalik liderni aniqlaydi va WeeklyLeader modeliga yozadi.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Haftalik liderni hisoblash boshlandi...'))
        calculate_weekly_leader()
        self.stdout.write(self.style.SUCCESS('Haftalik liderni hisoblash yakunlandi.'))
