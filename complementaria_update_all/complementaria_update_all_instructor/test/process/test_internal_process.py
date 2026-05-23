import pytest
from unittest.mock import MagicMock, patch
from bd.exception.timeout_exception import TimeoutException
from process.internal_process import InternalProcess  
from datetime import datetime, timedelta

@pytest.fixture
def mock_connections():
    oc_connection = MagicMock()
    pg_connection = MagicMock()
    return oc_connection, pg_connection


@pytest.fixture
def internal_process(mock_connections):
    oc_connection, pg_connection = mock_connections
    return InternalProcess(oc_connection, pg_connection)


def test_execute_success(internal_process, mock_connections):
    """Prueba que execute procese fichas correctamente."""

    oc_connection, pg_connection = mock_connections

    internal_process._get_fichas_complementaria = MagicMock(return_value=[(1,), (2,)])

    with patch('process.internal_process.InsertIntoHistories') as mock_insert:
        internal_process.execute(2, 'all')

        internal_process._get_fichas_complementaria.assert_called_once_with(2)

        mock_insert.assert_not_called()


def test_execute_no_fichas(internal_process, mock_connections):
    """Prueba que execute maneje el caso sin fichas."""
    oc_connection, pg_connection = mock_connections

    internal_process._get_fichas_complementaria = MagicMock(return_value=[])

    internal_process.execute(2, 'all')

    internal_process._get_fichas_complementaria.assert_called_once_with(2)


def test_execute_exception(internal_process, mock_connections):
    """Prueba que execute maneje excepciones durante la ejecución."""

    oc_connection, pg_connection = mock_connections

    internal_process._get_fichas_complementaria = MagicMock(side_effect=Exception("Error de conexión"))

    with patch('process.internal_process.InsertIntoHistories.insert') as mock_insert:
        internal_process.execute(2, 'all')

        internal_process._get_fichas_complementaria.assert_called_once_with(2)

        mock_insert.assert_called_once_with(
            ("No se encontraron Fichas para procesar en la tabla INDICE_CAMBIO ", "sin datos", "sin datos")
        )

def test_get_fichas_complementaria(mock_connections):
    """Prueba que _get_fichas_complementaria devuelva los resultados correctos."""

    oc_connection, pg_connection = mock_connections
    internal_process = InternalProcess(oc_connection, pg_connection)

    mock_querys_db = MagicMock()
    mock_querys_db.select_pg.return_value = [(1,), (2,), (3,)]  

    with patch('process.internal_process.QuerysDB', return_value=mock_querys_db):
        entity = 2
        results = internal_process._get_fichas_complementaria(entity)

        mock_querys_db.select_pg.assert_called_once_with(
            internal_process._query_fichas(entity), None, False
        )

        assert results == [(1,), (2,), (3,)]
        
def test_query_fichas_with_entity_2(internal_process):
    """Prueba que _query_fichas genere la consulta correcta para entity 2 sin condiciones adicionales."""
    internal_process.type_search = "all"
    entity = 2

    query = internal_process._query_fichas(entity)

    assert "FIC_ESTADO" not in query 
    assert "FIC_FCH_INICIALIZACION" not in query 

def test_query_fichas_with_entity_other(internal_process):
    """Prueba que _query_fichas genere la consulta correcta para entidades distintas de 2."""
    internal_process.type_search = "all"
    entity = 4

    query = internal_process._query_fichas(entity)

    assert "FIC_ESTADO" in query 
    assert "FIC_FCH_INICIALIZACION" not in query  

def test_query_fichas_with_date_condition(internal_process):
    """Prueba que _query_fichas genere la consulta correcta con condiciones de fecha."""
    internal_process.type_search = "month"  
    entity = 2

    query = internal_process._query_fichas(entity)

    assert "FIC_FCH_INICIALIZACION" in query  
    assert "FIC_ESTADO" not in query  


def test_get_date_of_initialization_month(internal_process):
    """Prueba que _get_date_of_initialization devuelva la fecha correcta para búsqueda por mes."""
    internal_process.type_search = "month"
    
    expected_date = (datetime.now().date() - timedelta(days=30)).strftime("%Y-%m-%d")
    
    date_result = internal_process._get_date_of_initialization()

    assert date_result == expected_date

def test_get_date_of_initialization_year(internal_process):
    """Prueba que _get_date_of_initialization devuelva la fecha correcta para búsqueda por año."""
    internal_process.type_search = "year"

    expected_date = datetime(datetime.now().year, 1, 1).date().strftime("%Y-%m-%d")

    date_result = internal_process._get_date_of_initialization()

    assert date_result == expected_date