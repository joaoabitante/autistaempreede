# Autista Empreende

Repositório: https://github.com/joaoabitante/autistaempreede

Site da iniciativa **Autista Empreende**, de João Carlos Bueno Abitante
(Contador CRC-SP 320961/O-4, autista PCD). Domínio: **https://autistaempreende.com.br/**
(canonical, OpenGraph e sitemap já apontam para ele).

Página única, autocontida: HTML + CSS, **sem JavaScript**, sem fonte web, sem CDN,
sem analytics. O CSP bloqueia qualquer requisição de rede em runtime.

## Arquivos
- `index.html` — o site inteiro.
- `og-image.png` — imagem de compartilhamento (1200×630).
- `logo.svg` — logo redesenhada em vetor (a página já traz a logo embutida; este arquivo é para reuso).
- `.htaccess` — HTTPS obrigatório, sem `www`, headers de segurança (CSP, HSTS,
  nosniff, no-referrer, DENY) e cache. Arquivo oculto: confira se ele subiu.
- `vercel.json` — reserva, caso o site um dia vá para a Vercel (não vai para a Hostinger).
- `robots.txt`, `sitemap.xml`, `llms.txt` — indexação (buscadores e assistentes de IA).
- `docs/na-midia.md` — onde o projeto já foi citado; `docs/plano-de-busca.md` — divulgação.

## Publicar na Hostinger (hospedagem oficial)
Enviar só os arquivos do site: `index.html`, `og-image.png`, `logo.svg`,
`robots.txt`, `sitemap.xml`, `llms.txt` e `.htaccess`. Os demais `.md` e o `vercel.json` ficam só no GitHub.

1. hPanel → **Sites** → `autistaempreende.com.br` → **Gerenciador de Arquivos**.
2. Abrir `public_html` e enviar **o conteúdo** desta pasta (não a pasta em si),
   incluindo o `.htaccess`. Se usar o `.zip`, enviar e clicar em **Extrair**.
3. Ativar o SSL gratuito em **Segurança → SSL** antes de testar (o `.htaccess`
   redireciona tudo para HTTPS).
4. Testar: https://autistaempreende.com.br/ e https://www.autistaempreende.com.br/
   (deve redirecionar para o sem `www`).

## Princípios de design
- Baixa estimulação: sem animação, paleta calma, contraste AA nos dois temas (claro/escuro automático).
- Texto direto, fonte grande, linhas curtas, link "pular para o conteúdo" e foco visível.
- Só cita ferramentas que existem e estão no ar.
