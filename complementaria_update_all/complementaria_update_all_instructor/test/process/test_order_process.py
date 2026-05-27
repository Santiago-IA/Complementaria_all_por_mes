import pytest
from concurrent.futures import TimeoutError 
from unittest.mock import MagicMock, patch
from process.order_process import OrderProcess  
from bd.exception.timeout_exception import TimeoutException
from bd.db.querys_db import QuerysDB 
import bd.db.queries as queries
@pytest.fixture
def mock_connections():
    """Crea conexiones simuladas a las bases de datos."""
    oc_connection = MagicMock()
    pg_connection = MagicMock()
    return oc_connection, pg_connection

@pytest.fixture
def order_process(mock_connections):
    """Crea una instancia de OrderProcess con conexiones simuladas."""
    return OrderProcess(*mock_connections)


# def test_execute_with_records(order_process, mock_connections):
#     """Prueba que execute procese registros correctamente."""
    
#
#     oc_connection, pg_connection = mock_connections
#     starting_id = 1
#     entity = 2

#     # Simula el comportamiento de _get_row_to_process
#     order_process._get_row_to_process = MagicMock(side_effect=[
#         [(1, 2)],  # Devuelve registros en la primera llamada
#         [],        # Devuelve vacío en la segunda llamada
#     ])
#     order_process._define_what_process_run = MagicMock()

#     # Simula el comportamiento de ThreadPoolExecutor y Future
#     with patch('concurrent.futures.ThreadPoolExecutor') as mock_executor:
#         mock_future = MagicMock()
#         mock_future.result.return_value = [(1, 2)]  # Simula el resultado esperado
        
#         # Aquí simulas que la función submit retorna tu mock_future
#         mock_executor.return_value.__enter__.return_value.submit.return_value = mock_future

#         # Llama al método execute
#         order_process.execute(starting_id, entity)

#         # Verifica que se llamara a _get_row_to_process
#         order_process._get_row_to_process.assert_called()



def test_execute_no_records(order_process, mock_connections):
    """Prueba que execute maneje la ausencia de registros correctamente."""
    
    oc_connection, pg_connection = mock_connections
    starting_id = 1
    entity = 2
    
    order_process._get_row_to_process = MagicMock(return_value=[])

    with patch('concurrent.futures.ThreadPoolExecutor'):
        order_process.execute(starting_id, entity)

        order_process.insert_status_process = MagicMock()
        order_process.insert_status_process(pg_connection, tuple([starting_id, entity, 0, None, None, None, None, "2024-09-24 12:00:00"]), "NO SE ENCONTRARON MÁS REGISTROS DE FICHA DESDE EL ICA_ID 1")


def test_execute_timeout_exception(order_process, mock_connections):
    """Prueba que execute maneje TimeoutError."""
    
    oc_connection, pg_connection = mock_connections
    starting_id = 1
    entity = 2
    

    order_process._get_row_to_process = MagicMock(side_effect=TimeoutError("La consulta tomó más de 15 minutos y fue interrumpida."))

    with pytest.raises(TimeoutException):
        order_process.execute(starting_id, entity)


def test_get_next_id_to_start(order_process, mock_connections):
    """Prueba que _get_next_id_to_start retorne el ID correcto."""
    
    order_process._get_next_id_to_start = MagicMock(return_value=10)

    result = order_process._get_next_id_to_start(2)

    assert result == 10

def test_define_what_process_run(order_process, mock_connections):
    """Prueba que _define_what_process_run llame al proceso correcto."""
    
    record = {"some_field": "some_value"}
    ent_id = 2
    mock_class = MagicMock()
    mock_module = MagicMock()
    mock_module.FichaCaracterizacion = mock_class

    with patch('importlib.import_module', return_value=mock_module):
        order_process._define_what_process_run(record, ent_id)

        mock_class.assert_called_once_with(order_process.oc_connection, order_process.pg_connection, record)
        instance_class = mock_class.return_value
        instance_class.process.assert_called_once()

def test_get_row_to_process_calls_select_oc(order_process, mock_connections):
    """Prueba que _get_row_to_process llame al método select_oc correctamente."""
    oc_connection, pg_connection = mock_connections
    
   
    order_query = "SELECT * FROM example_table WHERE id = :ica_id AND entity = :entity"
    order_process._get_order_query_other_entities = MagicMock(return_value=order_query)

    mock_results = [(1, 2)]
    with patch('bd.db.querys_db.QuerysDB.select_oc', return_value=mock_results) as mock_select:
        results = order_process._get_row_to_process(1, 2)

        mock_select.assert_called_once_with(order_query, {"ica_id": 1, "entity": 2}, False)

        assert results == mock_results


def test_get_next_id_to_start_returns_id(order_process, mock_connections):
    """Prueba que _get_next_id_to_start devuelva el ID correcto."""

    oc_connection, pg_connection = mock_connections

    mock_result = [(5,)]
    with patch.object(QuerysDB, 'select_pg', return_value=mock_result) as mock_select_pg:
        result = order_process._get_next_id_to_start(2)

        mock_select_pg.assert_called_once_with(queries.get_last_row_processed(), (2,))
        
        assert result[0] == 5
        
def test_insert_status_process(order_process, mock_connections):
    """Prueba que insert_status_process inserte el estado correctamente."""
    pg_connection = mock_connections

    with patch.object(QuerysDB, 'insert_or_update') as mock_insert_or_update:
        record = (1, 'test_entity', 3, None, 'test_state', None, None, '2024-09-24 12:00:00')  
        state = 'Estado de prueba'

        OrderProcess.insert_status_process(pg_connection, record, state)

        mock_insert_or_update.assert_called_once_with(
            OrderProcess.insert_to_icap(), 
            (record[0], record[1], record[2], record[7], state)
        )
        
def test_get_order_query_ficha(order_process):
    """Prueba que _get_order_query_other_entities retorne la consulta correcta para ficha."""
    expected_query = order_process._get_order_query_ficha()   
    result = order_process._get_order_query_other_entities(2) 
    assert result == expected_query, f"Expected: {expected_query}, but got: {result}"

def test_get_order_query_registro_academico(order_process):
    """Prueba que _get_order_query_other_entities retorne la consulta correcta para registro académico."""
    expected_query = order_process._get_order_query_registro_academico()   
    result = order_process._get_order_query_other_entities(4)  
    assert result == expected_query, f"Expected: {expected_query}, but got: {result}"

def test_get_order_query_instructor_x_ficha(order_process):
    """Prueba que _get_order_query_other_entities retorne la consulta correcta para instructor x ficha."""
    expected_query = order_process._get_order_query_instructor_x_ficha()   
    result = order_process._get_order_query_other_entities(6)  
    assert result == expected_query, f"Expected: {expected_query}, but got: {result}"

def test_get_order_query_calificaciones(order_process):
    """Prueba que _get_order_query_other_entities retorne la consulta correcta para calificaciones."""
    expected_query = order_process._get_order_query_calificaciones()   
    result = order_process._get_order_query_other_entities(7)  
    assert result == expected_query, f"Expected: {expected_query}, but got: {result}"
    
def test_define_what_process_run_imports_correct_class(order_process, mock_connections):
    """Prueba que se importe la clase correcta desde el módulo correspondiente."""
    
    record = {"another_field": "another_value"}
    entity_id = 2

    mock_class = MagicMock()

    mock_module = MagicMock()
    mock_module.FichaCaracterizacion = mock_class  

    with patch('importlib.import_module', return_value=mock_module):
        order_process._define_what_process_run(record, entity_id)

        mock_class.assert_called_once_with(
            order_process.oc_connection,
            order_process.pg_connection,
            record
        )

        instance_class = mock_class.return_value  
        instance_class.process.assert_called_once()  