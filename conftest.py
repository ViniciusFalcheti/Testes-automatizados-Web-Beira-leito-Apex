import pytest
from utils.init_driver import init_driver
from utils.db_conn import connect_bd, criar_prescricao_usando_procedure

@pytest.fixture(scope="session")
def driver():
    connection = connect_bd()
    driver, wait = init_driver()
    # prescricao = criar_prescricao_usando_procedure(connection)
    prescricao = None
    yield driver, wait, connection, prescricao
    driver.quit()
    connection.close()