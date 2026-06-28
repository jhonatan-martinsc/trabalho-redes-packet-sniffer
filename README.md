# 🌐 Python Packet Sniffer (Analisador de Tráfego de Rede)

Este projeto é um **interceptador de pacotes de rede (Packet Sniffer)** desenvolvido em Python. Baseado em uma estrutura de captura de baixo nível, o projeto foi expandido para suportar o desempacotamento e a interpretação semântica de protocolos das camadas de Enlace e de Aplicação.

---

## 🚀 Novas Funcionalidades Implementadas

O código original capturava protocolos base (**Ethernet, IPv4, ICMP, TCP e UDP**). Neste projeto, foram desenvolvidos interpretadores avançados para as seguintes camadas:

* **ARP (Camada de Enlace):** Decodifica frames Ethernet (`0x0806`), extraindo o OpCode, endereços MAC e IPs de origem (Sender) e destino (Target).

* **DNS (Camada de Aplicação):** Intercepta o tráfego UDP na porta **53**, extraindo o **Transaction ID**, **Flags** e convertendo o **Query Name** em texto legível.

* **HTTP (Camada de Aplicação):** Analisa pacotes TCP na porta **80**, convertendo o payload em UTF-8 para identificar metadados importantes da navegação (**Method**, **Host** e **User-Agent**).

---

## 📋 Pré-requisitos

Devido ao uso de **raw sockets** (`AF_PACKET`) em modo promíscuo, que exigem acesso direto ao hardware de rede, este projeto **não funciona no Windows de forma nativa**.

* **Sistema Operacional:** Linux (Físico, WSL ou Máquina Virtual)
* **Linguagem:** Python 3.x
* **Privilégios:** Root / Administrador (`sudo`)

---

## 🛠️ Como Executar

### 1. Clone o repositório

```bash
git clone https://github.com/SEU-USUARIO/NOME-DO-REPOSITORIO.git
```

### 2. Entre na pasta do projeto

```bash
cd NOME-DO-REPOSITORIO
```

### 3. Execute o programa

```bash
sudo python3 sniffer.py
```

---

## 🧪 Como Testar

Com o sniffer executando em um terminal, utilize um segundo terminal para gerar tráfego de rede.

### 📡 Testando o Interpretador ARP

Dispare um ping para um IP inexistente na rede local para forçar uma requisição ARP.

```bash
ping 10.0.2.99
```

### 🌍 Testando o Interpretador DNS

Force uma consulta DNS utilizando o servidor do Google.

```bash
nslookup ucs.br 8.8.8.8
```

### 🌐 Testando o Interpretador HTTP

Faça uma requisição HTTP simples.

```bash
curl http://ucs.br
```

---

## 📁 Estrutura do Projeto

O projeto está organizado da seguinte forma, separando claramente os módulos desenvolvidos neste trabalho dos arquivos base do repositório original:

### Módulos Desenvolvidos

* **sniffer.py** — Arquivo principal (refatorado) contendo o loop de captura de pacotes e a hierarquia de identificação dos protocolos.
* **arp_decoder.py** — Responsável pelo parsing e interpretação dos pacotes ARP.
* **dns_decoder.py** — Responsável por extrair o *Query Name* e demais informações dos pacotes DNS.
* **http_decoder.py** — Responsável por interpretar requisições HTTP e extrair informações como *Method*, *Host* e *User-Agent*.
* **README.md** — Documentação do projeto.

### Módulos Base (Repositório Original)

* **networking/** — Contém as classes originais para desempacotamento dos protocolos Ethernet, IPv4, TCP, UDP, ICMP, HTTP e gravação PCAP.
* **Other/** — Diagramas de referência dos cabeçalhos de rede e materiais auxiliares do projeto original.
* **general.py** — Funções utilitárias para formatação de endereços MAC e exibição de dados.
* **.gitignore** — Arquivo de configuração do Git.

---

## 📚 Tecnologias Utilizadas

* Python 3
* Raw Sockets (`AF_PACKET`)
* Programação de Redes
* Protocolos Ethernet, ARP, IPv4, ICMP, TCP, UDP, DNS e HTTP

---

## 👨‍💻 Autor

Projeto desenvolvido para a disciplina de **Redes de Computadores** — **2026**.
