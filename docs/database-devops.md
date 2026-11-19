# Database changes in CI/CD — DevOps reading lab (no execution)

**Scope:** Educational examples only. No database service, account, network connection, schema or SQL command is executed by this repository's workflows.

## Who owns what?
- **Developer** authors and tests migration SQL alongside application changes.
- **DBA** reviews risky SQL (large tables, indexes, long-running locks, destructive commands) and approves production changes.
- **DevOps** builds CI validations, approval gates, migration-job automation, auditable logs, and release ordering.
- **Cloud/DBA** manages the database instance, availability, backups and recovery. Infrastructure provisioning is distinct from schema deployment.

## Simple versioned migration example
A versioned Flyway migration file under `db/migration/V2__add_customer_email.sql` might contain:

```sql
ALTER TABLE customers
ADD COLUMN customer_email VARCHAR(255);
```

Flyway records the applied version in its schema history table and avoids applying the same version twice. This example is not executed here.

## Recommended release sequence
1. Developer opens PR with app code and migration file.
2. CI runs unit tests, SAST/SCA and validates migration scripts in an **isolated disposable test database** (a future, optional lab).
3. DBA reviews high-risk DDL and confirms backup/recovery readiness.
4. Deploy an **additive, backward-compatible** schema migration through a separately approved job/pipeline.
5. Argo CD deploys the new application version after migration succeeds.
6. Run smoke/integration tests, monitor errors and latency, and retain change evidence.

## Why expand-and-contract?
When version 1 and version 2 of the application run simultaneously during rolling deployment, both should operate safely against the new schema. First **expand** (add nullable column), then upgrade application, and later **contract** (drop old column in a subsequent release after consumers are migrated).

## Failure and rollback
If application deployment fails, roll back the application to a version compatible with the **new schema**. A `git revert` or Argo CD rollback **does not undo database schema/data changes**. Destructive migrations require a DBA-led restore/recovery procedure, ideally tested beforehand. Never assume DDL rollback will restore deleted data.

## Security controls
- Migration runner should have a separate short-lived identity and the minimum needed schema permissions.
- App runtime credentials must not carry `ALTER` or `DROP` rights.
- Review and approve production changes with protected GitHub Environments or the organization's change process.
- Do not commit connection strings, passwords or SQL dumps.

## Where should this run?
In a production setup, choose either a separate approved migration job (preferred for shared critical DBs) or an idempotent Argo CD PreSync Job with risk controls. Do not couple every Argo sync to destructive SQL.

**Lab status:** Documentation-only. No Flyway, PostgreSQL, Cloud SQL, database migration, or SQL execution has taken place.
