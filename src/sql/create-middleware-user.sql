DROP USER IF EXISTS [middleware];
GO

CREATE USER [middleware] FOR LOGIN [middleware] WITH DEFAULT_SCHEMA=[dbo];
GRANT SELECT, INSERT, UPDATE, DELETE ON [dbo].[asset_data] TO [middleware];
DENY UPDATE ON [dbo].[asset_data](AssetID) TO [middleware];
GO
