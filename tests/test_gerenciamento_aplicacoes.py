import pytest
from pages.gerenciamento_aplicacoes_page import GerenciamentoAplicacoesPage
from utils.tipo_item import TipoItem

# Teste 1 - Administração de Item
@pytest.mark.parametrize("paciente, tipoItem", [
    ("0269690H", TipoItem.MED),
    ("0269690H", TipoItem.MEDCONTINUO),
    ("0269690H", TipoItem.SORO),
    ("0269690H", TipoItem.HEMO),
    ("0269690H", TipoItem.NUTRICAO),
    ("0269690H", TipoItem.CUIDADOS),
])
# @pytest.mark.skip(reason="Teste")
def test_administracao_item(driver, paciente, tipoItem):
    driver, wait, connection, prescricao = driver
    page = GerenciamentoAplicacoesPage(driver, wait, connection, prescricao)
    page.acessar()
    page.digita_paciente(paciente)
    page.seleciona_aba_item(tipoItem)
    page.administra_item(tipoItem)

# Teste 2 - Editar observação da Administração do Material
@pytest.mark.parametrize("paciente, tipoItem", [
    ("0269690H", TipoItem.MED),
    ("0269690H", TipoItem.MEDCONTINUO),
    ("0269690H", TipoItem.SORO),
    ("0269690H", TipoItem.HEMO),
    ("0269690H", TipoItem.NUTRICAO),
])
# @pytest.mark.skip(reason="Teste")
def test_alterar_observacao_adm(driver, paciente, tipoItem):
    driver, wait, connection, prescricao = driver
    page = GerenciamentoAplicacoesPage(driver, wait, connection, prescricao)
    page.acessar()
    page.digita_paciente(paciente)
    page.seleciona_aba_item(tipoItem)
    page.alterar_observacao_adm(tipoItem)

# Teste 3 - Remover dados da aplicação do Material
@pytest.mark.parametrize("paciente, tipoItem", [
    ("0269690H", TipoItem.MED),
    ("0269690H", TipoItem.MEDCONTINUO),
    ("0269690H", TipoItem.SORO),
    ("0269690H", TipoItem.HEMO),
    ("0269690H", TipoItem.NUTRICAO),
    ("0269690H", TipoItem.CUIDADOS),
])
# @pytest.mark.skip(reason="Teste")
def test_remocao_administracao_item(driver, paciente, tipoItem):
    driver, wait, connection, prescricao = driver
    page = GerenciamentoAplicacoesPage(driver, wait, connection, prescricao)
    page.acessar()
    page.digita_paciente(paciente)
    page.seleciona_aba_item(tipoItem)
    page.remove_adm_item(tipoItem)

# Teste 4 - Marcar item como não adm
@pytest.mark.parametrize("paciente, tipoItem", [
    ("0269690H", TipoItem.MED),
    # ("0269690H", TipoItem.MEDCONTINUO),
    ("0269690H", TipoItem.SORO),
    ("0269690H", TipoItem.HEMO),
    ("0269690H", TipoItem.NUTRICAO),
    ("0269690H", TipoItem.CUIDADOS),
])
# @pytest.mark.skip(reason="Teste")
def test_nao_administracao_item(driver, paciente, tipoItem):
    driver, wait, connection, prescricao = driver
    page = GerenciamentoAplicacoesPage(driver, wait, connection, prescricao)
    page.acessar()
    page.digita_paciente(paciente)
    page.seleciona_aba_item(tipoItem)
    page.marcar_item_como_nao_adm(tipoItem)

# Teste 5 - Remover Marcação não adm
@pytest.mark.parametrize("paciente, tipoItem", [
    ("0269690H", TipoItem.MED),
    # ("0269690H", TipoItem.MEDCONTINUO),
    ("0269690H", TipoItem.SORO),
    ("0269690H", TipoItem.HEMO),
    ("0269690H", TipoItem.NUTRICAO),
    ("0269690H", TipoItem.CUIDADOS),
])
# @pytest.mark.skip(reason="Teste")
def test_remover_nao_adm_item(driver, paciente, tipoItem):
    driver, wait, connection, prescricao = driver
    page = GerenciamentoAplicacoesPage(driver, wait, connection, prescricao)
    page.acessar()
    page.digita_paciente(paciente)
    page.seleciona_aba_item(tipoItem)
    page.remover_marcacao_nao_adm(tipoItem)

# Teste 6 - Suspender em lote
@pytest.mark.parametrize("paciente", [
    ("0269690H"),
])
# @pytest.mark.skip(reason="Teste")
def test_suspender_em_lote(driver, paciente):
    driver, wait, connection, prescricao = driver
    page = GerenciamentoAplicacoesPage(driver, wait, connection, prescricao)
    page.acessar()
    page.digita_paciente(paciente)
    page.suspender_em_lote()