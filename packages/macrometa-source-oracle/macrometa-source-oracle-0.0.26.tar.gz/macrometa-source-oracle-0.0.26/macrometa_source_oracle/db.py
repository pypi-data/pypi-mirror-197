import singer
import uuid
from pathlib import Path
from singer import metadata, utils
from typing import Dict
import macrometa_source_oracle.sync_strategies.common as common
import oracledb

LOGGER = singer.get_logger()

def fully_qualified_column_name(schema, table, column):
    return '"{}"."{}"."{}"'.format(schema, table, column)

def make_dsn(config):
    dsn = "tcp://" + config["host"] + ":" + str(config["port"]) + "/" + config["service_name"]
    if config.get('ewallet_pem'):
        dsn = dsn.replace("tcp", "tcps", 1)
        dsn = dsn + "?wallet_location=" + config.get('ewallet_pem')

    return dsn

def create_ssl_string(ssl_string: str) -> str:
    tls_certificate_key_list = []
    split_string = ssl_string.split("-----")
    if len(split_string) < 4:
        raise Exception("Invalid PEM format for certificate.")
    for i in range(len(split_string)):
        if((i % 2) == 1):
            tls_certificate_key_list.append("-----")
            tls_certificate_key_list.append(split_string[i])
            tls_certificate_key_list.append("-----")
        else:
            tls_certificate_key_list.append(split_string[i].replace(' ', '\n'))
    
    tls_certificate_key_file = ''.join(tls_certificate_key_list)
    return tls_certificate_key_file

def create_wallet_file(config: Dict) -> Dict:
    path_uuid = uuid.uuid4().hex
    path = None
    try:
        if config.get('ewallet_pem'):
            path = f"/opt/oracle/config/{path_uuid}/ewallet.pem"
            cwallet = Path(path)
            cwallet.parent.mkdir(exist_ok=True, parents=True)
            cwallet.write_text(create_ssl_string(config['ewallet_pem']))
            config['ewallet_pem'] = f"/opt/oracle/config/{path_uuid}"
            LOGGER.info(f"ewallet.pem file created at: {path}")
    except Exception as e:
        LOGGER.warn(f"Failed to create ewallet.pem file at: {path}. {e}")
    return config

def delete_wallet_file(config: Dict) -> None:
    path = None
    try:
        if config.get('ewallet_pem'):
            path = config['ewallet_pem'] + "/ewallet.pem"
            cwallet = Path(path)
            config['ewallet_pem'] = cwallet.read_text()
            cwallet.unlink()
            LOGGER.info(f"ewallet.pem file deleted from: {path}")
            cwallet.parent.rmdir()
    except Exception as e:
        LOGGER.warn(f"Failed to delete ewallet.pem at: {path}. {e}")

def open_connection(config):
    LOGGER.info("dsn: %s", make_dsn(config))
    wallet_password = None
    wallet_location = None
    if config.get('ewallet_pem'):
        wallet_location = config["ewallet_pem"]
        if config.get('wallet_password'):
            wallet_password = config["wallet_password"]
    conn = oracledb.connect(user=config["user"], password=config["password"], dsn=make_dsn(config), wallet_location=wallet_location, wallet_password=wallet_password)
    return conn

def fetch_samples(conn_config: dict, stream):
    md_map = metadata.to_map(stream.metadata)
    conn_config['dbname'] = md_map.get(()).get('database-name')
    desired_columns = [c for c in stream.schema.properties.keys() if common.should_sync_column(md_map, c)]
    desired_columns.sort()

    if len(desired_columns) == 0:
        LOGGER.warning('There are no columns selected for stream %s, skipping it', stream.tap_stream_id)
        return []

    if md_map.get((), {}).get('is-view'):
        state = fetch_view(conn_config, stream, desired_columns)
    else:
        state = fetch_table(conn_config, stream, desired_columns)
    return state


def fetch_table(conn_config, stream, desired_columns):
    samples = []
    with open_connection(conn_config) as connection:
        connection.outputtypehandler = common.OutputTypeHandler
        with connection.cursor() as cur:
            cur.execute("ALTER SESSION SET TIME_ZONE = '00:00'")
            if conn_config['multitenant']:
                cur.execute(f"ALTER SESSION SET CONTAINER = {conn_config['pdb_name']}") #Switch to expected PDB
            cur.execute("""ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD"T"HH24:MI:SS."00+00:00"'""")
            cur.execute("""ALTER SESSION SET NLS_TIMESTAMP_FORMAT='YYYY-MM-DD"T"HH24:MI:SSXFF"+00:00"'""")
            cur.execute("""ALTER SESSION SET NLS_TIMESTAMP_TZ_FORMAT  = 'YYYY-MM-DD"T"HH24:MI:SS.FFTZH:TZM'""")
            time_extracted = utils.now()

            md = metadata.to_map(stream.metadata)
            schema_name = md.get(()).get('schema-name')
            escaped_columns = map(lambda c: common.prepare_columns_sql(stream, c), desired_columns)
            escaped_schema  = schema_name
            escaped_table   = stream.table
            select_sql      = """SELECT {} FROM {}.{}
                            ORDER BY ORA_ROWSCN ASC
                            FETCH FIRST 5 ROWS ONLY""".format(','.join(escaped_columns), escaped_schema, escaped_table)

            LOGGER.info("select %s", select_sql)
            for row in cur.execute(select_sql):
                record_message = common.row_to_singer_message(stream, row, None, desired_columns, time_extracted)
                samples.append(record_message.record)
    return samples


def fetch_view(conn_config, stream, desired_columns):
    samples = []
    with open_connection(conn_config) as connection:
        connection.outputtypehandler = common.OutputTypeHandler
        with connection.cursor() as cur:
            cur.execute("ALTER SESSION SET TIME_ZONE = '00:00'")
            if conn_config['multitenant']:
                cur.execute(f"ALTER SESSION SET CONTAINER = {conn_config['pdb_name']}") #Switch to expected PDB
            cur.execute("""ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD"T"HH24:MI:SS."00+00:00"'""")
            cur.execute("""ALTER SESSION SET NLS_TIMESTAMP_FORMAT='YYYY-MM-DD"T"HH24:MI:SSXFF"+00:00"'""")
            cur.execute("""ALTER SESSION SET NLS_TIMESTAMP_TZ_FORMAT  = 'YYYY-MM-DD"T"HH24:MI:SS.FFTZH:TZM'""")
            time_extracted = utils.now()

            md = metadata.to_map(stream.metadata)
            schema_name = md.get(()).get('schema-name')
            escaped_columns = map(lambda c: common.prepare_columns_sql(stream, c), desired_columns)
            escaped_schema  = schema_name
            escaped_table   = stream.table
            select_sql      = 'SELECT {} FROM {}.{}'.format(','.join(escaped_columns), escaped_schema, escaped_table)

            LOGGER.info("select %s", select_sql)
            for row in cur.execute(select_sql):
                record_message = common.row_to_singer_message(stream, row, None, desired_columns, time_extracted)
                samples.append(record_message.record)
    return samples
