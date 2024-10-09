import requests
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum
from django.utils.timezone import now
from .models import Visita


# Create your views here.
def get_client_ip(request):
    """Função para obter o IP do cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')    
    return ip

def get_location(ip):
    """Função para obter a localização do IP usando a API ipinfo.io."""
    try:
        response = requests.get(f'https://ipinfo.io/{ip}/json')
        data = response.json()
        cidade = data.get('city', 'Desconhecido')
        regiao = data.get('region', 'Desconhecido')
        return cidade, regiao
    
    except:
        return 'Desconhecida', 'Desconhecida'    

def home(request):
    ip = get_client_ip(request)

    # Verifica se o IP já existe no banco de dados
    visita, created = Visita.objects.get_or_create(ip=ip)

    # Se a visita for nova ou se a cidade/região ainda não estiverem preenchidas
    if created or not visita.cidade or not visita.regiao:
        # Se for a primeira visita ou se os dados de localização estiverem ausentes, busca a localização
        cidade, regiao = get_location(ip)
        visita.cidade = cidade
        visita.regiao = regiao

    # Incrementa o contador de visitas
    visita.visitas += 1
    visita.save()


    # Pega o número total de visitas
    total_visitas = Visita.objects.aggregate(total=Sum('visitas'))['total'] or 0

    # Ranking dos visitantes
    ranking = Visita.objects.order_by('-visitas')[:10] # top 10 visitantes 

    # Contexto a ser passado para o template
    context = {
        'ip': ip,
        'visita_numero': total_visitas,
        'ranking': ranking,
        'cidade': visita.cidade,  # Cidade da instância da visita
        'regiao': visita.regiao   # Região da instância da visita
    }  
    return render(request, 'home.html', context)