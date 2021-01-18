DROP LOGIN IF EXISTS [middleware];
GO

CREATE LOGIN [middleware] WITH PASSWORD=?,
DEFAULT_DATABASE=[mydb],
DEFAULT_LANGUAGE=[us_english],
CHECK_EXPIRATION=OFF,
CHECK_POLICY=OFF
GO
