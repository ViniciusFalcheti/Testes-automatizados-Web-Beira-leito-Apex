from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
from utils.tipo_item import TipoItem

class GerenciamentoAplicacoesPage:
    def __init__(self, driver, wait, connection, prescricao):
        self.driver = driver
        self.wait = wait
        self.connection = connection
        self.prescricao = prescricao


    # Funções iniciais
    def acessar(self):
        self.driver.get("https://apexdsv.hcrp.usp.br/apex/r/hc/gerenciamento-sati/home")

    def digita_paciente(self, cod_paciente_teste):
        # Clica para selecionar paciente
            registro_paciente = self.driver.find_element(By.ID, "P1_REGISTRO")
            registro_paciente.clear()  # Limpa o campo antes de digitar
            time.sleep(0.5)
            registro_paciente.send_keys(cod_paciente_teste)

            time.sleep(0.5)

            registro_paciente.send_keys(Keys.ENTER)

    def seleciona_aba_item(self, tipoItem: TipoItem):
        try:
            time.sleep(1)
            if tipoItem == TipoItem.MEDCONTINUO:
                tipoItem = TipoItem.MED  # Força o tipo de item para MEDCONTINUO
            self.driver.find_element(By.XPATH, f'//*[@id="SR_tab_{tipoItem.value}_tab"]/a').click()
        except Exception:
            raise ValueError("Tipo de item inválido!")
        
    def pega_id_grid_item(self, tipoItem: TipoItem):
        if tipoItem == "med" or tipoItem == "medContinuo":
            id_grid = "462998989098843343_orig"
        elif tipoItem == "soro":
            id_grid = "493991208242716213_orig"
        elif tipoItem == "hemo":
            id_grid = "494032035403860217_orig"
        elif tipoItem == "coleta":
            id_grid = "461474180923560632_orig"
        elif tipoItem == "nutricao":
            id_grid = "494132567709140308_orig"
        elif tipoItem == "terapia":
            id_grid = "494395274901033316_orig"
        elif tipoItem == "cuidados":
            id_grid = "441606800746207135_orig"
        elif tipoItem == "enfermagem":
            id_grid = "444061483845133805_orig"

        return id_grid

    # Funções de apoio
    def verificar_celula(self, idGrid, linha, ehContinuo = False, acao = "administrar"):
        try:
            time.sleep(1.5)


            # Localiza a célula pelo XPath
            xpath_base = f'//*[@id="{idGrid}"]//table//tbody/tr[{linha+1}]/td[2]'
            print(f"Verificando célula: {xpath_base}")

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath_base))
            )
            celula = self.driver.find_element(By.XPATH, xpath_base)
            filhos = celula.find_elements(By.XPATH, "./*")

            if acao == "administrar" or acao == "marcarComoNaoAdm":             
                if not filhos:
                    print("Célula sem filhos → True")
                    return True  # Célula completamente vazia (sem filhos)

                if len(filhos) == 1:
                    filho = filhos[0]
                    # tag = filho.tag_name
                    classe = filho.get_attribute("class") or ""

                    # if (tag == "span" and "fa-hourglass-2" in classe) or (tag == "span" and "fa-check-circle" in classe and ehContinuo):
                    if ("fa-hourglass-2" in classe) or ("fa-check-circle" in classe and ehContinuo):
                        print("Célula com apenas um span.fa-hourglass-2 → True")
                        return True

                print("Célula com conteúdo diferente → False")
                return False
            elif acao == "removerAdm" or acao == "alteraObsAdm":                
                if not filhos:
                    print("Célula sem filhos → False")
                    return False
                
                if len(filhos) == 1:
                    filho = filhos[0]
                    classe = filho.get_attribute("class") or ""

                    if "fa-check-circle" in classe:
                        print("Célula com apenas um span.fa-check-circle → True")
                        return True

                print("Célula com conteúdo diferente → False")
                return False
            elif acao == "removerNaoAdm":
                if not filhos:
                    print("Célula sem filhos → False")
                    return False
                
                if len(filhos) == 1:
                    filho = filhos[0]
                    classe = filho.get_attribute("class") or ""

                    if "fa-exclamation-circle" in classe:
                        print("Célula com apenas um span.fa-exclamation-circle → True")
                        return True

                print("Célula com conteúdo diferente → False")
                return False

        except NoSuchElementException:
            print("Célula não encontrada → False")
            return False

    def is_number(self, variable):
        """Verifica se uma string pode ser convertida para um número."""
        try:
            float(variable)
            return True
        except ValueError:
            return False
    
    # Funções de ações
    def administra_item(self, tipoItem: TipoItem):
        try:
            tipoItem = tipoItem.value
            print("Etapa: Convertido tipoItem")

            # idGrid = self.pega_id_grid_item(tipoItem)
            idGrid = "report_med" if tipoItem == "medContinuo" else f"report_{tipoItem}"
            print("Etapa: ID da grid:", idGrid)

            # Aguarde até que o elemento esteja clicável
            tbody_xpath = f'//*[@id="{idGrid}"]//table//tbody'
            grid = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, tbody_xpath))
            )

            # Pega a quantidade de linhas na grid
            print(f"Pegando a qtd de linhas de {tipoItem}")
            qtd_linhas = int(grid.get_attribute("childElementCount")) - 1
            print(f"Quantidade de linhas na grid de {tipoItem}: {qtd_linhas}")

            # Rola até o grid
            # self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", grid)

            # tbody = self.driver.find_element(By.XPATH, f'//*[@id="{idGrid}"]/tbody')

            for i in range(1, qtd_linhas + 1):
                print(f"Verificando linha {i}")
                try:
                    if tipoItem in ["med", "medContinuo"]:
                        celula_tipo = self.driver.find_element(By.XPATH, f'//*[@id="{idGrid}"]//table//tbody/tr[{i+1}]/td[11]/a')
                        ehContinuo = celula_tipo.text == "CONTINUO"
                    else:
                        ehContinuo = False

                    if ehContinuo and tipoItem != "medContinuo":
                        print("Pulando linha contínua")
                        continue

                    result = self.verificar_celula(idGrid, i, tipoItem == "medContinuo")
                    print("Resultado da verificação da célula:", result)

                    if result:
                        print("Clicando no botão de administração")
                        xpath_botao = f'//*[@id="{idGrid}"]//table//tbody/tr[{i+1}]/td[1]/div/button'
                        
                        botao = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, xpath_botao))
                        )
                        # self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao)
                        time.sleep(0.5)
                        botao.click()
                        break
                    
                    if i == qtd_linhas:
                        raise Exception(f"Não foi encontrado nenhum item para administrar na grid de {tipoItem}.")

                except Exception as e:
                    print(f"Erro ao processar linha {i}: {e}")
                    raise

            # Continuando o processo
            if tipoItem == "medContinuo":
                tipoItem = "med"

            print("Esperando botão de ações")
            print(f"actions{tipoItem.capitalize()}_0i")
            
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, f"actions{tipoItem.capitalize()}_0i")))
            self.driver.find_element(By.ID, f"actions{tipoItem.capitalize()}_0i").click()
            time.sleep(0.5)

            if tipoItem == "med":
                try:
                    self.driver.find_element(By.CSS_SELECTOR, ".js-confirmBtn").click()
                    time.sleep(0.5)
                except NoSuchElementException:
                    print("Botão de confirmação não encontrado — ignorando")

            print("Verificando se o modal está na tela")
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="adm_modal"]')))

            time.sleep(1)

            print("Preenchendo campos do modal")
            motivo_adm = self.driver.find_element(By.ID, "P1_MOTIVO_ADM")
            motivo_adm.send_keys(f"Teste de administração de {tipoItem.capitalize()} Apex")

            obs_adm = self.driver.find_element(By.ID, "P1_OBS_ADM")
            obs_adm.send_keys("Teste")

            try:
                qtd_continuo = self.driver.find_element(By.ID, "P1_QTD_CONTINUO_ADM")
                qtd_continuo.send_keys("50")
            except Exception:
                print("Campo P1_QTD_CONTINUO_ADM não encontrado — ignorando")

            time.sleep(0.5)
            print("Clicando no botão administrar")
            self.driver.find_element(By.ID, "btn_administrar").click()

        except Exception as e:
            print("Erro geral em administra_item:", e)
            raise

    def alterar_observacao_adm(self, tipoItem: TipoItem):
        try:
            tipoItem = tipoItem.value
            print("Etapa: Convertido tipoItem")


            if tipoItem not in ["med", "medContinuo", "soro", "hemo", "nutricao", "terapia", "enfermagem"]:
                raise ValueError("Tipo de item inválido para alterar observação de administração!")

            # idGrid = self.pega_id_grid_item(tipoItem)
            idGrid = "report_med" if tipoItem == "medContinuo" else f"report_{tipoItem}"
            print("Etapa: Pegou idGrid")


            # Aguarde até que o elemento esteja clicável
            tbody_xpath = f'//*[@id="{idGrid}"]//table//tbody'
            print("Etapa: Aguardando elemento")
            grid = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, tbody_xpath))
            )

            # Pega a quantidade de linhas na grid
            print(f"Pegando a qtd de linhas de {tipoItem}")
            qtd_linhas = int(grid.get_attribute("childElementCount")) - 1
            print(f"Quantidade de linhas na grid de {tipoItem}: {qtd_linhas}")

            for i in range(1, qtd_linhas + 1):

                result = self.verificar_celula(idGrid, i, False, acao="alteraObsAdm")

                if result:
                    self.driver.find_element(By.XPATH, f'//*[@id="{idGrid}"]//table//tbody/tr[{i+1}]/td[1]/div/button').click()
                    # flag = False
                    break

                if i == qtd_linhas:
                    raise Exception(f"Não foi encontrado nenhum item já administradado para efetuar a alteração da observação na grid de {tipoItem}.")

            if tipoItem == "medContinuo":
                tipoItem = "med"

            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, f"actions{tipoItem.capitalize()}_1i")))
            self.driver.find_element(By.ID, f"actions{tipoItem.capitalize()}_1i").click()

            time.sleep(0.5)

            print("Verificando se o modal está na tela")
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="alterar_obs_adm_modal"]')))

            obs_atual = self.driver.find_element(By.ID, "P1_OBS_ADM_PARAM").get_attribute("value")
            print("obs atual: ", obs_atual)

            if obs_atual == None or obs_atual == "":
                obs_nova = f"Teste de alteração de obs administração de {tipoItem.capitalize()} Apex"
            elif obs_atual == f"Teste de alteração de obs administração de {tipoItem.capitalize()} Apex".upper():
                obs_nova = f"Teste de alteração de obs administração de {tipoItem.capitalize()} Apex 1"
            elif self.is_number(obs_atual[-1]):
                obs_nova = f"Teste de alteração de obs administração de {tipoItem.capitalize()} Apex {int(obs_atual[-1]) + 1}"
            else:
                obs_nova = f"Teste de alteração de obs administração de {tipoItem.capitalize()} Apex"

            obs_nova_input = self.driver.find_element(By.ID, "P1_OBS_ALTERACAO")
            obs_nova_input.send_keys(obs_nova)

            time.sleep(0.5)

            self.driver.find_element(By.ID, "btn_salvar_alteracao_obs").click()
        except Exception as e:
            print("Erro geral em alterar_observacao_adm:", e)
            raise    

    def remove_adm_item(self, tipoItem: TipoItem):
        try:
            print("Etapa: Convertido tipoItem")
            tipoItem = tipoItem.value

            # idGrid = self.pega_id_grid_item(tipoItem)
            idGrid = "report_med" if tipoItem == "medContinuo" else f"report_{tipoItem}"
            print("Etapa: ID da grid:", idGrid)

            # Aguarde até que o elemento esteja clicável
            tbody_xpath = f'//*[@id="{idGrid}"]//table//tbody'
            grid = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, tbody_xpath))
            )

            # Pega a quantidade de linhas na grid
            print(f"Pegando a qtd de linhas de {tipoItem}")
            qtd_linhas = int(grid.get_attribute("childElementCount")) - 1
            print(f"Quantidade de linhas na grid de {tipoItem}: {qtd_linhas}")

            # Rola até o grid
            # self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", grid)

            for i in range(1, qtd_linhas + 1):
                if tipoItem == "med" or tipoItem == "medContinuo":
                    ehContinuo = True if self.driver.find_element(By.XPATH, f'//*[@id="{idGrid}"]//table//tbody/tr[{i+1}]/td[11]/a').text == "CONTINUO" else False
                else:
                    ehContinuo = False

                if ehContinuo and (tipoItem != "medContinuo"):
                    continue

                result = self.verificar_celula(idGrid, i, False, acao="removerAdm")

                if result:
                    self.driver.find_element(By.XPATH, f'//*[@id="{idGrid}"]//table//tbody/tr[{i+1}]/td[1]/div/button').click()
                    # flag = False
                    break

                if i == qtd_linhas:
                    raise Exception(f"Não foi encontrado nenhum item já administradado para efetuar a remoção na grid de {tipoItem}.")

            # Pegando o número da ação de remover dependendo do tipo de item
            if tipoItem in ["med", "medContinuo", "soro", "hemo", "nutricao", "terapia", "enfermagem"]:
                numAcao = 2
            else:
                numAcao = 1

            # clicando na ação de remover adm no menu suspenso
            acao_id = f"actionsMed_{numAcao}i" if tipoItem == "medContinuo" else f"actions{tipoItem.capitalize()}_{numAcao}i"
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, acao_id)))
            self.driver.find_element(By.ID, acao_id).click()

            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="remover_adm_modal"]')))

            motivo_nao_adm = self.driver.find_element(By.ID, "P1_MOTIVO_REMOVEU_ADM")
            motivo_nao_adm.send_keys(f"Teste de remoção da administração de {tipoItem.capitalize()} Apex")

            if tipoItem in ["cuidados", "medContinuo"]:
                # Encontra todos os checkboxes com o name específico
                checkboxes = self.driver.find_elements(By.NAME, "f01")

                # Marca os que não estão marcados ainda
                for checkbox in checkboxes:
                    if not checkbox.is_selected():
                        checkbox.click()

            self.driver.find_element(By.ID, "btn_remover_adm").click()
        except Exception as e:
            print("Erro geral em remove_adm:", e)
            raise    

    def marcar_item_como_nao_adm(self, tipoItem: TipoItem):
        try:
            tipoItem = tipoItem.value
            # flag = True

            # idGrid = self.pega_id_grid_item(tipoItem)
            idGrid = "report_med" if tipoItem == "medContinuo" else f"report_{tipoItem}"
            print("Etapa: ID da grid:", idGrid)

            # Aguarde até que o elemento esteja clicável
            tbody_xpath = f'//*[@id="{idGrid}"]//table//tbody'
            grid = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, tbody_xpath))
            )

            # Pega a quantidade de linhas na grid
            print(f"Pegando a qtd de linhas de {tipoItem}")
            qtd_linhas = int(grid.get_attribute("childElementCount")) - 1
            print(f"Quantidade de linhas na grid de {tipoItem}: {qtd_linhas}")

            # Rola até o grid
            # self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", grid)

            for i in range(1, qtd_linhas+1):
                result = self.verificar_celula(idGrid, i, False, acao="marcarComoNaoAdm")

                if result:
                    print("Etapa: Clicando no botão de menu")
                    
                    self.driver.find_element(By.XPATH, f'//*[@id="{idGrid}"]//table//tbody/tr[{i+1}]/td[1]/div/button').click()
                    # flag = False
                    break

                if i == qtd_linhas:
                    raise Exception(f"Não foi encontrado nenhum item para ser marcado como não adm na grid de {tipoItem}.")

            if tipoItem == "medContinuo":
                tipoItem = "med"

            # Pegando o número da ação de não adm dependendo do tipo de item
            if tipoItem in ["coleta", "cuidados"]:
                numAcao = 2
            else:
                numAcao = 4


            print("Etapa: Selecionando a ação")
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, f"actions{tipoItem.capitalize()}_{numAcao}i")))
            self.driver.find_element(By.ID, f"actions{tipoItem.capitalize()}_{numAcao}i").click()

            print("Etapa: Esperando modal aparecer na tela")
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="nao_adm_modal"]')))

            motivo_nao_adm = self.driver.find_element(By.ID, "P1_MOTIVO_NAO_ADM")
            motivo_nao_adm.send_keys(f"Teste de não administração de {tipoItem.capitalize()} Apex")

            self.driver.find_element(By.ID, "btn_nao_administrar").click()
        except Exception as e:
            print("Erro geral em marcar_item_como_nao_adm:", e)
            raise

    def remover_marcacao_nao_adm(self, tipoItem: TipoItem):
        try:
            tipoItem = tipoItem.value

            # idGrid = self.pega_id_grid_item(tipoItem)
            idGrid = "report_med" if tipoItem == "medContinuo" else f"report_{tipoItem}"

            # Aguarde até que o elemento esteja clicável
            tbody_xpath = f'//*[@id="{idGrid}"]//table//tbody'
            grid = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, tbody_xpath))
            )

            # Pega a quantidade de linhas na grid
            print(f"Pegando a qtd de linhas de {tipoItem}")
            qtd_linhas = int(grid.get_attribute("childElementCount")) - 1
            print(f"Quantidade de linhas na grid de {tipoItem}: {qtd_linhas}")

            for i in range(1, qtd_linhas + 1):
                result = self.verificar_celula(idGrid, i, False, acao="removerNaoAdm")

                if result:
                    print("Etapa: Clicando no botão de menu")
                    
                    self.driver.find_element(By.XPATH, f'//*[@id="{idGrid}"]//table//tbody/tr[{i+1}]/td[1]/div/button').click()
                    # flag = False
                    break

                print(f"Linha: {i} - qtd_linhas: {qtd_linhas}")
                        
                if i == qtd_linhas:
                    raise Exception(f"Não foi encontrado nenhum item para ser marcado como não adm na grid de {tipoItem}.")

            if tipoItem == "medContinuo":
                tipoItem = "med"

            # Pegando o número da ação de não adm dependendo do tipo de item
            if tipoItem in ["coleta", "cuidados"]:
                numAcao = 3
            else:
                numAcao = 5

            print("Etapa: Selecionando a ação")
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, f"actions{tipoItem.capitalize()}_{numAcao}i")))
            self.driver.find_element(By.ID, f"actions{tipoItem.capitalize()}_{numAcao}i").click()

            print("Etapa: Esperando modal aparecer na tela")
            # WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="nao_adm_modal"]')))
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.confirm-remover-nao-adm')))
            
            print("Etapa: Clicando no botão de confirma remoção")
            time.sleep(1)
            self.driver.find_element(By.CSS_SELECTOR, ".js-confirmBtn").click()
                    
        except Exception as e:
            print("Erro geral em remover_marcacao_nao_adm:", e)
            raise

    def suspender_em_lote(self):
        try:
            time.sleep(1)
            self.driver.find_element(By.ID, f'btn_suspender_em_lotes').click()

            grid = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "report_supensao_med"))
            )

            # Encontra todos os checkboxes com name="meu_checkbox"
            checkboxes = self.driver.find_elements(By.NAME, "f01")

            # Marca apenas os dois primeiros
            for checkbox in checkboxes[:2]:
                if not checkbox.is_selected():
                    checkbox.click()

            time.sleep(1)

            print("Etapa: Colocando a justificativa")
            justificativa_suspensao = self.driver.find_element(By.ID, "P8_JUSTIFICATIVA")
            justificativa_suspensao.send_keys(f"Teste de suspensão de medicamento em lote Apex")
            
            print("Etapa: Clicando no botão de suspender")
            time.sleep(1)
            self.driver.find_element(By.ID, "btn_suspender").click()

            print("Etapa: Verificando se apareceu um alerta de sucesso")
            time.sleep(1)
            alerta = self.driver.find_element(By.CSS_SELECTOR, ".t-Alert-title").text

            if alerta != "Suspensão de medicamento realizada com sucesso!":
                raise Exception("Alerta de sucesso não esncontrado! Algo ocorreu errado")
                    
        except Exception as e:
            print("Erro geral em suspensao em lote:", e)
            raise    