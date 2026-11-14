from pathlib import Path
from datetime import datetime
from html import escape
import re
import shutil
import sys

arquivo = Path("public/index.html")
if not arquivo.exists():
    sys.exit("ERRO: public/index.html não encontrado.")

conteudo = arquivo.read_text(encoding="utf-8")

inicio = '<section class="section proposals-section" id="propostas">'
fim = '<section class="section reconstruction-section" id="reconstrucao">'

if conteudo.count(inicio) != 1 or conteudo.count(fim) != 1:
    sys.exit("ERRO: não foi possível identificar com segurança os limites da seção.")

if conteudo.index(fim) < conteudo.index(inicio):
    sys.exit("ERRO: estrutura inesperada. Nenhuma alteração realizada.")

propostas = [
{
"titulo": "Amor ao Brasil e compromisso nacional",
"original": "que o povo tenha amor ao Brasil",
"leitura": "A declaração apresenta o amor ao Brasil como princípio central de orientação da vida coletiva. A ideia é valorizar o vínculo dos cidadãos com o país e estimular uma postura de responsabilidade em relação à sua sociedade, território e futuro.",
"objetivos": ["Estimular o sentimento de pertencimento nacional.", "Valorizar a responsabilidade individual e coletiva pelo desenvolvimento do Brasil.", "Associar o patriotismo à contribuição concreta para o país."],
"possibilidades": ["Debates públicos sobre cidadania, história e realidade brasileira.", "Ações educativas e comunitárias de valorização do patrimônio nacional.", "Campanhas de participação social e cuidado com os espaços coletivos."],
"condicoes": "As iniciativas devem respeitar o pluralismo, a liberdade de consciência, a diversidade cultural e a convivência democrática. O patriotismo não deve ser confundido com obrigação de concordar com governos, partidos ou opiniões políticas.",
"questoes": "Como o autor pretende transformar o amor ao Brasil em ações concretas? Quais atividades educativas ou comunitárias considera prioritárias?",
"esclarecimento": "A declaração original não especifica instrumentos, programas, órgãos responsáveis ou obrigações legais."
},
{
"titulo": "Acesso à Constituição Federal e cumprimento das leis",
"original": "Que todo o brasileiro tenha em casa a constituição Federal ou leia atravez da Internet, e trabalhe para fazer cumprir a constituição Federal brasileira",
"leitura": "A proposta busca ampliar o conhecimento da Constituição Federal e incentivar os cidadãos a conhecerem seus direitos, deveres e mecanismos de participação, contribuindo para que as normas constitucionais sejam respeitadas.",
"objetivos": ["Facilitar o acesso à Constituição em formato impresso e digital.", "Estimular a educação constitucional.", "Incentivar o exercício responsável da cidadania e a cobrança pelo cumprimento das leis."],
"possibilidades": ["Disponibilização de materiais de leitura em linguagem acessível.", "Atividades de educação cívica em escolas e associações.", "Divulgação dos canais institucionais de informação, denúncia e participação."],
"condicoes": "O acesso à Constituição deve ser voluntário e acompanhado de informação confiável. A interpretação e aplicação das normas devem respeitar as instituições competentes e os procedimentos legais.",
"questoes": "A proposta pretende distribuir exemplares impressos? Como seriam organizadas as ações de orientação e educação constitucional?",
"esclarecimento": "A expressão original 'trabalhe para fazer cumprir' é preservada como incentivo à participação cidadã, não como autorização para substituir autoridades ou procedimentos legais."
},
{
"titulo": "Aquisição de terras às margens das rodovias e desenvolvimento produtivo",
"original": "A desapropriação das margens das estradas 300 metro de cada lado,seja divido em 100 metros por 300 e 3 hectares, e que seja criado o dia da terra e que todo brasileiro entenda que Deus fez a terra para que o homem more e trabalhe na terra, que crie o dia da terra, novembro a dezembro, todo cidadão brasileiro se volte a pensar na terra, e desenvolver a terra para que se produza mais alimento na terra",
"leitura": "A declaração reúne a ideia de aquisição de áreas próximas às rodovias, organização de lotes para moradia e produção, valorização do trabalho rural e criação de um período nacional de reflexão sobre a terra. A referência religiosa expressa a visão do autor sobre a finalidade social e produtiva da terra.",
"objetivos": ["Debater o aproveitamento produtivo de áreas próximas às rodovias.", "Estudar lotes com as dimensões mencionadas pelo autor: 100 por 300 metros, equivalentes a 3 hectares.", "Ampliar oportunidades de moradia, trabalho rural e produção de alimentos.", "Criar uma mobilização nacional em novembro e dezembro em torno da terra."],
"possibilidades": ["Estudos territoriais, fundiários, ambientais e econômicos sobre áreas potencialmente adequadas.", "Avaliação da infraestrutura, água, acesso, segurança e aptidão agrícola.", "Debate sobre programas de produção de alimentos e apoio a famílias trabalhadoras rurais.", "Discussão pública sobre a criação do chamado Dia da Terra e sua realização em novembro e dezembro."],
"condicoes": "Qualquer aquisição ou intervenção fundiária depende de fundamento legal, avaliação, orçamento, planejamento, respeito à propriedade, proteção ambiental e procedimentos administrativos e judiciais aplicáveis. A faixa de 300 metros e o parcelamento proposto não são apresentados como regra vigente.",
"questoes": "A faixa de 300 metros seria medida a partir de qual limite da rodovia? A proposta se aplicaria a todas as estradas? Como seriam escolhidas as áreas, os beneficiários e as atividades produtivas?",
"esclarecimento": "O texto original usa a palavra 'desapropriação'. A proposta seguinte esclarece que o autor pretende a compra da terra, e não a tomada forçada. Essa distinção precisa ser mantida e aprofundada antes de qualquer formulação jurídica."
},
{
"titulo": "Participação de empresários no apoio aos trabalhadores da terra",
"original": "quem é empresário rico se volte para ajudar os que trabalham na terra em novembro a dezembro, dia da terra",
"leitura": "A proposta convida empresários com maior capacidade econômica a contribuir com pessoas que trabalham na terra durante o período de novembro a dezembro, associado pelo autor ao Dia da Terra.",
"objetivos": ["Estimular a cooperação entre empresários e trabalhadores rurais.", "Fortalecer iniciativas de produção e desenvolvimento no campo.", "Valorizar a solidariedade e a responsabilidade social."],
"possibilidades": ["Debate sobre apoio financeiro, técnico, material ou logístico.", "Parcerias voluntárias com associações e trabalhadores rurais.", "Ações de capacitação, fornecimento de equipamentos e apoio à produção, conforme definição futura."],
"condicoes": "A participação empresarial deve respeitar a legislação, a transparência, a autonomia dos beneficiários e a liberdade de adesão. Não se presume obrigação compulsória, contribuição obrigatória ou mecanismo de cobrança.",
"questoes": "O apoio seria voluntário ou decorreria de alguma política pública? Quais formas de ajuda o autor considera adequadas? Como seriam escolhidos os beneficiários?",
"esclarecimento": "Esta é uma proposta própria e distinta da política de aquisição de terras e do apoio estatal ao agronegócio."
},
{
"titulo": "Compra das terras pela União, sem tomada forçada",
"original": "e que não seja desapropriado, que significa que a unicao [União] cumpre [compre] a terra das pessoas que tem terra onde vai ser desapropriação na margem das estradas, não e tomar, é comprar, que a terra seja da união, que as pessoa possam trabalhar e viver na terra, que a terra seja da união",
"leitura": "Esta declaração esclarece a intenção do autor em relação à proposta fundiária: a União compraria as propriedades situadas nas áreas abrangidas pela iniciativa, em vez de simplesmente tomar as terras dos proprietários. Depois da aquisição, as áreas permaneceriam pertencendo à União e poderiam ser destinadas ao trabalho e à moradia de pessoas interessadas.",
"objetivos": ["Distinguir compra de propriedade de tomada forçada.", "Debater a aquisição pública de terras mediante negociação e pagamento.", "Estudar formas de utilização das áreas por famílias que trabalhem e vivam no local."],
"possibilidades": ["Estudos sobre avaliação de imóveis, negociação e disponibilidade orçamentária.", "Definição transparente de critérios para utilização das terras públicas.", "Estudo de instrumentos de concessão, autorização ou outros modelos juridicamente adequados."],
"condicoes": "A compra pública depende de avaliação, disponibilidade orçamentária, procedimento legal e respeito aos direitos dos proprietários. A destinação posterior exige regras claras, fiscalização, proteção ambiental e definição da situação jurídica dos ocupantes.",
"questoes": "A aquisição seria exclusivamente consensual? Como seria calculado o preço? Qual seria o regime de uso das terras pelas famílias? Haveria prazo, sucessão, transferência ou condições de permanência?",
"esclarecimento": "A palavra 'desapropriação' aparece na declaração anterior, mas aqui o autor afirma expressamente: 'não é tomar, é comprar'. A aparente contradição deve ser registrada, não ocultada."
},
{
"titulo": "Continuidade do ensino e debate sobre ENEM e vestibulares",
"original": "o partido foi criado para tirar o vestibular e o enem, quando as pessoas fizeram o ensino fundamental não tenha barreira para passar direto para faculdade, ensino continuado, não pode ser barrada pelo enem e nem pelo vestibular",
"leitura": "A proposta defende uma trajetória educacional contínua, questionando o uso do ENEM e dos vestibulares como barreiras de ingresso no ensino superior. O autor deseja que a conclusão de etapas da educação permita continuidade dos estudos, sem os processos seletivos mencionados.",
"objetivos": ["Debater alternativas ao modelo de seleção para ingresso no ensino superior.", "Valorizar a continuidade da formação escolar.", "Ampliar oportunidades de acesso à universidade."],
"possibilidades": ["Estudos sobre modelos de ingresso e transição entre educação básica e superior.", "Debate sobre avaliação ao longo da trajetória escolar.", "Análise de vagas, capacidade das instituições, financiamento e critérios acadêmicos."],
"condicoes": "Qualquer mudança deve considerar a Constituição, a legislação educacional, a autonomia universitária, a igualdade de acesso e a capacidade de atendimento das instituições. A proposta não significa que a conclusão do ensino fundamental, isoladamente, já confira ingresso automático em curso superior.",
"questoes": "O autor pretende ingresso direto após o ensino fundamental ou continuidade após a conclusão do ensino médio? Como seriam organizadas as vagas e a avaliação da aprendizagem?",
"esclarecimento": "A declaração original menciona expressamente o ensino fundamental e o acesso à faculdade. Essa formulação é mantida, mas sua aplicação prática precisa ser esclarecida."
},
{
"titulo": "Formação de profissionais conforme as necessidades dos municípios e estados",
"original": "e que todos os municípios e Estados formam seu corpo técnico que eles precisam, quando médicos precisam naquele município, e selecionam os melhores alunos, que o município vai colocar na universidade, que o município que vai pagar as universidades, para aue essas pessoas se formam pelo município",
"leitura": "A proposta sugere que municípios e estados identifiquem quais profissionais são necessários em seus territórios, selecionem estudantes e financiem sua formação técnica ou universitária, conforme as necessidades locais.",
"objetivos": ["Identificar carências de profissionais em cada município e estado.", "Apoiar a formação de estudantes em áreas consideradas necessárias.", "Aproximar o planejamento educacional das necessidades dos serviços públicos locais."],
"possibilidades": ["Levantamento periódico das necessidades de profissionais.", "Programas de bolsas ou financiamento público com critérios transparentes.", "Convênios com instituições de ensino, respeitada sua autonomia.", "Planejamento de vagas e áreas de formação conforme estudos de demanda."],
"condicoes": "O programa exigiria previsão orçamentária, critérios públicos de seleção, regras de acompanhamento, igualdade de oportunidades e instrumentos jurídicos adequados. O financiamento municipal de cursos superiores precisa ser analisado conforme as competências e responsabilidades de cada ente federativo.",
"questoes": "Quais critérios definiriam os melhores alunos? Como seriam distribuídas as vagas? O município financiaria integralmente os cursos? Como seriam tratadas as necessidades de estudantes de baixa renda?",
"esclarecimento": "A proposta seguinte trata separadamente do retorno e da atuação profissional de quem receber apoio para estudar."
},
{
"titulo": "Retorno dos profissionais formados ao município financiador",
"original": "essas pessoas que são formadas pelo município, quando terminarem de se formar, quando voltarem para o município, ja é um funcionário automaticamente do município",
"leitura": "A proposta complementa a anterior ao defender que estudantes cuja formação tenha sido financiada pelo município retornem ao território e contribuam profissionalmente com a comunidade que apoiou seus estudos.",
"objetivos": ["Estimular a permanência ou o retorno de profissionais aos municípios.", "Aproveitar a formação financiada com recursos públicos em benefício da população local.", "Reduzir carências de profissionais em áreas necessárias."],
"possibilidades": ["Estudo de contratos de bolsa com compromissos de retorno ou prestação de serviços, quando juridicamente admissíveis.", "Programas de residência, estágios e cooperação profissional.", "Planejamento de concursos e processos seletivos para os cargos necessários."],
"condicoes": "A contratação automática para cargo público não pode ser presumida como juridicamente permitida. O ingresso no serviço público deve respeitar a Constituição, especialmente as regras de concurso público, as exceções legais, a igualdade e os direitos do profissional.",
"questoes": "Por quanto tempo o profissional deveria trabalhar no município? O compromisso seria proporcional ao apoio recebido? O que ocorreria se não houvesse vaga ou se o profissional não pudesse retornar?",
"esclarecimento": "A expressão 'funcionário automaticamente' é parte essencial da declaração original e não foi apagada. Sua viabilidade jurídica é uma questão expressamente pendente."
},
{
"titulo": "Alfabetização, matemática e conhecimento das leis desde o primeiro ano escolar",
"original": "quando bota o menino no primeiro ano de escola, ele tem que aprender de inciio, ler e escrever a matemática, e observar a lei orgânica do município e a constituição do estado e a constituição Federal",
"leitura": "A proposta defende que a formação escolar comece com o domínio da leitura, da escrita e da matemática, acompanhado de noções sobre a organização política e jurídica do município, do estado e do país.",
"objetivos": ["Fortalecer a alfabetização e a aprendizagem matemática desde os primeiros anos.", "Estimular a formação cidadã.", "Apresentar às crianças, de forma adequada à idade, as instituições e normas que organizam a sociedade."],
"possibilidades": ["Materiais didáticos acessíveis sobre município, estado e União.", "Atividades de cidadania adaptadas à faixa etária.", "Integração de conteúdos cívicos ao currículo escolar, sem prejudicar a alfabetização e as demais aprendizagens."],
"condicoes": "A proposta deve respeitar a legislação educacional, a Base Nacional Comum Curricular, a autonomia pedagógica e o desenvolvimento infantil. O conteúdo jurídico deve ser adequado à idade e não pode substituir o ensino fundamental de leitura, escrita e matemática.",
"questoes": "O que significa 'observar' as leis nessa etapa? O autor imagina leitura de trechos, explicações em sala ou atividades práticas?",
"esclarecimento": "A declaração distingue o aprendizado básico de leitura, escrita e matemática da formação sobre as normas municipais, estaduais e federais."
},
{
"titulo": "Critérios técnicos para a escolha do Ministro da Fazenda",
"original": "o ministro da fazenda venha de uma carreira de economia e que seja aprovado pelas organizações do sistema econômico, tipo uma eleição para ser aprovado pelas organizações de economia",
"leitura": "A proposta defende que a escolha do Ministro da Fazenda considere trajetória profissional na área econômica e inclua alguma forma de avaliação ou aprovação por organizações ligadas ao sistema econômico.",
"objetivos": ["Valorizar experiência e qualificação técnica na condução da política econômica.", "Debater a participação de organizações econômicas na avaliação de candidatos.", "Estimular transparência e responsabilidade na escolha de dirigentes."],
"possibilidades": ["Debate sobre requisitos de experiência e formação.", "Audiências e consultas a entidades representativas.", "Estudo de modelos de avaliação pública e apresentação de critérios técnicos."],
"condicoes": "A nomeação ministerial deve respeitar as competências constitucionais do Presidente da República e as regras legais aplicáveis. Uma votação de entidades privadas não pode ser apresentada como requisito vigente sem alteração normativa válida.",
"questoes": "Quais organizações participariam? Como seriam escolhidas? A aprovação seria consultiva ou vinculante? O que o autor entende por carreira de economia?",
"esclarecimento": "A expressão 'tipo uma eleição' é preservada como ideia de consulta ou aprovação a ser detalhada, sem inventar um sistema eleitoral específico."
},
{
"titulo": "Transferência de pessoas condenadas para outra cidade do mesmo estado",
"original": "Todas as pessoas que cometerem crime, que vão para a justiça e foram processadas, ele não pode ficar na cidade onde cometeu crime, ele precisa ir para outra cidade naquele mesmo estado por um período de 19 anos mais ou menos",
"leitura": "A proposta sugere que pessoas que cometeram crimes e foram processadas sejam transferidas para outra cidade do mesmo estado, por período aproximado de 19 anos. A declaração associa a mudança de local à resposta estatal ao crime.",
"objetivos": ["Debater medidas territoriais relacionadas à segurança pública e à prevenção de novos delitos.", "Avaliar a ideia de afastamento da pessoa condenada do local em que ocorreu o crime.", "Examinar possíveis efeitos sobre vítimas, comunidades e reintegração social."],
"possibilidades": ["Estudo jurídico e penitenciário da proposta.", "Análise de alternativas de cumprimento de pena e medidas cautelares já previstas em lei.", "Avaliação de custos, capacidade das unidades, vínculos familiares e acompanhamento social."],
"condicoes": "Ser processado não equivale a ser condenado. A proposta precisa distinguir investigados, acusados, presos provisórios e condenados. Qualquer restrição de circulação ou transferência deve respeitar presunção de inocência, devido processo, competência judicial, execução penal e direitos fundamentais.",
"questoes": "O período de aproximadamente 19 anos seria contado a partir de qual decisão? A medida seria aplicável somente após condenação definitiva? Como seria definida a cidade de destino?",
"esclarecimento": "O prazo de cerca de 19 anos é uma referência expressa do autor, não um prazo legal vigente nem uma regra cuja viabilidade esteja estabelecida."
},
{
"titulo": "Transferência interestadual em caso de reincidência",
"original": "cometeu outro crime em outra cidade, ele vai ter que mudar de estado, e ir para outro estado, ele tem todo o direito de ser brasileiro, andar no Brasil, menos nesses lugares que cometem crime, e se cometer crime em outro estado, é necessário ir para outro estado denovo",
"leitura": "A proposta complementa a anterior e sugere que, caso a pessoa volte a cometer crime em outra cidade, seja transferida para outro estado. O autor afirma que a pessoa manteria o direito de circular pelo Brasil, com exceção dos lugares em que cometeu crimes.",
"objetivos": ["Debater uma resposta à reincidência.", "Avaliar a proposta de afastamento dos locais relacionados aos delitos.", "Examinar a compatibilidade entre a ideia e a liberdade de circulação no território nacional."],
"possibilidades": ["Estudos sobre reincidência, prevenção e execução penal.", "Avaliação de medidas de proteção às vítimas e comunidades.", "Análise dos efeitos de transferências interestaduais sobre famílias, custos e reintegração."],
"condicoes": "A liberdade de locomoção, a competência dos entes federativos, a execução penal e as garantias judiciais precisam ser consideradas. Não se pode criar automaticamente uma proibição territorial ou transferência interestadual sem fundamento legal e decisão competente.",
"questoes": "A transferência ocorreria após condenação definitiva por novo crime? Como seriam identificados os locais de restrição? Quem fiscalizaria a medida e por quanto tempo?",
"esclarecimento": "A proposta não significa expulsão da nacionalidade ou perda da condição de brasileiro. A formulação sobre lugares em que a pessoa não poderia permanecer exige esclarecimento e análise constitucional."
},
{
"titulo": "Avaliação de comandantes e gestores da segurança pública",
"original": "todo comandante da policia militar, o responsável pelo físico da segurança, o delegado de policia e o representante da policia militar e não consegue combater o crime, precisa rebaixar o salário, serem mudados daquele local",
"leitura": "A proposta defende que comandantes, delegados e responsáveis pela gestão da segurança sejam avaliados pelos resultados de sua atuação e que a insuficiência no combate ao crime possa levar a mudanças de função ou local de trabalho e a consequências remuneratórias.",
"objetivos": ["Debater mecanismos de avaliação da gestão da segurança pública.", "Estimular responsabilidade por resultados e qualidade dos serviços.", "Examinar critérios para substituição ou transferência de gestores."],
"possibilidades": ["Indicadores públicos e contextualizados de desempenho.", "Avaliações institucionais periódicas.", "Análise de fatores externos que influenciam os índices de criminalidade.", "Procedimentos administrativos para mudanças de comando quando justificadas."],
"condicoes": "A avaliação deve considerar devido processo, direito de defesa, regras das carreiras, competências administrativas e fatores que não dependem exclusivamente do gestor. Alterações remuneratórias devem respeitar a Constituição e a legislação, sem redução arbitrária de salários.",
"questoes": "Quais indicadores definiriam que um gestor não conseguiu combater o crime? Quem faria a avaliação? O que significa 'responsável pelo físico da segurança'? Qual seria o procedimento para mudança de local ou remuneração?",
"esclarecimento": "A expressão 'responsável pelo físico da segurança' é mantida como trecho que necessita esclarecimento do autor; não foi reinterpretada como cargo específico."
},
{
"titulo": "Respeito e dignidade dos cidadãos nas delegacias e instituições públicas",
"original": "e que os cidadãos sejam respeitados na delegacia, e os postos de trabalho da policia do ministério publico e do poder judiciário, pq os cidadãos não estão sendo respeitados principalmente nas delegacias e pelos representantes da policia militar",
"leitura": "A proposta exige respeito aos cidadãos no atendimento realizado por delegacias, órgãos policiais, Ministério Público e Poder Judiciário. A declaração destaca a preocupação do autor com situações de desrespeito, especialmente em delegacias e no contato com representantes da Polícia Militar.",
"objetivos": ["Promover atendimento digno e respeitoso.", "Combater humilhação, abuso, discriminação e tratamento arbitrário.", "Valorizar a responsabilidade dos agentes e a confiança nas instituições."],
"possibilidades": ["Capacitação em atendimento ao público e direitos fundamentais.", "Canais acessíveis de reclamação e acompanhamento.", "Transparência sobre procedimentos e responsabilidades.", "Avaliação institucional da qualidade do atendimento."],
"condicoes": "A apuração de denúncias deve respeitar imparcialidade, contraditório, ampla defesa, proteção de dados e os canais legalmente competentes. A crítica institucional não deve ser confundida com acusação comprovada contra todos os profissionais.",
"questoes": "O autor pretende propor mecanismos específicos de fiscalização? Como seriam recebidas e acompanhadas as reclamações? Que medidas considera necessárias para melhorar o atendimento?",
"esclarecimento": "A declaração expressa uma preocupação com o tratamento dado aos cidadãos. Não apresenta levantamento estatístico ou afirmação comprovada sobre todos os agentes públicos."
},
{
"titulo": "Moradia como direito e acompanhamento das demandas habitacionais",
"original": "A moradia, e que todo o cidadão que não tenha casa para morar naquele estado, terá que registrar um processo no judiciário alegando que não tem casa para morar, e aue o estado e município responda na justiça e que passe o acompanhamento para aquela pessoa para adquirir o seu direito a moradia que está expresso na constituição Federal, que todo brasileiro tem direito a moradia, mas ninguem entra na justiça, que as pessoas que são de outro estado e chegam em outro estado para morar, terá o direito de questionar o seu direito de moradia em apenas em 5 anos",
"leitura": "A proposta defende que pessoas sem moradia possam buscar judicialmente a efetivação do direito à moradia, exigindo resposta e acompanhamento dos entes públicos responsáveis. Também apresenta uma condição de cinco anos para pessoas que chegam de outro estado, cuja aplicação precisa ser esclarecida e submetida a análise jurídica.",
"objetivos": ["Ampliar o conhecimento sobre o direito à moradia.", "Estimular respostas públicas às demandas habitacionais.", "Debater mecanismos de acompanhamento individual de pessoas sem moradia.", "Examinar a situação de pessoas que migram entre estados."],
"possibilidades": ["Orientação sobre serviços habitacionais e assistência jurídica.", "Canais de encaminhamento e acompanhamento das demandas.", "Integração entre políticas municipais, estaduais e federais.", "Estudos sobre critérios de atendimento e prioridades habitacionais."],
"condicoes": "O direito à moradia deve ser interpretado conforme a Constituição e a legislação aplicável. Não se pode afirmar que toda pessoa sem casa precise obrigatoriamente abrir processo judicial, nem que exista atualmente uma espera geral de cinco anos para migrantes. Critérios de residência devem ser analisados à luz da igualdade, dignidade e repartição de competências.",
"questoes": "O prazo de cinco anos seria contado a partir da chegada ao estado? A regra se aplicaria a todos os programas habitacionais ou apenas a uma modalidade? O acompanhamento seria judicial, administrativo ou ambos?",
"esclarecimento": "A referência a cinco anos é uma ideia original em debate, não uma exigência legal vigente. A expressão 'terá que registrar um processo' também exige avaliação sobre acesso à justiça e alternativas administrativas."
},
{
"titulo": "Federação e cooperação entre partidos com a mesma ideologia",
"original": "que os partidos políticos, aqueles que tenha a mesma ideologia se juntem como federação para defender a mesma proposta, e que toda a dificuldade que o pais tiver, os partidos políticos encaminhem uma declaração apoiando a punição de quem ofender o país, ou não",
"leitura": "A proposta defende que partidos com ideias convergentes possam se organizar em federações para defender propostas comuns. Também sugere declarações conjuntas diante de dificuldades nacionais e apresenta uma formulação sobre punição de quem ofender o país, que precisa ser esclarecida e analisada à luz dos direitos fundamentais.",
"objetivos": ["Estimular cooperação programática entre partidos.", "Debater a formação de federações partidárias.", "Promover manifestações conjuntas sobre questões nacionais.", "Esclarecer o sentido da responsabilização mencionada na declaração."],
"possibilidades": ["Debates e documentos conjuntos sobre propostas convergentes.", "Estudos sobre federações e regras eleitorais vigentes.", "Manifestações institucionais em defesa da soberania e das instituições democráticas."],
"condicoes": "Federações partidárias devem obedecer à legislação eleitoral. Qualquer punição exige conduta legalmente definida, competência, devido processo e respeito à liberdade de expressão e aos direitos fundamentais. Discordância, crítica ou opinião política não podem ser tratadas automaticamente como ofensa punível.",
"questoes": "O que significa 'ofender o país'? O autor se refere a crimes já previstos em lei, atos contra a soberania ou outra conduta? A declaração conjunta seria política ou teria algum efeito jurídico pretendido?",
"esclarecimento": "O trecho final 'ou não' é preservado na transcrição original e demonstra que o alcance da ideia ainda precisa ser esclarecido."
}
]

def lista(itens):
    return "<ul>" + "".join("<li>" + escape(x) + "</li>" for x in itens) + "</ul>"

cartoes = []
for i, p in enumerate(propostas, 1):
    corpo = f"""
      <div class="proposal-content">
        <div class="proposal-original">
          <h4>Declaração original</h4>
          <blockquote>{escape(p['original'])}</blockquote>
        </div>
        <div class="proposal-analysis">
          <h4>Explicação e alcance da proposta</h4>
          <p>{escape(p['leitura'])}</p>
          <h4>Objetivos apresentados</h4>
          {lista(p['objetivos'])}
          <h4>Possibilidades para debate e implementação</h4>
          {lista(p['possibilidades'])}
          <h4>Condições e responsabilidades</h4>
          <p>{escape(p['condicoes'])}</p>
          <h4>Questões jurídicas, técnicas, econômicas e administrativas</h4>
          <p>{escape(p['questoes'])}</p>
          <h4>Pontos que dependem de esclarecimento do autor</h4>
          <p>{escape(p['esclarecimento'])}</p>
        </div>
      </div>"""
    cartoes.append(
        f'<details class="proposal-card">'
        f'<summary><span>{i:02d}</span><h3>{escape(p["titulo"])}</h3></summary>'
        f'{corpo}</details>'
    )

complementares = """
    <section class="proposal-supplement">
      <h3>Declaração complementar sobre educação e formação profissional</h3>
      <blockquote>“A formação profissional de curso superior, é responsabilidade da união, e dos Estados, que está expresso na constituição Federal, o direito da educação é direito do cidadão e dever do estado, mas ninguém briga na justiça contra o estado, que devemos trabalhar mais com a escola técnica para que o povo aprenda a trabalhar, do que mesmo no geral do curso superior”</blockquote>
      <p>Esta declaração complementar expressa a compreensão do autor sobre a responsabilidade do poder público pela educação e sua defesa do fortalecimento do ensino técnico. Não integra a numeração das 16 propostas e não deve ser apresentada como transcrição literal ou interpretação jurídica definitiva da Constituição.</p>
    </section>
    <section class="proposal-supplement">
      <h3>Declaração complementar sobre conhecimento constitucional e desenvolvimento do trabalho</h3>
      <blockquote>“E também que quando o PMCB estuda as leis da constituição Federal é para que tenham conhecimentos das leis, suponhamos, a constituição Federal determina que todo brasileiro precisa se desenvolver com iniciativa do trabalho, trabalhando, que o brasileiro precisa desenvolver”</blockquote>
      <p>O autor relaciona o estudo da Constituição à compreensão das leis e à valorização da iniciativa do trabalho e do desenvolvimento dos brasileiros. A referência é ao PMCB nesta declaração. Ela não autoriza alterar automaticamente referências históricas a outras siglas, cuja documentação ainda precisa ser examinada.</p>
    </section>
    <section class="proposal-supplement">
      <h3>Declaração complementar sobre terra, agricultura e preservação ambiental</h3>
      <p>O autor também apresenta ideias complementares que não devem ser confundidas com as 16 propostas numeradas:</p>
      <ul>
        <li>Mobilização de pessoas de diferentes funções e posições sociais, inclusive do Presidente da República ao trabalhador da limpeza urbana, durante o período de plantio, por meio de uma iniciativa cuja forma legal ainda precisa ser definida.</li>
        <li>Referência a outubro, novembro e dezembro como meses de mobilização em torno da terra, preservando a distinção em relação à proposta original do Dia da Terra em novembro e dezembro.</li>
        <li>Aquisição de terras próximas às rodovias para possibilitar que famílias trabalhem e vivam da terra.</li>
        <li>A partir da faixa de 300 metros mencionada pelo autor, apoio estatal ao agronegócio e à produção de grãos destinados à exportação. Essa finalidade é distinta da destinação de áreas para famílias trabalhadoras.</li>
        <li>Cooperação de empresários com trabalhadores da terra durante novembro e dezembro, como ideia distinta do apoio estatal ao agronegócio.</li>
        <li>Reflexão sobre responsabilidade dos cidadãos em relação ao país e sobre condutas que prejudiquem a sociedade, sem criar punições ou órgãos que o autor não especificou.</li>
        <li>Preservação de rios, nascentes, matas ciliares e animais, incluindo cães, gatos, cavalos e bovinos.</li>
        <li>Debate sobre uma faixa de preservação de 50 a 100 metros ao redor de cada nascente, como proposta do autor, não como afirmação de que essa seja automaticamente a regra legal aplicável.</li>
      </ul>
      <p>As medidas dependem de esclarecimento, estudos ambientais, fundiários, técnicos, econômicos e jurídicos. Nenhuma obrigação, sanção ou dimensão deve ser inventada.</p>
    </section>
    <section class="proposal-supplement">
      <h3>Memória e registro dos colaboradores</h3>
      <p>O registro histórico de fundadores, organizadores, representantes, voluntários e colaboradores permanece como conteúdo institucional complementar, separado das 16 propostas originais. Sua organização deverá respeitar a privacidade, a proteção de dados e a autorização ou outra base legal adequada para divulgação.</p>
    </section>
"""

secao = f"""
{inicio}
  <div class="section-heading centered">
    <span class="eyebrow">IDEIAS PARA O BRASIL</span>
    <h2>As 16 propostas originais do PMCB.</h2>
    <p>As declarações originais são apresentadas separadamente de suas explicações editoriais. As análises ampliam o entendimento das ideias sem substituir a formulação do autor. Todas permanecem abertas a debate e dependem de esclarecimentos e estudos de viabilidade.</p>
  </div>
  <div class="proposal-grid proposal-accordion">
    {''.join(cartoes)}
  </div>
  {complementares}
  <p class="disclaimer">As 16 propostas e as declarações complementares são ideias apresentadas para debate. Não constituem, por si mesmas, programa partidário definitivo aprovado por convenção, nem devem ser confundidas com legislação vigente. Sua eventual adoção depende de deliberação institucional, participação pública e análises jurídicas, técnicas, econômicas, ambientais, administrativas e orçamentárias.</p>
</section>
"""

novo = conteudo[:conteudo.index(inicio)] + secao + "\n" + conteudo[conteudo.index(fim):]

if novo.count('class="proposal-card"') != 16:
    sys.exit("ERRO: a validação não encontrou exatamente 16 cartões. Arquivo original preservado.")

if novo.count(fim) != 1:
    sys.exit("ERRO: a seção seguinte não foi preservada. Arquivo original preservado.")

backup = Path("backups") / f"index-antes-16-propostas-{datetime.now().strftime('%Y%m%d-%H%M%S')}.html"
backup.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(arquivo, backup)

arquivo.write_text(novo, encoding="utf-8")

verificacao = arquivo.read_text(encoding="utf-8")
quantidade = len(re.findall(r'<details class="proposal-card">', verificacao))

if quantidade != 16 or inicio not in verificacao or fim not in verificacao:
    shutil.copy2(backup, arquivo)
    sys.exit("ERRO na validação final. O arquivo anterior foi restaurado.")

print("ALTERAÇÃO CONCLUÍDA.")
print("Propostas individuais:", quantidade)
print("Declarações complementares: incluídas separadamente.")
print("Seção de reconstrução: preservada.")
print("Backup:", backup)
print("Banco de dados, servidor e painel administrativo: não alterados.")
