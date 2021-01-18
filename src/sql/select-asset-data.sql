USE [mydb]
EXECUTE AS USER = 'middleware';
EXEC sp_set_session_context @Key=N'UserID', @value=null;
SELECT * FROM asset_data
GO

USE [mydb]
EXECUTE AS USER = 'middleware';
EXEC sys.sp_set_session_context @Key=N'UserID', @value=N'98355e46-0bdb-4d04-9bf2-ddcff230754c';
SELECT * FROM asset_data
GO

USE [mydb]
EXECUTE AS USER = 'middleware';
EXEC sp_set_session_context @Key=N'UserID', @value=N'de25441a-ea6c-45ea-bbf0-5d102c393e54';
SELECT * FROM asset_data
GO

