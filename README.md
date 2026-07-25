### Identificação do Candidato

- **Nome completo:**  Sávio Menezes Brito
- **GitHub:** https://github.com/savio-mb/

## Visão Geral da Solução

Para este desafio, escolhi desenvolver o Contador de Produção Não-Intrusivo. A ideia me chamou a atenção por ser uma solução muito prática para o dia a dia de indústrias e linhas de montagem. 

O projeto funciona, basicamente, como um detector luz na esteira. Utilizando um sensor óptico, o sistema consegue perceber sempre que uma caixa passa e interrompe a iluminação, registrando isso automaticamente no contador. Além disso, ele também fica de olho no tempo. Ou seja, se uma peça enroscar no caminho, ele percebe a demora e emite um alerta. Outro ponto é que deixei um botão configurado para que o operador possa zerar tudo de um jeito fácil quando o turno acabar.

---

## Arquitetura do Sistema Embarcado

Na hora de estruturar a lógica no main.py, fiz questão de adotar uma arquitetura de loop contínuo e não-bloqueante, como foi solicitado. 

Na prática, em vez de usar comandos que mandam o processador parar por alguns milissegundos e acabam travando o sistema, programei o código para rodar direto, apenas consultando o relógio interno da placa a cada ciclo. Com isso, o projeto passou a funcionar como um verdadeiro multitarefa onde ele consegue monitorar o sensor de luz, calcular o tempo de uma possível peça travada e ainda perceber se o botão de reset foi apertado, tudo ao mesmo tempo e sem engasgar.

---

## Componentes Utilizados na Simulação

Eu utilizei três componentes:

- Placa ESP32 DevKit: É a placa principal do projeto, onde o código é processado.
- Sensor LDR (ldr1): É o sensor de luz. Ele altera sua resistência elétrica conforme a iluminação da esteira, sinalizando quando a caixa faz sombra.
- Botão Pushbutton (btn1): Um botão para dar reset. Configurei ele usando um recurso interno da própria placa que deixou o diagrama muito mais limpo e sem a necessidade de resistores extras.

---

## Decisões Técnicas Relevantes

Durante a montagem do projeto, precisei tomar algumas decisões práticas para garantir que o código desse conta dos requisitos e não falhasse no meio do caminho:

1. A Inversão do Sinal e a Calibragem: Na teoria, sombra é falta de luz. Mas, no circuito do simulador, essa falta de luz faz a tensão do pino subir. Adaptei o código para entender essa inversão e defini uma margem de corte segura (o valor 1600). Com isso, o sistema não se confunde com qualquer variação de iluminação do ambiente e só conta a caixa quando tem certeza absoluta.

2. O Filtro do Botão: Pesquisando sobre como fazer o projeto, aprendi que todo botão físico tem um problema chato de trepidar ao ser apertado, o que faz o sistema entender vários cliques de uma vez. Para resolver isso no próprio código, criei um filtro de 50ms. Assim, ele ignora esses ruídos elétricos e só valida a ação quando percebe que a intenção de quem apertou foi firme e clara.

3. Contagem na Saída: Para não correr o risco de uma caixa passar devagar e ser contada duas vezes, programei o sistema para só registrar o "+1" no painel quando a peça terminar de passar por completo e a luz voltar a bater direto no sensor.

---

## Resultados Obtidos

Fiquei bastante satisfeito com o resultado final do projeto. No final, ele atendeu a todos os critérios solicitados no documento de requisitos:

- Contagem Normal: As caixas são detectadas sem atrasos e o painel acompanha a produção em tempo real.
- Paradas na Esteira: O sistema cumpre o que promete e avisa assim que a esteira fica ociosa e escura por mais de 5 segundos.
- Reset de Turno: O botão limpa o sistema instantaneamente sem travar as outras funções.

A versão final do projeto rodou tudo dentro do esperado.

---

## Comentários Adicionais

O que mais aprendi e achei interessante foi traduzir a luz do mundo real para o mundo lógico (a leitura do sinal no código). Acompanhar como uma simples variação de sombra se transforma em números no terminal e ter que ensinar o sistema a ignorar pequenas interferências foi um baita desafio. Isso tornou o projeto muito mais interessante, mostrando na prática como a programação precisa lidar com as imperfeições do ambiente físico para funcionar bem na vida real/dia a dia.