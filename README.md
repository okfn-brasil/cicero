# Cícero

> Quosque tandem abutere patientia nostra?

Bot que monitora a pauta de dados abertos no legislativo federal (Câmara dos Deputados e Senado Federal). O [Cícero](https://twitter.com/botcicero) tuíta sempre que um projeto de lei sobre o tema é criado.

## Instruções de uso

### Configurações

Copie os arquivos de configuração e edite-os de acordo com o desejado:

```sh
$ cp .env.sample .env
```

Em seguida, crie a tabela no banco de dados:

```sh
docker-compose run --rm scrapy python -c "from cicero.models import create_tables; create_tables()"
```

### Instalação

Requer [Docker](https://docs.docker.com/install/) e
[Docker Compose](https://docs.docker.com/compose/install/).

### Coletando dados

Para coletar os dados, utilize os raspadores regulamente, eles alimentam o banco de dados:

```sh
$ docker-compose run --rm scrapy scrapy crawl chamber
$ docker-compose run --rm scrapy scrapy crawl senate
```

### Tuitando

Para tuitar a atividade mais recente, use esse comando (cada vez que ele é executado, um tuíte é publicado com o projeto de lei ou emenda mais recente encontrado no banco e ainda não tuitado):

```sh
$ docker-compose run --rm scrapy python tweet.py
```


### Testes

```sh
docker-compose run --rm scrapy py.test
```

## Créditos

Esse repositório é um _fork_ [de um projeto](https://github.com/cuducos/raspadorlegislativo) feito para integrar o [Radar Legislativo](https://gitlab.com/codingrights/radarlegislativo), durante uma iniciativa financiada pelo [IBCCRIM](https://ibccrim.org.br). Mais tarde a [Open Knowledge Brasil](https://br.okfn.org) fez o _fork_ para iniciar o Cícero.