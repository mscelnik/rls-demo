-- https://docs.microsoft.com/en-us/sql/relational-databases/security/row-level-security
-- https://github.com/Azure-Samples/azure-sql-db-secure-data-access-api

DROP SECURITY POLICY IF EXISTS rls.AssetDataFilter;
DROP FUNCTION IF EXISTS rls.fn_SecurityPredicate;
DROP FUNCTION IF EXISTS rls.fn_UserAssets;
DROP SCHEMA IF EXISTS rls;
GO

CREATE SCHEMA rls;
GO

CREATE FUNCTION rls.fn_UserAssets(@UserID sql_variant)
    RETURNS TABLE
    WITH SCHEMABINDING
AS
    RETURN SELECT dbo.company_assets.AssetID FROM
    dbo.users
    LEFT JOIN
    dbo.companies ON dbo.users.CompanyID = dbo.companies.ID
    RIGHT JOIN
    dbo.company_assets ON dbo.companies.ID = dbo.company_assets.CompanyID
    WHERE
    dbo.users.ID = CONVERT(uniqueidentifier, @UserID);
GO

CREATE FUNCTION rls.fn_SecurityPredicate(@AssetID uniqueidentifier)
    RETURNS TABLE
    WITH SCHEMABINDING
AS
    RETURN SELECT 1 AS fn_SecurityPredicate_result
    WHERE
    DATABASE_PRINCIPAL_ID() = DATABASE_PRINCIPAL_ID(N'middleware')
    AND
    @AssetID IN (SELECT AssetID FROM rls.fn_UserAssets(SESSION_CONTEXT(N'UserID')))
    OR
    IS_MEMBER(N'db_owner') = 1;

GO

CREATE SECURITY POLICY rls.AssetDataFilter
    ADD FILTER PREDICATE rls.fn_SecurityPredicate(AssetID)
        ON [dbo].[asset_data],
    ADD BLOCK PREDICATE rls.fn_SecurityPredicate(AssetID)
        ON [dbo].[asset_data] AFTER INSERT
    WITH (STATE = ON);
GO
