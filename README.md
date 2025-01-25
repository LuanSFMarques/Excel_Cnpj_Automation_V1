# Processador de Dados de CNPJ com Integração de API

Este projeto oferece uma solução automatizada em Python para processar dados de CNPJs extraídos de planilhas Excel, realizar consultas a uma API pública e registrar os resultados diretamente no arquivo Excel. Além disso, os dados são armazenados em um histórico CSV para consultas futuras.

## Disclaimer

**Português**  
**Este algoritmo foi desenvolvido para ser utilizado no Brasil, pois a API integrada é exclusiva para dados relacionados ao Cadastro Nacional da Pessoa Jurídica (CNPJ) no território brasileiro.** Portanto, não será possível utilizá-lo para CNPJs de outros países ou realizar consultas internacionais.

**English**  
**This algorithm was developed to be used in Brazil, as the integrated API is exclusive for data related to the National Register of Legal Entities (CNPJ) within Brazilian territory. Therefore,** it will not be possible to use it for CNPJs from other countries or perform international queries.


## Sumário

1. [Visão Geral](#visão-geral)  
2. [Funcionalidades](#funcionalidades)  
3. [Limitações da API](#limitações-da-api)  
4. [Configuração e Instalação](#configuração-e-instalação)  
5. [Como Usar](#como-usar)  
6. [Personalização](#personalização)  
7. [Requisitos](#requisitos)  
8. [Contribuição](#contribuição)  
9. [Licença](#licença)  

## Visão Geral

O **Processador de Dados de CNPJ** é uma ferramenta versátil que realiza:  
- Leitura de identificadores de CNPJ de um arquivo Excel.  
- Integração com a API pública `https://publica.cnpj.ws/` para buscar dados relevantes como:  
  - Situação Cadastral  
  - Cidade e Estado  
  - Nome dos Sócios  
  - Contatos (Telefone e E-mail)  
- Registro dos resultados em uma cópia da planilha original.  
- Armazenamento de logs detalhados em formato CSV.  

### Exemplo de Caso de Uso
Empresas podem utilizar este projeto para enriquecer bases de dados de clientes ou fornecedores com informações atualizadas, evitando decisões baseadas em dados desatualizados.

## Funcionalidades

- **Processamento Seguro**: O algoritmo trabalha em uma cópia da planilha original, preservando os dados originais.  
- **Registro em CSV**: Todas as interações e respostas da API são salvas para auditoria e reuso.  
- **Flexibilidade**: Possibilidade de personalizar o intervalo de linhas a ser processado.  

## Limitações da API

A API pública utilizada tem uma **limitação de 3 requisições por minuto**. O script implementa uma pausa automática para respeitar esse limite.

## Configuração e Instalação

### Pré-requisitos

1. Python 3.7 ou superior instalado.  
2. Bibliotecas necessárias:  
   - `pandas`  
   - `requests`  
   - `openpyxl`  
## Como Usar

1. **Edite o arquivo principal (`main()`):**  
- Defina o intervalo de linhas a ser processado:
  ```python
  row_range = [0, 100]  # Exemplo: Processar as 100 primeiras linhas
  ```
- Atualize o nome das colunas dado a direita, se necessário:
  ```python
  col_names = {
      "Situação Cadastral": "SITUAÇÃO",
      "Cidade_e_Estado": "CIDADE",
      "Socios": "SOCIOS",
      "Telefone": "TELEFONE",
      "Email": "EMAIL"
  }
  ```

2. **Execute o script:**  
```Python
python main.py
```

3. **Verifique os resultados:**  
- Arquivo Excel processado: `excel/CNPJ_COPIA.xlsx`  
- Logs das interações: `cnpj_data_hist.csv`  
## Requisitos

- **Sistema Operacional:** Compatível com Windows, macOS e Linux.  
- **Softwares Adicionais:** Requer suporte ao formato Excel através de `openpyxl`.  

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
