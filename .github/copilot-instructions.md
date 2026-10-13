# Instruções do projeto

## Objetivo

- Este projeto é um MVP para validar uma ideia rapidamente. Priorize entregar o resultado funcional com o menor esforço e a menor complexidade razoáveis.
- Não presuma requisitos de produto que não foram informados. Quando uma decisão importante de escopo ou comportamento estiver em aberto, pergunte antes de escolher.

## Implementação

- Antes de alterar código, confira a estrutura existente e siga os padrões já usados no projeto.
- Prefira a solução direta e legível que resolva o pedido. Evite camadas, abstrações, generalizações, padrões arquiteturais e configurações que não sejam necessários agora.
- Mantenha responsabilidades claras e código fácil de entender, sem comprometer a possibilidade de refatorar depois se a ideia for validada.
- Faça alterações pequenas e focadas no pedido. Não aproveite a tarefa para reescrever ou reorganizar partes não relacionadas.
- Reutilize as dependências e ferramentas existentes. Não adicione uma biblioteca quando a funcionalidade puder ser implementada de forma simples com o que já existe.

## Dependências e Python

- Antes de instalar ou adicionar qualquer biblioteca ou dependência, explique por que ela é necessária e peça autorização. Não instale sem consentimento.
- Todo comando Python deve ser executado em um ambiente virtual do projeto, preferencialmente `.venv`. Nunca use o Python ou o `pip` globais. Se não houver ambiente virtual, prepare ou solicite orientação antes de executar comandos Python; não instale dependências até receber autorização.

## Execução e validação

- Economize tempo e tokens: não execute a aplicação, não inicie servidores e não faça testes manuais que o usuário possa executar diretamente.
- Em particular, se a validação exigir iniciar o servidor ou interagir com a aplicação, não o faça; informe ao usuário o comando e deixe a execução para ele.
- Evite comandos de validação demorados ou que exijam instalação/configuração. Quando uma verificação automatizada existente for curta, relevante e puder ser executada sem instalar dependências, prefira a verificação mais específica; informe claramente o que foi ou não validado.

## Comunicação

- Seja conciso e indique o que mudou, decisões relevantes, verificações realizadas e como o usuário pode testar manualmente quando aplicável.
