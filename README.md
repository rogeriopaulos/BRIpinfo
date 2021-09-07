# BrIpInfo

![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/rogeriopaulos/BRIpinfo?label=BRIpinfo&style=flat-square)
![Python](https://img.shields.io/badge/python-3.8%2B-yellowgreen?style=flat-square)
![GitHub](https://img.shields.io/github/license/rogeriopaulos/BRIpinfo?style=flat-square)

Uma maneira fácil de obter dados relativos a um IP/bloco CIDR associado a um fornecedor de serviço de internet (ISP).

Periodicamente, o [Registro.br](https://registro.br/) disponibiliza, via [ftp](https://ftp.registro.br/pub/numeracao/origin/nicbr-asn-blk-latest.txt), uma listagem (em um arquivo _.txt_) dos IPs/blocos CIDR ativos no Brasil, bem como a qual fornecedor de serviço de internet o mesmo é associado (juntamente com seu CNPJ).

A partir do desse arquivo, o BrIpInfo analisa e estrutura esses dados de uma forma amigável, permitindo a exportação do mesmo para os formatos _json_ ou _csv_.

## Features

- Obtenção da listagem completa do IPs ativos no Brasil, e suas respectivas ISP's, com base no [Registro.br](https://registro.br/);
- Fácil atualização da listagem disponibilizada;
- Exportação dos dados em um arquivo _json_ ou _csv_.

## Pré-Requisitos

- [Python 3.8+](https://www.python.org/downloads/)
- [git](https://git-scm.com/downloads)

## Instalação & Configuração

### Clonar repositório

Faça o clone do repositório da aplicação em um local de sua preferência.

```
git clone https://github.com/rogeriopaulos/BRIpinfo.git
```

### Crie um ambiente virtual [OPCIONAL]

Embora não seja obrigatório, é recomendável a criação prévia de um ambiente virtual do python. Para maiores informações, veja esse [passo-a-passo](https://cloud.google.com/python/setup?hl=pt-br).

### Instalando as dependências

No _prompt de comando_ ou _terminal_ do seu sistema operacional, acesse a pasta da aplicação e instale as dependências da mesma executando o comando abaixo.

_Ps: Caso tenha criado um ambiente virtual antes, ative-o._

```
pip install -r requirements.txt
```

### Setup da aplicação

Para finalizar, execute o _setup_ da aplicação.

**Importante**: Para que o _setup_ da aplicação ocorra normalmente, é necessário uma conexão de internet ativa.

_Ps: Caso tenha criado um ambiente virtual antes, ative-o._

```
python bripinfo setup
```

## Comandos & Uso

### Geral
```
Usage: bripinfo [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  export  Export data from registro.br to json/csv.
  query   Query IP or CNPJ from Registro.br.
  setup   Load data from registro.br.
```

### Exportação

```
Usage: bripinfo export [OPTIONS]

  Export data from registro.br to json/csv.

Options:
  -f, --format TEXT       Format: [json, csv]. Default: json.
  -d, --destination TEXT  Where to save. Default: "<current-dir>".

  -n, --name TEXT         Filename. Default: "nicbr-asn-blk-latest"
  --help                  Show this message and exit.
```

### Consulta

```
Usage: bripinfo query [OPTIONS]

  Query IP or CNPJ from Registro.br.

Options:
  -t, --type TEXT    Type of query: [ip, cnpj]
  -s, --search TEXT  Term to searched (ip or cnpj). Ex: 192.168.0.22 (ip) |
                     10942479000139 (cnpj)

  --help             Show this message and exit.
```

### Exemplos

```
python bripinfo export
```
...um arquivo no formato _json_ será gerado no diretório corrente onde a aplicação foi baixada (_git clone_).


```
python bripinfo export -f csv -d /home -n "test"
```
...um arquivo no formato _csv_, com o nome _"test"_, será gerado no diretório __"/home"__.

```
python bripinfo query -t ip -s "186.241.20.224"

# output
{
    "cnpj": "33.000.118/0001-79",
    "ips": [
        "200.223.0.0/16",
        "200.199.0.0/17",
        (...)
    ],
    "name": "Telemar Norte Leste S.A.",
    "ref": "AS7738"
}
```


## Versionamento

Este projeto segue as diretrizes do versionamento semântico (SemVer). Para maiores informações, acesse esse [link](https://semver.org/lang/pt-BR/).

## Licença

Veja o arquivo [LICENÇAS](LICENSE) para saber os direitos e limitações da licença aplicada neste projeto (*MIT*).