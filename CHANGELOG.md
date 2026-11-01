# Changelog

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/).

## [2.2.0] — 2026-11-01
### Adicionado
- **Blog** em `/blog/` com 23 edições da newsletter "Autista Empreende" do LinkedIn
  (fev–set/2026), em quatro temas: Autismo, carreira e inclusão; Contabilidade,
  compliance e IA; Cripto e fintech; Vida, jogos e opinião. Cada artigo tem página
  própria com JSON-LD `BlogPosting`, link para o original no LinkedIn e "Continue lendo".
- Seção "Do blog" na página inicial (3 textos mais recentes sobre autismo e trabalho)
  e link "Blog" no menu.
- `tools/gerar_blog.py`: gera o blog a partir da exportação de artigos do LinkedIn.
- `sitemap.xml` com as 25 URLs; `llms.txt` com a lista de artigos.

### Não publicado (de propósito)
- "Carta aberta para o prefeito de São Paulo Ricardo Nunes": o texto traz CPF e
  endereço residencial do autor.
- 2 rascunhos não publicados e 12 artigos antigos (2016–2021) fora da newsletter.
- Imagens dos artigos (hospedadas no LinkedIn; quebrariam a regra de zero requisição externa).

## [2.1.0] — 2026-10-31
### Adicionado
- Seção **"Na mídia"** (podcast Carreira e Suas Vozes; matérias Gamers & Games e GeekPop
  News sobre o LAIC) e link "Na mídia" no menu.
- Seção **"Perguntas frequentes"** (MEI, cota PCD, intraempreendedorismo, privacidade,
  quem criou) com JSON-LD `FAQPage`.
- JSON-LD `WebSite`; `Organization` com `@id`, `alternateName`, `areaServed` e `knowsAbout`.
- `llms.txt`; `docs/na-midia.md` (levantamento de publicações) e `docs/plano-de-busca.md`.

### Alterado
- `<title>` e keywords com os termos de busca do público.
- `sitemap.xml` com `lastmod` 2026-10-31.

## [2.0.1] — 2026-10-31
### Alterado
- Hospedagem definida: **Hostinger**. `AGENTS.md` e `README.md` atualizados; o pacote
  de envio leva só os arquivos do site.

## [2.0.0] — 2026-10-31
### Alterado
- Redesenho completo, mais moderno: hero escuro em "aurora" azul com colagem da
  foto e da logo e selos (CRC-SP, Autista · PCD), faixa de números sobreposta,
  ferramentas em mosaico com o Simulador MEI em destaque, caminhos A/B, sete
  pontos em grade numerada e bloco de contato em destaque. Amarelo como cor de
  destaque, junto com os azuis da logo.

### Adicionado
- Seção **"A história por trás"**: linha do tempo de 2016 ao primeiro dia na
  Caldeira OTC (dados públicos do joao.abitante.net).
- "Quem faz" com cargo atual, formação (Ciências Contábeis, pós em Controladoria
  pela FECAP), especialidade (PLD/FT, AML, KYC/KYB) e link para o LinkedIn.
- LinkedIn no bloco de contato e no JSON-LD; card "Ecossistema" com as demais
  ferramentas do autor.

## [1.2.0] — 2026-10-07
### Adicionado
- `vercel.json` com os headers de segurança e passo a passo da Vercel no README.

## [1.1.0] — 2026-10-07
### Alterado
- Layout novo, mais moderno: cabeçalho fixo com desfoque, hero em duas colunas,
  cards de ferramentas com ícone, faixas escuras, sete pontos em grade e bloco de
  contato em destaque.
- Identidade do Autista Empreende aplicada: logo (duas pessoas conversando)
  redesenhada em SVG (`logo.svg`, também embutida na página e no favicon), paleta
  azul da marca e o lema "Interação e empreendedorismo".
- `og-image.png` refeita com a logo.
- Foto de João Carlos Bueno Abitante (a mesma do joao.abitante.net) no bloco
  "Quem faz", no lugar das iniciais, embutida na página (JPEG 400×400).

## [1.0.0] — 2026-10-07
### Adicionado
- Primeira versão do site: ferramentas (Simulador MEI, Parcelamento Federal,
  NeuroCompliance NR-1), empreender × intraempreender (sete pontos), para empresas
  (NR-1), quem faz e contato. Tema claro/escuro automático, sem animação, contraste AA.
- `.htaccess` para Hostinger com HTTPS, headers de segurança e cache.
- `og-image.png`, `robots.txt`, `sitemap.xml`.
