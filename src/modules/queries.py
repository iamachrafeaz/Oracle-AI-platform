import os

# Dossier de sortie CSV/JSON
DATA_DIR = os.path.join(os.path.dirname(__file__), "../../data/oracle_raw")
os.makedirs(DATA_DIR, exist_ok=True)

# Fichier JSON simulant AUD$ si la table est vide
AUDIT_JSON_FILE = os.path.join(DATA_DIR, "synthetic_audits.json")

QUERIES = {
    "audit_logs": {
        "query": """
            SELECT NTIMESTAMP# AS event_timestamp, USERID, USERHOST, PRIV$USED, ACTION#, OBJ$NAME, SQLTEXT, COMMENT$TEXT, RETURNCODE
            FROM
                SYS.AUD$
            WHERE
                NTIMESTAMP# > SYSDATE - 30 -- last 30 days, adjust as needed
            ORDER BY
                NTIMESTAMP# DESC
        """,
    },
    "sql_plan": {"query": """
            SELECT sql_id, plan_hash_value, id, parent_id, operation, options, object_name
            FROM V$SQL_PLAN
        """
    },
    "users": {"query": "SELECT username, account_status, created FROM DBA_USERS"},
    "roles": {"query": "SELECT role, authentication_type FROM DBA_ROLES"},
    "privileges": {"query": "SELECT grantee, privilege FROM DBA_SYS_PRIVS"},
    "sqlstat": {"query": """
            SELECT sql_id, elapsed_time, cpu_time, buffer_gets, disk_reads
            FROM V$SQLSTATS
        """
    },
    "system_event": {"query": """
            SELECT event, total_waits, time_waited
            FROM V$SYSTEM_EVENT
        """
    },
    "users_roles" : {"query" : """
            SELECT u.username, u.account_status, u.default_tablespace, u.profile, r.granted_role, r.admin_option
            FROM dba_users u
            LEFT JOIN dba_role_privs r
            ON u.username = r.grantee
            ORDER BY u.username
        """
    },
    "system_privileges" : {"query" : """
            SELECT grantee, privilege, admin_option
            FROM dba_sys_privs
            ORDER BY grantee
        """
    },
    "password_profiles" : {"query" : """
            SELECT profile, resource_name AS limit_name, limit AS limit_value
            FROM dba_profiles
            WHERE resource_type = 'PASSWORD'
            ORDER BY profile
        """
    },
}


def get_queries(query_type: str) -> dict:
    """
    Retourne la définition d'une requête par son type
    """
    if query_type not in QUERIES:
        raise KeyError(
            f"Query '{query_type}' inconnue. "
            f"Disponibles: {list(QUERIES.keys())}"
        )
    return QUERIES[query_type]


