# Domains & DNS

## demo.g-track.eu
1. Add the domain in Vercel → **Projects** → **gtrack-app** → **Settings** → **Domains** → add `demo.g-track.eu`.
2. Configure DNS provider to point the `demo` CNAME record to `cname.vercel-dns.com`.
3. Verify that host-based rewrites defined in `next.config.js` serve assets from `/demo/drivers/`.
