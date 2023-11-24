delete from `sqlite_sequence`;
delete from users;
insert into users (name, email, password, created_at, updated_at) values
            ('test_name1', 'test_email1', 'pbkdf2:sha256:600000$KctZrvFhZznh0qGO$a20b5d4c31529cca7cbb83755c04166306058f3741909e4ececf90fc2dd3edb3', '2023-10-12 00:00:00', '2023-10-12 01:00:00'),
            ('test_name2', 'test_email2', 'pbkdf2:sha256:600000$6lgJ4rydabvwP5sL$550b65660f286fa81293cf4280b8a726a3feeff2bb5e236ed1f8c1a67820c489', '2023-10-13 00:00:00', '2023-10-13 01:00:00');


delete from videos;
insert into videos (title, description, videoPath, userId) values
            ('test_title1','test_description1','test_path1',1),
            ('test_title2','test_description2','test_path2',1),
            ('test_title3','test_description3','test_path3',2);
