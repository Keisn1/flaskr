drop table if exists 'users';
drop table if exists 'videos';

create table users (
  'userId' integer primary key autoincrement,
  'name' text not null,
  'email' text unique not null,
  'password' text not null,
  'created_at' text default CURRENT_TIMESTAMP,
  'updated_at' text default CURRENT_TIMESTAMP
);

create table videos (
  'videoId' integer primary key autoincrement,
  'title' text not null,
  'description' text not null,
  'url' text not null,
  'userId' integer not null,
  'created_at' text default CURRENT_TIMESTAMP,
  'updated_at' text default CURRENT_TIMESTAMP,
  foreign key (UserId) references users (UserId)
);
