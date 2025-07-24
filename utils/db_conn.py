import oracledb
import os
from dotenv import load_dotenv

def connect_bd():
    try:
        load_dotenv()

        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")
        db_service = os.getenv("DB_SERVICE")

        # oracledb.init_oracle_client(lib_dir=r"C:\oracle\instantclient_23_7")
        lib_dir = os.getenv("ORACLE_CLIENT_DIR", "./instantclient_19_15")
        oracledb.init_oracle_client(lib_dir=lib_dir)

        dsn = oracledb.makedsn(db_host, 1521, service_name=db_service)

        connection = oracledb.connect(
            user=db_user,
            password=db_password,
            dsn=dsn
        )

        print("Successfully connected to Oracle Database")

        # testSelect(connection)
        # criar_prescricao_usando_procedure(connection)

        return connection
    except:
        print("Error connecting to Oracle Database")
        connection = None
         
def test_select(connection):
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM PACIENTE P WHERE P.COD_PACIENTE = '0269690H'")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        cursor.close()
        connection.close()
                 
def criar_prescricao_usando_procedure(connection):
    if connection:
        cursor = connection.cursor()

        # Cria variáveis de saída
        cod_erro = cursor.var(str)
        msg_erro = cursor.var(str)
        num_prescricoes = cursor.var(str)

        # Chama a procedure com parâmetros de entrada e saída
        cursor.callproc("PROC_GERA_PRESC_COD_VERMELHO", [
            13,             # p_SEQ_TRANSF_MACICA -- Modelo criado de teste - 13
            'CACJ01011',    # p_COD_CENCUSTO
            '0269690H',     # p_COD_PACIENTE
            1,              # p_COD_PROFISSIONAL
            '0320',         # p_NUM_QUARTO
            1,              # p_NUM_LEITO
            78000,          # p_NUM_PESO
            None,           # p_NUM_ALTURA
            None,           # p_NUM_PA_MIN
            None,           # p_NUM_PA_MAX
            None,           # p_NUM_PULSO
            None,           # p_NUM_TEMPERATURA
            cod_erro,       # PN_COD_ERRO
            msg_erro,       # PC_MSG_ERRO
            num_prescricoes # P_NUM_PRESCRICOES
        ])
        
        # print("codErro:", cod_erro.getvalue())
        # print("Msg:", msg_erro.getvalue())
        # print("Prescricoes:", num_prescricoes.getvalue())
        # connection.close()

        if cod_erro.getvalue() == '0':
            connection.commit()
        else:
            connection.rollback()
            print("codErro:", cod_erro.getvalue())

        return num_prescricoes.getvalue()