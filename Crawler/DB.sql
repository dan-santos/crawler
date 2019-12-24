create table candidatos(
	ID_Candidato int not null auto_increment,
    Nome_Candidato varchar (20) not null,
    constraint PK_candidatos_ID primary key (ID_Candidato)
);

create table tweets(
	ID_Tweet int not null auto_increment,
    ID_Candidato int not null,
    Conteudo_Tweet varchar(280) not null,
    Link_Tweet varchar(300) not null,
    constraint PK_tweets_ID primary key (ID_Tweet),
    constraint FK_tweets_IdCandidato foreign key (ID_Candidato) references candidatos (ID_Candidato)
);

create table tematicas(
	ID_Tematica int not null auto_increment,
    ID_Tweet int null,
    Nome_Tematica varchar(30) not null,
    constraint PK_tematicas_ID primary key (ID_Tematica),
    constraint FK_tematicas_IdTweet foreign key (ID_Tweet) references tweets (ID_Tweet)
);

create table noticias(
	ID_Noticia int not null auto_increment,
    ID_Candidato int not null,
    Titulo_Noticia varchar(60),
    Conteudo_Noticia text not null,
    Link_Noticia varchar(300) not null,
    constraint PK_noticias_ID primary key (ID_Noticia),
    constraint FK_noticias_IdCandidato foreign key (ID_Candidato) references candidatos (ID_Candidato)
);

insert into candidatos (Nome_Candidato) values ("João Dória Jr.");
insert into candidatos (Nome_Candidato) values ("Márcio França");