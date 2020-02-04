create database eleicoes;
use eleicoes;
drop table tematicas;

create table candidatos(
	ID_Candidato int not null auto_increment,
    Nome_Candidato varchar (20) not null,
    constraint PK_candidatos_ID primary key (ID_Candidato)
);

create table tweets(
	ID_Tweet int not null auto_increment,
    ID_Candidato int not null,
    Conteudo_Tweet text not null,
    constraint PK_tweets_ID primary key (ID_Tweet),
    constraint FK_tweets_IdCandidato foreign key (ID_Candidato) references candidatos (ID_Candidato)
);

create table tematicas(
	ID_Tematica int not null auto_increment,
    ID_Candidato int not null,
    Nome_Tematica varchar(80) not null,
    Quantidade_Tematica int not null,
    constraint PK_tematicas_ID primary key (ID_Tematica),
    constraint FK_tematicas_IdCandidato foreign key (ID_Candidato) references candidatos (ID_Candidato)
);

create table noticias(
	ID_Noticia int not null auto_increment,
    Titulo_Noticia text not null,
    Link_Noticia text not null,
    Relevancia_Noticia int not null,
    constraint PK_noticias_ID primary key (ID_Noticia)
);

drop table noticias;

insert into candidatos (Nome_Candidato) values ("João Dória Jr.");
insert into candidatos (Nome_Candidato) values ("Márcio França");

delete from tweets;

select Conteudo_Tweet from tweets;

select * from candidatos;
select count(*) from tematicas;
select count(*) from tweets;
select * from noticias limit 250;
drop table tematicas;
drop table tweets;

select tematicas.Quantidade_Tematica as 'Quantidade de Aparições', tematicas.Nome_Tematica as 'Palavra / Temática', candidatos.Nome_Candidato as 'Candidato que mencionou'
from tematicas, candidatos where tematicas.ID_Candidato = candidatos.ID_Candidato
order by Quantidade_Tematica desc;

select tweets.Conteudo_Tweet as 'Tweet'
from tweets
order by tweets.ID_Candidato asc;

select count(*) from tweets where ID_Candidato = 2;

select noticias.ID_Noticia as 'ID', noticias.Titulo_Noticia as 'Título da notícia', noticias.Link_Noticia as 'Link', noticias.Relevancia_Noticia as 'Relevância'
from noticias order by ID_Noticia asc;