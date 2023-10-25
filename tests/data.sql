delete from users;
delete from `sqlite_sequence`;
insert into users
       (name, email, password, created_at, updated_at)
       values('test_name1', 'test_email1',
       'pbkdf2:sha256:600000$CflColapQX5g4WLt$39a913130a5d99c762237a97439f63d59d90f4f958c28bc16d69b2c31f5d7e85',
       '2023-10-12 00:00:00', '2023-10-12 01:00:00');
