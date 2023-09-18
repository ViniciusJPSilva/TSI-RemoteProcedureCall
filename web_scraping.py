import requests
from requests import exceptions
from bs4 import BeautifulSoup
from typing import List, Tuple

def get_links(url: str, classes: str) -> List[Tuple[str, str]]:
    """
    Obtém os links da página da web com base na URL fornecida e nas classes especificadas.

    :param url: A URL da página da web a ser analisada.
    :param classes: As classes dos elementos HTML a serem procurados para extrair os links, separadas por espaço em branco.
    :return: Uma lista de links encontrados na página ou None se não houver links disponíveis.
    """
    # Padroniza a URL.
    url = standardize_url(url)

    # Cria a requisição.
    response = create_request(url)

    if not response: 
        return None

    # Extrai os links da página.
    links = create_links_list(url, classes, BeautifulSoup(response.content, 'html.parser'))

    if not links: 
        return None

    return links



def standardize_url(url: str) -> str:
    """
    Padroniza uma URL, adicionando "https://" por padrão e garantindo que o domínio comece com "www." se necessário.

    :param url: A URL a ser padronizada.
    :return: A URL padronizada.
    """
    if not url.startswith("https://") and not url.startswith("http://"):
        url = "https://" + url  # Adiciona "https://" por padrão

    parsed_url = url.split("//")
    domain = parsed_url[1] if len(parsed_url) > 1 else parsed_url[0]

    if not domain.startswith("www."):
        url = url.replace(domain, "www." + domain)

    return url



def create_request(url: str) -> requests.Response: 
    """
    Cria uma requisição HTTP e retorna a resposta.
    
    Tenta criar uma requisição com verificação de certificados SSL por padrão, 
    mas se não for possível devido a erros de SSL, cria a requisição sem verificar os certificados.

    :param url: A URL para a qual a requisição HTTP será feita.
    :return: A resposta da requisição HTTP ou None em caso de falha.
    """
    try:
        return requests.get(url)
    except (exceptions.SSLError):
        return requests.get(url, verify = False)
    except (exceptions.ConnectionError, exceptions.MissingSchema, 
            exceptions.InvalidSchema, exceptions.InvalidURL):
        return None
    except Exception:
        return None


def create_links_list(url: str, classes: str, soup: BeautifulSoup) -> List[Tuple[str, str]]:
    """
    Cria uma lista de links com base nas tags 'a' e classes especificadas em um objeto BeautifulSoup.

    :param url: A URL da página da web analisada, usada para tratar links relativos.
    :param classes: As classes das tags 'a' a serem procuradas.
    :param soup: O objeto BeautifulSoup que representa o conteúdo da página da web.
    :return: Uma lista de tuplas contendo texto do link e o link tratado.
    """
    links = []
    for link_tag in soup.find_all('a', classes):
        link_href = link_tag.get('href')
        
        if(link_href):
            treated_link = treatLink(url,link_href)
       
            if link_href:
                links.append(
                   (link_tag.text, treated_link)
                )
      
    return links


def treatLink(url_page: str, link: str) -> str: 
    """
    Trata um link para torná-lo completo (URL completa) ou retorna o link original se não for necessário tratamento.

    :param url_page: A URL da página da web atual, usada como base para links relativos.
    :param link: O link a ser tratado.
    :return: O link tratado como uma URL completa ou o link original se não for necessário tratamento.
    """
    if link.startswith("/"):
        return f"{url_page}{link}"
    if link.startswith("#"):
        return url_page
    
    return link
