import pytest
from unittest.mock import MagicMock, patch
from services.migrate_temporal import MigrateTemporal
import sql.queries as queries


@pytest.fixture
def mock_connections():
    """Simula las conexiones a Oracle y PostgreSQL."""
    oc_connection = MagicMock()
    pg_connection = MagicMock()
    return oc_connection, pg_connection


@pytest.fixture
def mock_rga():
    """Simula un registro académico (rga)."""
    return [None, None, '12345', None, None, None, 'FIC123', None, None, None, '4']


@pytest.fixture
def migrate_instance(mock_connections, mock_rga):
    """Crea una instancia de MigrateTemporal para las pruebas."""
    oc_connection, pg_connection = mock_connections
    return MigrateTemporal(oc_connection, pg_connection, mock_rga)


def test_migrate_person_active_state(migrate_instance):
    """Prueba la migración de una persona con un estado activo."""
    with patch.object(migrate_instance, '_create_registro_academico') as mock_create_registro_academico, \
         patch.object(migrate_instance, '_migrate_person') as mock_migrate_person, \
         patch.object(migrate_instance, '_migrate_usuario_lms') as mock_migrate_usuario_lms, \
         patch.object(migrate_instance, '_migrate_usuario_lms_enroll_c') as mock_migrate_usuario_lms_enroll_c:

        migrate_instance.migrate()

        mock_create_registro_academico.assert_called_once()
        mock_migrate_person.assert_called_once()
        mock_migrate_usuario_lms.assert_called_once()
        mock_migrate_usuario_lms_enroll_c.assert_called_once()


def test_migrate_person_inactive_state(migrate_instance, mock_rga):
    """Prueba que no se migra una persona si su estado no es activo."""
    # Cambia el estado a uno inactivo
    mock_rga[10] = '2'
    migrate_instance.rga = mock_rga

    with patch.object(migrate_instance, '_create_registro_academico') as mock_create_registro_academico, \
         patch.object(migrate_instance, '_migrate_person') as mock_migrate_person, \
         patch.object(migrate_instance, '_migrate_usuario_lms') as mock_migrate_usuario_lms, \
         patch.object(migrate_instance, '_migrate_usuario_lms_enroll_c') as mock_migrate_usuario_lms_enroll_c:

        migrate_instance.migrate()

        mock_create_registro_academico.assert_not_called()
        mock_migrate_person.assert_not_called()
        mock_migrate_usuario_lms.assert_not_called()
        mock_migrate_usuario_lms_enroll_c.assert_not_called()


def test_create_registro_academico(migrate_instance):
    """Prueba la creación del registro académico."""
    with patch('bd.db.queries.insert_registro_academico', return_value='INSERT INTO...') as mock_query, \
         patch.object(migrate_instance, '_create_record') as mock_create_record:

        migrate_instance._create_registro_academico()

        mock_create_record.assert_called_once_with(mock_query(), migrate_instance.rga)


def test_migrate_person(migrate_instance):
    """Prueba la migración de una persona."""
    person_mock = MagicMock()

    with patch.object(migrate_instance, '_get_record_by_id_pg', return_value=person_mock) as mock_get_record, \
         patch.object(migrate_instance, '_verify_or_create_record') as mock_verify_record, \
         patch.object(migrate_instance, '_update_column') as mock_update_column:

        migrate_instance._migrate_person()

        mock_get_record.assert_called_once_with(queries.query_person_temporal(), migrate_instance.nis)
        mock_verify_record.assert_called_once_with(
            queries.query_persona_post(),
            queries.insert_persona_from_temporal(),
            migrate_instance.nis,
            person_mock
        )
        mock_update_column.assert_called_once_with(
            migrate_instance.TABLE_PERSON,
            {'FLAG': 1},
            migrate_instance.NAME_ID,
            migrate_instance.nis,
            migrate_instance.SCHEMA_TEMPORAL
        )
        
def test_setup_new_rga_state(migrate_instance):
    """Prueba que _setup_new_rga_state modifique correctamente el estado."""
    user_lms_enroll = ['id_usuario', 'curso', 'otro_dato', 4]

    result = migrate_instance._setup_new_rga_state(user_lms_enroll)

    assert isinstance(result, tuple)
    
def test_migrate_usuario_lms_create_record(migrate_instance):
    """Prueba que _migrate_usuario_lms cree un registro si el usuario LMS existe."""

    migrate_instance._get_record_by_id_pg = MagicMock(return_value={'id': 1, 'nombre': 'Usuario'})

    migrate_instance._migrate_usuario_lms()

    migrate_instance._get_record_by_id_pg.assert_called_once_with(
            queries.query_usuario_lms_temporal(), '12345'  
        )

       
