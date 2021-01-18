INSERT INTO [dbo].[companies] ([ID], [Name])
VALUES
('bc7a63b2-1516-4cf4-9701-d1434e1eabe7', 'MyCompany Ltd'),
('987bf416-8747-4310-9c86-9c57561514b7', 'Bloggs Industries Ltd');

INSERT INTO [dbo].[users] ([ID], [Name], [Email], [CompanyID])
VALUES
('98355e46-0bdb-4d04-9bf2-ddcff230754c', 'Admin', 'admin@mycompany.com', 'bc7a63b2-1516-4cf4-9701-d1434e1eabe7'),
('de25441a-ea6c-45ea-bbf0-5d102c393e54', 'Joe Bloggs', 'joe@bloggs.com', '987bf416-8747-4310-9c86-9c57561514b7');

INSERT INTO [dbo].[assets] ([ID], [Name])
VALUES
('ffa23572-3300-4fa7-b3c2-e06d74bf6634', 'MyCompany head office'),
('013d9598-55c5-42e5-be34-2a010fb55382', 'Bloggs warehouse');

INSERT INTO [dbo].[company_assets] ([ID], [CompanyID], [AssetID])
VALUES
('de61460b-5d86-4699-a498-d11692323e4a', 'bc7a63b2-1516-4cf4-9701-d1434e1eabe7', 'ffa23572-3300-4fa7-b3c2-e06d74bf6634'),
('8da81cc6-3989-4fe2-bab6-5cf2db9bc4f1', 'bc7a63b2-1516-4cf4-9701-d1434e1eabe7', '013d9598-55c5-42e5-be34-2a010fb55382'),
('67296035-a342-43e1-a83b-cfd1d63cc236', '987bf416-8747-4310-9c86-9c57561514b7', '013d9598-55c5-42e5-be34-2a010fb55382');

INSERT INTO [dbo].[asset_data] ([ID], [AssetID], [Parameter], [Value], [Description])
VALUES
('fcda7621-9c55-442a-9da2-a9143e7147ae', 'ffa23572-3300-4fa7-b3c2-e06d74bf6634', 'Location', 'MyCity', 'Office location'),
('dadd896d-ba82-48a8-8fd3-b8e22b974a1c', 'ffa23572-3300-4fa7-b3c2-e06d74bf6634', 'Size', '50', 'Office square footage'),
('11b9a85c-4012-4f00-947b-037c586aac6b', '013d9598-55c5-42e5-be34-2a010fb55382', 'Location', 'Bloggsville', 'Warehouse location'),
('b9642f71-b4a2-4158-b1fe-f23961ccb983', '013d9598-55c5-42e5-be34-2a010fb55382', 'Inventory', '2000', 'Product count in warehouse');
