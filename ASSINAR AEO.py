# Criado por: F. Wellisson
# Data: 29/05/2026

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
import getpass
import time

def login(usuario, senha):
    campo_do_usuario = wait.until(EC.element_to_be_clickable((By.ID, "txtLogin")))
    campo_do_usuario.send_keys(usuario)

    campo_da_senha = wait.until(EC.element_to_be_clickable((By.ID, "txtSenha")))
    campo_da_senha.send_keys(senha)

    campo_do_usuario.send_keys(Keys.ENTER)


def aguardar(locator, tempo=30):
    esperar_clique = WebDriverWait(navegador, tempo)
    fim = time.time() + tempo
    
    while time.time() < fim:
        try:
            time.sleep(3)
            elemento = esperar_clique.until(EC.element_to_be_clickable(locator))
            elemento.click()
            return True
        except ElementClickInterceptedException:
            time.sleep(1)
        except Exception as e:
            print(f"Erro ao clicar: {e}")
            break
    return False

def buscar_nota(nota):
    pesquisar_nota = wait.until(EC.element_to_be_clickable((By.ID, "txtNotaPesq")))
    pesquisar_nota.clear()
    pesquisar_nota.send_keys(nota)
    aguardar((By.ID, "btnPesqSolInvest"))


def verificar_elemento_invisivel(navegador, iD):
    time.sleep(20)
    try:
        elemento = navegador.find_element(By.ID, iD)
        if not elemento.is_displayed():
            print("Elemento está no DOM, mas invisível.")
            return "indisponivel"
        else:
            print("Elemento está visível.")
            return "disponivel"
    except NoSuchElementException:
        print("Elemento nem sequer existe no DOM.")
        return "erro"


servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico)

site = "http://10.1.1.80:8083/#/login"
pc = getpass.getuser()
arquivo = f'C:\\Users\\{pc}\\Dropbox\\PYTHON\\BOT TELEGRAM\\texto.txt'
nota_status = [ ]
usuario = "T56827"
senha = "5c!gt6EuVnnGgB8"

wait = WebDriverWait(navegador, 20)

navegador.get(site)
navegador.maximize_window()

login(usuario, senha)

engenharia = aguardar((By.XPATH, '//*[@id="sidebar"]/ul/li[1]/a'))

gestao_investimento = aguardar((By.XPATH, '//*[@id="sidebar"]/ul/li[1]/ul/li/a/span'))

gestao_solicitacao = aguardar((By.XPATH, '//*[@id="sidebar"]/ul/li[1]/ul/li/ul/li/a'))

T_inicial = time.localtime()
t_i = time.time()


with open(arquivo, 'r', encoding='utf-8') as f:
    linhas = f.readlines()
     
    for nota in linhas:
        try:
            buscar_nota(nota.strip())

            status = wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="000{nota.strip()}"]/td[4]')))

            if status.text == "Material Liberado":
                engrenagem = aguardar((By.XPATH, f'//*[@id="000{nota.strip()}"]/td[8]/div/div'))
                xpath_fluxo = f'//*[@id="000{nota.strip()}"]//li[@tooltip="Clique Para Ir ao Fluxo de Aprovações"]/a'
                try:
                    botao_fluxo = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_fluxo)))
                    navegador.execute_script("arguments[0].click();", botao_fluxo)
                    
                except Exception as e:
                    print(f"Erro ao tentar clicar no fluxo: {e}")
                    botao_fluxo.click()

                teste_aeo = verificar_elemento_invisivel(navegador, "btnAssinarAEO")
                if teste_aeo == "disponivel":
                    assinar = aguardar((By.ID, 'btnAssinarAEO'))
                    xpath_string = "//button[@id='btnAssinarAEO' and contains(text(), 'Assinar AEO')]"
                    confirmar = aguardar((By.XPATH, xpath_string))
                    confirmar_f = aguardar((By.XPATH, '/html/body/div[3]/div[2]/button[2]'))
                    xpath_string_ok = "//button[contains(text(), 'OK')]"
                    botao_ok = aguardar((By.XPATH, xpath_string_ok))
                    nota_status.append(f"{nota.strip()} - ASSINADO !")

                elif teste_aeo == "indisponivel":
                    print("Já assinada !")
                    nota_status.append(f"{nota.strip()} - Já assinada !")
                    navegador.execute_script("window.scrollTo(0, 0);")
                    lista = aguardar((By.ID,'tabPesquisar'))

                else:
                    print("erro")
                    nota_status.append(f"{nota.strip()} - erro ao assinar !")
                    navegador.execute_script("window.scrollTo(0, 0);")
                    lista = aguardar((By.ID,'tabPesquisar'))
        
            else:
                print("Status diferente de Material Liberado")
                nota_status.append(f"{nota.strip()} - {status.text}")
        except Exception as e:
            print(f"erro: {e}")
            print(nota_status)
            lista = aguardar((By.ID,'tabPesquisar'))
        
for i in nota_status:
    print(i)

print(f"feito - {len(nota_status)}")

T_final = time.localtime()
t_f = time.time()
t_t = t_f - t_i
with open("arquivo.txt", "w", encoding="utf-8") as arquivo:
    for i in nota_status:
        arquivo.write(f"{i}\n")
    arquivo.write(f"feito - {len(nota_status)}\n")
    arquivo.write(f"Hora inicial = {time.strftime('%H:%M:%S',T_inicial)}\n")
    arquivo.write(f"Hora Final = {time.strftime('%H:%M:%S',T_final)}\n")
    arquivo.write(f"Tempo Decorrido = {t_t // (60 * 60):.0f}:{t_t/60:.0f}:{t_t % 60:.0f}")