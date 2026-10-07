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
- `vercel.json` — os mesmos headers de segurança, para quando o site roda na Vercel.
- `robots.txt`, `sitemap.xml` — indexação.

## Publicar na Vercel (via GitHub)
1. No GitHub, criar um repositório novo (ex.: `autistaempreende`) e enviar **o conteúdo**
   desta pasta para a raiz dele (Add file → Upload files). Inclua o `vercel.json`.
2. Na Vercel (time CONTBITTAX): **Add New → Project** → importar esse repositório.
   Framework Preset: **Other**. Build Command e Output Directory: deixar vazios.
3. Deploy. Depois, em **Settings → Domains**, adicionar `autistaempreende.com.br` e
   `www.autistaempreende.com.br` (redirecionando o `www` para o sem `www`).
4. No DNS do domínio, criar os registros que a Vercel mostrar (no Cloudflare: proxy cinza).

O `.htaccess` não tem efeito na Vercel; ele fica para o caso de usar a Hostinger.
Deploy só por push no GitHub: nada de `vercel --prod` nem edição no painel.

## Publicar na Hostinger
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
